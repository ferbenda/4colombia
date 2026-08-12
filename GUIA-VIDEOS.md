# Curar los videos — hoja de trabajo

La página aguanta **7 a 10 videos**. Ni menos (se ve vacía) ni más (deja de ser
curaduría y se vuelve un feed).

Todo se edita en **`videos.json`**. Nada de HTML.

---

## Qué video sirve y cuál no

El objetivo de esta página es que alguien mire y decida ayudar. Eso lo logran
tres tipos de video:

| Funciona | Por qué |
|---|---|
| **Un rescate en curso** | Tensión y desenlace. Se entiende sin una palabra. |
| **La escala del daño** | Una cuadra, un edificio caído, un dron sobre la zona. Da magnitud. |
| **Gente ayudando** | Cadenas humanas, voluntarios, vecinos. Muestra que el aporte se suma a algo. |

| No funciona | Por qué |
|---|---|
| Alguien hablando a cámara | Si es en español, el extranjero se va en 3 segundos. |
| Cifras y gráficos | Informa, no mueve. Para eso está el bloque de instituciones. |
| Cuerpos, heridos, familias llorando | Cruza la línea. Un directorio no hace morbo. |
| Video sin verificar | Un viral de otro país destruye toda la credibilidad. |

**La prueba de los 3 segundos:** silencia el video y míralo tres segundos. Si no
entiendes qué pasa, no va.

---

## Dónde buscarlos

- **TikTok / Instagram**: `#terremotocolombia`, `#sismocolombia`, `#pereira`,
  `#cali`, `#manizales`, `#quibdó`
- **X**: busca `terremoto Colombia` filtrando por Videos, ordenado por Populares
- **Cuentas que ya publican material bueno**: `@UNGRD`, `@DefensaCivilCo`,
  `@cruzrojacol`, `@rtvcnoticias`, `@PlataformaALTO` (animales)
- **En inglés**: AP, Reuters, CNN, NBC publican el mismo material con narración
  en inglés — esos merecen `destacado: true`.

---

## Verificar antes de publicar

Tres chequeos, un minuto cada uno:

1. **Fecha del post**: 10 de agosto de 2026 o después.
2. **El lugar coincide**: nombres de calles, comercios, placas, acentos.
3. **Búsqueda inversa** si algo no cuadra: guarda un fotograma y súbelo a Google
   Imágenes. Si aparece en notas de 2023 o de Turquía, no es de este sismo.

---

## Sacar el enlace directo

**Nunca el perfil. Siempre el video.**

- **TikTok** -> Compartir -> Copiar enlace -> `tiktok.com/@usuario/video/7412...`
- **Instagram** -> tres puntos -> Copiar enlace -> `instagram.com/reel/CxYz.../`
- **X** -> la fecha del post -> Copiar enlace -> `x.com/usuario/status/1234...`

Si la URL termina en el nombre de la cuenta y nada más, **no sirve**.

---

## Plantilla

Copia y pega dentro de `"videos": [ ... ]`, separando cada bloque con coma:

```json
{
  "plataforma": "tiktok",
  "url": "https://www.tiktok.com/@usuario/video/7412345678901234567",
  "autor": "@usuario",
  "titulo_es": "Cadena humana para sacar a una mujer en Pereira",
  "titulo_en": "Human chain rescues a woman in Pereira",
  "idioma": "sin_texto",
  "destacado": false
}
```

- `plataforma`: `tiktok` / `instagram` / `x` / `youtube` / `web`
- `idioma`: `en` (hablan inglés) / `es` (español) / `sin_texto` (se entiende solo)
- `miniatura`: ruta a una imagen en `/img/thumbs/` (ver más abajo). Opcional.
- El orden del archivo es el orden en pantalla.
- El último bloque **no lleva coma** al final.

---

## Miniaturas

Todas las tarjetas son del mismo tamaño (vertical 3:4). Sin miniatura muestran
el color de la plataforma; con miniatura muestran la imagen del video.

**No se pueden traer automáticamente de Instagram ni Facebook**: bloquean el
acceso y sus direcciones de imagen vencen en días. Hay que capturarlas:

1. Pausa el video en el fotograma más representativo
2. Captura de pantalla, recorta a vertical 3:4, exporta a 360x480 px
3. Guarda en `img/thumbs/` con nombre claro: `rescate-cali.jpg`
4. En `videos.json` agrega al video: `"miniatura": "/img/thumbs/rescate-cali.jpg"`

Si el archivo falta, la tarjeta cae al degradado. Nunca se rompe.

## Orden recomendado

1. El más impactante primero — es el que más se mira
2. El resto, alternando: rescate -> daño -> gente ayudando -> rescate...

Termina con algo esperanzador. Justo debajo aparece el boton de donar, y esa es
la transición que importa.

---

## Cómo llegan los datos a la página

`videos.json` es la fuente, pero la galería **no la lee por red**: el script copia
los datos dentro de `fuentes.html`, entre los marcadores `DATOS-VIDEOS`. Por eso
la galería funciona servida, en local y aunque falle la conexión.

Si editas `videos.json` a mano, corre `python scripts/actualizar_videos.py`
—o edita `links.txt` y deja que GitHub lo haga— para que el bloque incrustado
quede al día. Nunca edites el bloque de `fuentes.html` directamente.

## Publicar

```bash
git add videos.json
git commit -m "Actualiza videos"
git push
```

Un minuto y está arriba. Antes de subir, pasa el archivo por **jsonlint.com**:
una coma de más deja la sección vacía.

**Revisa cada dos días.** Los virales se borran o se hacen privados; un enlace
roto en la primera posición hace ver el sitio abandonado.
