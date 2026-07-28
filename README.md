# IJR — Seminario de Programación

Repositorio oficial del proyecto **Robledo Market Lab**, una aplicación web educativa construida con HTML, CSS y JavaScript puro para que los estudiantes puedan revisar una versión completa, funcional y documentada.

También incluye un **tablero docente de seguimiento** para consultar commits públicos, registrar metas, calificar competencias y conservar observaciones individuales.

## Enlaces oficiales

- **Repositorio:** https://github.com/juanperez238421-cpu/IJR---Seminario
- **Proyecto de referencia:** https://juanperez238421-cpu.github.io/IJR---Seminario/
- **Seguimiento de estudiantes:** https://juanperez238421-cpu.github.io/IJR---Seminario/progress.html
- **Rama oficial:** `main`
- **Versión de referencia:** `1.1.0`

La rama `main` contiene la versión vigente. Los estudiantes deben estudiar la estructura, el flujo y la calidad esperada; no copiar literalmente la solución.

## Proyecto de referencia: Robledo Market Lab

Incluye:

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

## Tablero de seguimiento

`progress.html` permite:

- registrar estudiantes, grupos, repositorios y proyectos;
- consultar automáticamente el último commit público de GitHub;
- detectar commits pendientes de revisión;
- asignar una ruta de **consolidación funcional** o **especialización CSS**;
- marcar diez metas verificables;
- aplicar una rúbrica ponderada en escala de 0,0 a 5,0;
- registrar la siguiente meta y observaciones de la entrevista;
- marcar el SHA revisado;
- exportar e importar el seguimiento en JSON.

Las consultas de GitHub se actualizan al abrir el tablero, manualmente y cada diez minutos mientras la pestaña permanece visible. Las evaluaciones se guardan únicamente en el navegador mediante `localStorage`; se recomienda exportar el JSON al terminar cada jornada.

La guía completa está en [`docs/PROGRESS_DASHBOARD.md`](docs/PROGRESS_DASHBOARD.md).

## Rutas de trabajo estudiantil

### Ruta 1 — Consolidación funcional

Para estudiantes con ejercicios aislados o flujos incompletos:

1. Elegir un proyecto principal.
2. Integrar HTML, JavaScript, eventos y DOM.
3. Agregar validaciones y persistencia.
4. Documentar el proyecto.
5. Entregar commits pequeños y descriptivos.

### Ruta 2 — Especialización CSS

Para el estudiante cuyo proyecto presenta el mayor nivel de integración:

1. Variables y arquitectura CSS.
2. Jerarquía visual.
3. Grid, Flexbox y responsive.
4. Estados hover, focus, error y disabled.
5. Accesibilidad y contraste.
6. Componentes reutilizables.

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

Para el tablero:

```text
http://localhost:8000/progress.html
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
├── progress.html
├── css/
│   ├── styles.css
│   └── progress.css
├── js/
│   ├── app.js
│   ├── cart-store.js
│   ├── core.js
│   ├── products.js
│   ├── receipt.js
│   ├── storage.js
│   ├── progress-core.js
│   └── progress.js
├── tests/
│   ├── core.test.js
│   └── progress-core.test.js
├── docs/
│   ├── GUION_CLASE.md
│   ├── SOURCE_REVIEW.md
│   ├── STUDENT_CHECKLIST.md
│   └── PROGRESS_DASHBOARD.md
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

El tablero docente no reemplaza la defensa oral ni la modificación en vivo. Los commits muestran evidencia de actividad, pero la competencia individual se valida cuando el estudiante explica y adapta su código.

## Uso educativo

Este proyecto no procesa pagos reales, no utiliza credenciales y no envía evaluaciones a servidores externos. La información del tablero se conserva únicamente en el navegador del docente mediante `localStorage`.
