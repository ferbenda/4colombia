# Cómo actualizar los videos

Todo vive en **`videos.json`**. Es el único archivo que tocas. No hay que
editar HTML ni CSS.

---

## Agregar un video

Copia este bloque y pégalo dentro de `"videos": [ ... ]`, separado por coma:

```json
{
  "plataforma": "tiktok",
  "url": "https://www.tiktok.com/@usuario/video/123456789",
  "autor": "@usuario",
  "titulo_es": "Rescate en el centro de Pereira",
  "titulo_en": "Rescue in downtown Pereira",
  "idioma": "sin_texto"
}
```

### Los campos

| Campo | Qué poner |
|---|---|
| `plataforma` | `tiktok` · `instagram` · `x` · `youtube` · `web` |
| `url` | **El enlace del video en sí, nunca de un perfil ni de una portada** |
| `autor` | El @ o el nombre del medio |
| `titulo_es` | Qué se ve, en español |
| `titulo_en` | Lo mismo en inglés (**no lo dejes vacío**) |
| `idioma` | `en` si se habla inglés · `es` si es en español · `sin_texto` si se entiende solo con la imagen |
| `destacado` | `true` para que salga con borde rojo. Máximo dos o tres. |

**El orden del archivo es el orden en pantalla.** Lo más importante arriba.

---

## Consejos de curaduría

- **Prioriza lo que se entiende sin idioma.** Un rescate, una calle, un edificio.
  Ahí el video hace lo que el texto no puede.
- **Marca bien el idioma.** Un extranjero ve la etiqueta y sabe si le va a servir.
- **Siempre la URL del video, nunca del perfil.** Es la regla que no se rompe.
  Alguien que llega buscando ver lo que pasó no debe aterrizar en una cuenta y
  tener que buscar entre publicaciones.

  Cómo sacar el enlace directo:
  - **TikTok**: abre el video, botón Compartir → Copiar enlace. Queda así:
    `tiktok.com/@usuario/video/7412...`
  - **Instagram**: abre el reel, los tres puntos → Copiar enlace. Queda así:
    `instagram.com/reel/CxYz.../`
  - **X**: la fecha del post → Copiar enlace. Queda así:
    `x.com/usuario/status/1234...`
  - Si la URL termina en el nombre de la cuenta y nada más, **no sirve**.
- **Nada de contenido gráfico**: cuerpos, personas heridas identificables,
  familias en el peor momento. Es un directorio, no morbo.
- **Verifica que sea de ESTE sismo.** Es lo que promete el título de la página.
  En emergencia circula muchísimo video antiguo o de otro país, a veces con
  millones de vistas. Contrasta contra la cobertura del 10 de agosto: el edificio,
  la ciudad, la fecha del post. Si no lo puedes confirmar, no lo pongas.
- **Revisa cada dos días.** Los videos virales se borran o se hacen privados.
  Un enlace roto en la primera posición hace que el sitio parezca abandonado.

---

## Publicar el cambio

```bash
git add videos.json
git commit -m "Actualiza videos"
git push
```

Vercel redespliega solo en un minuto. Si el JSON queda mal escrito (una coma de
más, una comilla suelta), la sección muestra un aviso en vez de romper la página
— pero conviene revisarlo antes en jsonlint.com.

---

## Si algo no aparece

- **Ningún video se muestra** → error de sintaxis en el JSON.
- **Uno solo falta** → revisa que su bloque tenga todas las comillas y esté
  separado del anterior por coma.
- **El último bloque** no lleva coma al final.
