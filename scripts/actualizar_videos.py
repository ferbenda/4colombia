"""
Convierte links.txt en videos.json.

Uso:  python scripts/actualizar_videos.py

Cada línea de links.txt es una URL. Opcionalmente, título en español e inglés
separados por |:

    https://www.tiktok.com/@usuario/video/7412...
    https://www.instagram.com/reel/Abc123/ | Rescate en Pereira | Rescue in Pereira | @autor | sin_texto

El quinto campo es el idioma: en / es / sin_texto (se entiende solo con la imagen).

Lo que se puede sacar automáticamente (TikTok, YouTube, X) se saca vía oEmbed:
título, autor y miniatura, que se descarga al repo para que no venza.
Instagram y Facebook no tienen oEmbed público: quedan con lo que traiga la línea.

Si un video ya está en videos.json con título o miniatura, se conserva: nunca se
pisa el trabajo manual.
"""

import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Parámetros que solo sirven para rastrear; el resto se conserva porque a veces
# lleva el identificador del video (youtube.com/watch?v=...).
RASTREO = {"igsh", "igshid", "mibextid", "fbclid", "si", "feature", "s", "t",
           "is_from_webapp", "sender_device", "web_id", "_r", "_t", "lang", "q",
           "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"}


def limpiar(url: str) -> str:
    partes = urllib.parse.urlsplit(url)
    query = [(k, v) for k, v in urllib.parse.parse_qsl(partes.query)
             if k.lower() not in RASTREO]
    return urllib.parse.urlunsplit(
        (partes.scheme, partes.netloc, partes.path,
         urllib.parse.urlencode(query), ""))

RAIZ = Path(__file__).resolve().parent.parent
LINKS = RAIZ / "links.txt"
SALIDA = RAIZ / "videos.json"
THUMBS = RAIZ / "img" / "thumbs"
AGENTE = "Mozilla/5.0 (compatible; 4colombia/1.0; +https://4colombia.com)"

OEMBED = {
    "tiktok": "https://www.tiktok.com/oembed?url=",
    "youtube": "https://www.youtube.com/oembed?format=json&url=",
    "x": "https://publish.twitter.com/oembed?omit_script=1&url=",
}

TITULO_GENERICO = {
    "tiktok": ("Video en TikTok", "Video on TikTok"),
    "instagram": ("Video en Instagram", "Video on Instagram"),
    "facebook": ("Video en Facebook", "Video on Facebook"),
    "x": ("Video en X", "Video on X"),
    "youtube": ("Video en YouTube", "Video on YouTube"),
    "web": ("Ver video", "Watch video"),
}


def plataforma_de(url: str) -> str:
    d = url.lower()
    if "tiktok.com" in d: return "tiktok"
    if "instagram.com" in d: return "instagram"
    if "facebook.com" in d or "fb.watch" in d: return "facebook"
    if "twitter.com" in d or "x.com" in d: return "x"
    if "youtube.com" in d or "youtu.be" in d: return "youtube"
    return "web"


def autor_de(url: str) -> str:
    """Respaldo cuando oEmbed no responde: el @ suele estar en la propia URL."""
    m = re.search(r"(?:tiktok\.com|instagram\.com|(?:twitter|x)\.com)/@?([A-Za-z0-9_.]+)", url)
    reservadas = {"reel", "reels", "p", "tv", "share", "video", "status", "watch", "explore"}
    if m and m.group(1) not in reservadas:
        return "@" + m.group(1)
    return ""


def pedir(url: str, binario=False, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binario else json.loads(r.read().decode("utf-8"))


def bajar_miniatura(url_img: str, clave: str) -> str:
    """Descarga la miniatura al repo. Las URL de las plataformas vencen; los archivos no."""
    destino = THUMBS / f"{clave}.jpg"
    if destino.exists():
        return f"/img/thumbs/{destino.name}"
    THUMBS.mkdir(parents=True, exist_ok=True)
    datos = pedir(url_img, binario=True)
    try:
        from PIL import Image
        from io import BytesIO
        im = Image.open(BytesIO(datos)).convert("RGB")
        ancho = int(im.height * 3 / 4)
        if ancho <= im.width:                       # recorte vertical centrado
            x = (im.width - ancho) // 2
            im = im.crop((x, 0, x + ancho, im.height))
        im.resize((360, 480), Image.LANCZOS).save(destino, "JPEG", quality=80, optimize=True)
    except ImportError:
        destino.write_bytes(datos)                  # sin Pillow: se guarda tal cual
    return f"/img/thumbs/{destino.name}"


def enriquecer(url: str, plat: str) -> dict:
    """Consulta oEmbed. Devuelve {} si la plataforma no lo ofrece o si falla."""
    if plat not in OEMBED:
        return {}
    try:
        d = pedir(OEMBED[plat] + urllib.parse.quote(url, safe=""))
    except Exception as e:
        print(f"  aviso: oEmbed falló ({e})")
        return {}

    datos = {}
    if d.get("author_name"):
        datos["autor"] = d["author_name"] if plat == "youtube" else "@" + d["author_name"].lstrip("@")
    titulo = (d.get("title") or "").strip()
    if plat == "x":                                  # X devuelve el tuit en HTML
        titulo = re.sub(r"<[^>]+>", " ", d.get("html", ""))
        titulo = re.sub(r"https?://\S+", "", titulo)
        titulo = " ".join(titulo.split())[:110]
    if titulo:
        datos["titulo_es"] = titulo[:120]
    if d.get("thumbnail_url"):
        clave = hashlib.sha1(url.encode()).hexdigest()[:10]
        try:
            datos["miniatura"] = bajar_miniatura(d["thumbnail_url"], clave)
        except Exception as e:
            print(f"  aviso: no se pudo bajar la miniatura ({e})")
    return datos


def main():
    if not LINKS.exists():
        sys.exit(f"Falta {LINKS.name}")

    previos = {}
    if SALIDA.exists():
        d = json.loads(SALIDA.read_text(encoding="utf-8"))
        previos = {v["url"] if isinstance(v, dict) else v: v for v in d.get("videos", [])}

    videos = []
    for linea in LINKS.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        partes = [p.strip() for p in linea.split("|")]
        url = limpiar(partes[0])
        plat = plataforma_de(url)
        print(f"{plat:10} {url}")

        anterior = previos.get(url) or {}
        if isinstance(anterior, str):
            anterior = {}
        v = {"url": url, "plataforma": plat}
        v.update({k: val for k, val in anterior.items() if val})   # nunca pisar lo manual

        if not v.get("miniatura") or not v.get("titulo_es"):
            v.update({k: val for k, val in enriquecer(url, plat).items()
                      if not v.get(k)})

        if len(partes) > 1 and partes[1]:
            v["titulo_es"] = partes[1]
        if len(partes) > 2 and partes[2]:
            v["titulo_en"] = partes[2]
        if len(partes) > 3 and partes[3]:
            v["autor"] = partes[3]
        if len(partes) > 4 and partes[4] in ("en", "es", "sin_texto"):
            v["idioma"] = partes[4]

        gen_es, gen_en = TITULO_GENERICO[plat]
        v.setdefault("titulo_es", gen_es)
        v.setdefault("titulo_en", v["titulo_es"] if v["titulo_es"] != gen_es else gen_en)
        v.setdefault("autor", autor_de(url))
        v.setdefault("idioma", "")
        v.setdefault("miniatura", "")
        videos.append(v)

    SALIDA.write_text(json.dumps({
        "_leeme": "GENERADO por scripts/actualizar_videos.py — edita links.txt, no este archivo.",
        "actualizado": __import__("datetime").date.today().isoformat(),
        "videos": videos,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    con_mini = sum(1 for v in videos if v["miniatura"])
    print(f"\n{len(videos)} videos · {con_mini} con miniatura -> videos.json")


if __name__ == "__main__":
    main()
