# Sismo Colombia — dónde donar y dónde informarse

Sitio estático de dos páginas. Sin backend, sin base de datos, sin pipeline.

```
index.html     portada
ayudar.html    canales de donación verificados, con selector de país
fuentes.html   video de la emergencia + cuentas oficiales
videos.json    lista de videos (se edita sola, ver GUIA-VIDEOS.md)
legal.html     privacidad y términos
img/           fondos ilustrados, logo y favicon
  logo.png       marca horizontal (barra de navegación y portada)
  icono.png      el "4" tricolor — favicon y icono de app
  og.jpg         imagen que aparece al compartir el enlace
robots.txt     indexación
sitemap.xml    mapa del sitio
vercel.json    cabeceras de seguridad y caché
```

## Videos

`fuentes.html` lee la sección de video de `videos.json`. Para actualizarla no se
toca el HTML: se edita ese archivo y se hace push. Instrucciones completas en
`GUIA-VIDEOS.md`.

## Seguridad

HTTPS obligatorio: Vercel emite el certificado y redirige todo el tráfico.
`Strict-Transport-Security` con `preload` obliga al navegador a usar HTTPS
incluso en la primera visita, una vez el dominio esté en la lista de precarga
(se envía en hstspreload.org, es gratis y tarda unas semanas).

Once cabeceras de seguridad activas, entre ellas CSP con `default-src 'none'`,
COEP/COOP/CORP para aislar el sitio, y `Permissions-Policy` con todos los
permisos del navegador desactivados.

El sitio no tiene backend, API keys, formularios, cookies de seguimiento ni
llamadas de red. Lo único que guarda es la preferencia de idioma en
`localStorage`. `vercel.json` aplica CSP estricta (`default-src 'none'`),
HSTS, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer` y
`Permissions-Policy` con todo desactivado.

Al agregar contenido: no introducir scripts externos, `fetch`, formularios ni
`innerHTML` alimentado por texto libre del usuario — cualquiera de esos rompe
el modelo de seguridad actual.

## Idiomas

Todo el sitio es bilingüe: español por defecto, inglés con un botón. La elección
persiste entre páginas vía `localStorage`, con respaldo en el parámetro `?lang=en`
por si el navegador bloquea el almacenamiento. Título, descripción y `og:title`
cambian con el idioma.

Al traducir contenido nuevo, envolverlo siempre en el par
`<span lang-es>…</span><span lang-en>…</span>`. Los nombres propios, arrobas y
nombres de plataforma no se traducen.

## Alcance

**Hace dos cosas:**
1. Informa dónde donar de forma segura, con tarjeta, desde cualquier país.
2. Recomienda fuentes oficiales de información.

**No hace nada más.** No recibe dinero, no procesa pagos, no publica noticias, no
reproduce contenido de terceros y no maneja información de personas — ni nombres,
ni fotos, ni identidades. Quien busca a un familiar es remitido a la Cruz Roja
Colombiana y al Registro Nacional de Desaparecidos de Medicina Legal.

Ese límite es deliberado: mantiene el proyecto fuera del régimen de datos personales
(Ley 1581 de 2012) y elimina la necesidad de convenios con terceros.

## Desplegar

```bash
git init && git add . && git commit -m "inicial"
git remote add origin git@github.com:<usuario>/<repo>.git && git push -u origin main
```

Vercel → Add New → Project → importar el repo:

| Campo | Valor |
|---|---|
| Framework Preset | Other |
| Root Directory | `./` |
| Build Command | (vacío) |
| Output Directory | (vacío) |

Sin build. Sin variables de entorno. Sin cron.

## Mantenimiento

No hay proceso automático. El sitio no se rompe solo, pero **sí se desactualiza**.

**Pendiente:** la sección de animales entra solo por Plataforma ALTO, que verifica
refugio por refugio. Si se confirman canales de pago de refugios concretos, se pueden
añadir; no publicar ninguno sin confirmar que la cuenta es de la fundación.

**Revisión semanal (20 minutos):**
1. Abrir los enlaces de donación y confirmar que cargan y aceptan pago
2. Confirmar que las cuentas oficiales siguen activas
3. Actualizar la constante `VERIFICADO` en `ayudar.html` y `fuentes.html`
4. Si se agregó texto nuevo, confirmar que tiene su par en inglés

Esa fecha aparece al pie de cada página. Si lleva más de dos semanas sin moverse,
el sitio pierde el único respaldo que tiene: que alguien lo revisó.

## Analítica

Vercel Web Analytics y Speed Insights, cargados desde `/_vercel/...` (mismo
origen). **Hay que activarlos en el panel de Vercel** — Project → Analytics →
Enable, y Speed Insights → Enable. Sin eso los scripts devuelven 404 y no se
registra nada.

Sin cookies, sin identificadores persistentes, sin datos personales. Por eso la
CSP solo necesitó `connect-src 'self'`.

## Fotos de perfil de las organizaciones

El `<img>` ya está puesto en cada tarjeta. Solo falta subir el archivo a
`img/logos/` con el nombre exacto (ver `img/logos/LEEME.txt`). Si el archivo no
existe, la tarjeta cae a las iniciales — no se rompe nada mientras tanto.

**Nunca enlazar desde `scontent.cdninstagram.com`**: esas direcciones llevan
firma con vencimiento y dejan de cargar en días. Descargar, recortar a cuadrado
200x200 y subir al repo.

Pedir la imagen y el permiso en el mismo correo de autorización.

## Reglas editoriales

- Solo entidades con NIT verificable y canal de pago en su propio dominio
- Nunca publicar un número de cuenta o llave suelta: solo enlaces a página oficial
- Cero opinión, cero cifras propias, cero contenido reproducido de terceros
- Ninguna afirmación que no se pueda sostener (por ejemplo: "auditada")
