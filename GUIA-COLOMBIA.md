# Donaciones desde Colombia — cómo funciona y cómo llenarlo

La sección **"Desde Colombia"** está construida y oculta. Aparece sola en cuanto
agregues una cuenta en el bloque `datos-colombia` de `ayudar.html`.

---

## Primero, el sistema en corto

**Bre-B** es el sistema de pagos inmediatos del Banco de la República. Conecta a
todos los bancos y billeteras del país: la plata llega en segundos, gratis, a
cualquier hora.

Una **llave** es un alias que reemplaza el número de cuenta. Hay cuatro tipos:

| Tipo | Ejemplo | Cuándo usarla |
|---|---|---|
| Alfanumérica | `@fundacion123` | **La indicada para una fundación** |
| Celular | `3001234567` | Familia y conocidos |
| Documento | cédula o NIT | Clientes |
| Correo | `pagos@dominio.co` | Alternativa neutra |

**Para recibir donaciones usa la alfanumérica.** No expone tu cédula ni tu
celular, y puedes cambiarla sin cambiar de cuenta. Una llave apunta a una sola
cuenta, pero una cuenta puede tener varias llaves.

**Nequi** (Bancolombia) y **Daviplata** (Davivienda) son billeteras. Reciben por
número de celular, y también pueden tener llave Bre-B.

**Tope por transferencia:** alrededor de 10,9 millones de pesos, fijado por el
Banco de la República. Puede cambiar.

**Regla de seguridad que ya está en la página:** el dinero llega solo. Nadie
tiene que abrir un enlace para "aceptar" o "reclamar" una transferencia. Si
aparece un enlace así, es estafa.

---

## Qué necesitas antes de publicar

1. **La fundación constituida y con NIT.** El NIT se muestra en la tarjeta: es
   lo que permite a cualquiera verificarte en RUES.
2. **Una cuenta a nombre de la fundación**, no personal. Una cuenta personal
   recibiendo donaciones públicas es un problema contable y de confianza.
3. **Una llave alfanumérica** registrada a esa cuenta, desde la app del banco.
4. **Opcional:** Nequi o Daviplata empresarial, si quieres una vía más informal.

---

## Cómo llenarlo

En `ayudar.html`, entre los marcadores `DATOS-COLOMBIA`, reemplaza
`{"cuentas":[]}` por:

```json
{"cuentas":[
  {
    "nombre": "Nombre de la fundación",
    "nit": "901.234.567-8",
    "descripcion_es": "Qué hace con el dinero, en una línea.",
    "descripcion_en": "What it does with the money, in one line.",
    "medios": [
      {
        "tipo": "llave",
        "valor": "@tullave",
        "nota_es": "Llave alfanumérica Bre-B",
        "nota_en": "Bre-B alphanumeric key"
      },
      {
        "tipo": "nequi",
        "valor": "300 000 0000"
      },
      {
        "tipo": "cuenta",
        "valor": "123-456789-01",
        "nota_es": "Cuenta de ahorros Bancolombia",
        "nota_en": "Bancolombia savings account"
      }
    ]
  }
]}
```

**Campos opcionales de la tarjeta:**

- `foto`: ruta a un avatar en `/img/personas/` — cuadrado, 160x160 px, JPG.
  Se muestra redondo a 56 px. Sirve para que quien vio el video reconozca a la
  persona. Se saca de un fotograma: recorta cuadrado, exporta a 160x160.
- `tipo`: `"persona"` marca la tarjeta como individuo (borde amarillo y etiqueta
  "Persona, no fundación"). Se omite para fundaciones.
- `expira`: fecha en formato `2026-08-27`. La tarjeta se deja de mostrar ese
  día, sola, sin que nadie toque el sitio. Úsalo siempre en casos de personas:
  una necesidad puntual no debería seguir pidiendo dinero seis meses después.
  Mientras está publicada, la tarjeta muestra "Publicado hasta el 27 de agosto".
- `video`, `perfil` y `whatsapp`: enlaces bajo la descripción. En `whatsapp`
  va el número con indicativo (`+573145322215`); el enlace se arma solo.

**Campos de cada medio:**

- `tipo`: `llave` · `nequi` · `daviplata` · `cuenta` · `qr`
- `valor`: lo que la persona va a copiar. Escríbelo tal como se debe pegar.
- `nota_es` / `nota_en`: opcional, una línea aclaratoria.
- La etiqueta **"Solo desde Colombia"** se pone sola en cada tarjeta.

Cada valor sale con su botón **Copiar**, porque nadie transcribe a mano una
llave sin equivocarse.

---

## Antes de publicar tus datos

- **Verifica el valor carácter por carácter.** Un dígito mal en una llave manda
  la plata a un desconocido, y no hay reversa.
- **Prueba con una transferencia pequeña** desde otra cuenta antes de publicar.
- **Revísalo cada semana.** Si cambias de banco o de llave, el dato viejo sigue
  ahí cobrando.
- **Nunca publiques una cuenta personal.** Si aún no tienes la fundación, deja
  la sección vacía: es mejor no ofrecer la vía que ofrecerla mal.
