# Dos páginas HTML conectadas

Proyecto educativo completo para explicar cómo una primera página HTML recibe datos y cómo una segunda página los procesa y muestra.

## Archivos

- `two_html_pages_manim.py`: video didáctico completo en ManimCE.
- `web_demo/index.html`: página 1, formulario de entrada.
- `web_demo/resultado.html`: página 2, estructura de resultados.
- `web_demo/styles.css`: estilos compartidos.
- `web_demo/resultado.js`: lectura, validación, transformación y escritura en el DOM.

## Flujo

1. El usuario completa `index.html`.
2. El formulario usa `action="resultado.html"` y `method="get"`.
3. El navegador abre una URL como:

   ```text
   resultado.html?nombre=Ana+Torres&edad=14&curso=8-B&tema=HTML+y+CSS
   ```

4. `resultado.js` usa `URLSearchParams` para recuperar los datos.
5. JavaScript limpia el nombre, convierte la edad, valida el rango, calcula la próxima edad y clasifica el valor.
6. `textContent` escribe los resultados en `resultado.html`.

## Probar el sitio

Abre `web_demo/index.html` en un navegador. El ejemplo funciona como sitio estático y no necesita servidor.

## Render ManimCE

Prueba de protocolo:

```bash
manim -pql two_html_pages_manim.py HTMLTwoPagesCourse --format=mp4 --disable_caching
```

Render final:

```bash
manim -pqh two_html_pages_manim.py HTMLTwoPagesCourse --format=mp4 --disable_caching
```

En automatización sin entorno gráfico, `-ql` y `-qh` producen la misma calidad sin intentar abrir el reproductor.
