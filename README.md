# IJR — Seminario de Programación

Repositorio oficial del proyecto **Robledo Market Lab**, una aplicación web educativa construida con HTML, CSS y JavaScript puro para que los estudiantes puedan revisar una versión completa, funcional y documentada.

## Enlaces oficiales

- **Repositorio:** https://github.com/juanperez238421-cpu/IJR---Seminario
- **Página publicada:** https://juanperez238421-cpu.github.io/IJR---Seminario/
- **Rama oficial:** `main`
- **Versión de referencia:** `1.0.0`

La rama `main` contiene la versión vigente del proyecto. Los estudiantes deben usarla para estudiar la estructura, el flujo y la calidad esperada; no para copiar literalmente la solución.

## Qué incluye

- HTML semántico y accesible.
- CSS responsive con catálogo y panel de compra.
- Catálogo generado desde objetos JavaScript.
- Búsqueda y filtros por categoría.
- Carrito con cantidades y eliminación de productos.
- Estado centralizado mediante `CartStore`.
- Validación de nombre, correo, dirección y confirmación.
- Cupón de demostración `ROBLEDO10`.
- Cálculo de subtotal, descuento, domicilio y total.
- Persistencia con `localStorage`.
- Comprobante imprimible.
- Pruebas automáticas con Node.js.
- Guion docente, revisión técnica y lista de verificación estudiantil.

## Recorrido recomendado para estudiantes

1. Abrir la página publicada.
2. Buscar y filtrar productos.
3. Agregar productos y modificar cantidades.
4. Aplicar el cupón `ROBLEDO10`.
5. Cambiar entre recogida y domicilio.
6. Provocar y corregir errores de validación.
7. Generar el comprobante.
8. Recargar la página y comprobar la persistencia.
9. Abrir el código fuente y relacionar cada comportamiento con HTML, CSS y JavaScript.
10. Ejecutar las pruebas desde una copia local.

## Ejecutar localmente

### Windows

1. Descarga o clona este repositorio.
2. Abre la carpeta del proyecto.
3. Ejecuta `start-server.bat`.
4. Abre `http://localhost:8000`.

### Terminal

```bash
python -m http.server 8000
```

Luego abre:

```text
http://localhost:8000
```

## Ejecutar pruebas

Requiere Node.js 18 o superior:

```bash
npm test
```

## Estructura del repositorio

```text
IJR---Seminario/
├── index.html
├── receipt.html
├── css/
│   └── styles.css
├── js/
│   ├── app.js
│   ├── cart-store.js
│   ├── core.js
│   ├── products.js
│   ├── receipt.js
│   └── storage.js
├── tests/
│   └── core.test.js
├── docs/
│   ├── GUION_CLASE.md
│   ├── SOURCE_REVIEW.md
│   └── STUDENT_CHECKLIST.md
├── package.json
├── start-server.bat
└── start-server.sh
```

## Flujo principal

```text
Catálogo → agregar producto → actualizar estado → validar formulario
→ crear orden → guardar localmente → abrir comprobante → imprimir o reiniciar
```

## Nota pedagógica

La clase `CartStore` presenta una implementación orientada a objetos. Los estudiantes pueden alcanzar los requisitos mínimos usando funciones y objetos literales, pero deben mantener una separación clara entre estructura, estilos, datos, lógica y persistencia.

## Uso educativo

Este proyecto no procesa pagos reales, no utiliza credenciales y no envía información a servidores externos. Toda la información se conserva únicamente en el navegador del usuario mediante `localStorage`.
