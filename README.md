# Sismo Colombia — dónde donar y dónde informarse

Sitio estático de dos páginas. Sin backend, sin base de datos, sin pipeline.

```
publico/
  index.html     portada
  ayudar.html    canales de donación verificados, con selector de país
  fuentes.html   cuentas y sitios oficiales de información
vercel.json      cabeceras de seguridad y caché
```

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
| Root Directory | `publico` |
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

## Reglas editoriales

- Solo entidades con NIT verificable y canal de pago en su propio dominio
- Nunca publicar un número de cuenta o llave suelta: solo enlaces a página oficial
- Cero opinión, cero cifras propias, cero contenido reproducido de terceros
- Ninguna afirmación que no se pueda sostener (por ejemplo: "auditada")
