# IJR — Seminario de Programación

Repositorio oficial del proyecto **Robledo Market Lab**, una aplicación web educativa construida con HTML, CSS y JavaScript puro para que los estudiantes puedan revisar una versión completa, funcional y documentada.

También incluye:

- un tablero docente de evaluación individual;
- un monitor automático de repositorios cada 12 horas;
- el registro completo de estudiantes de 11-A, 11-B y 11-C;
- una interfaz para tomar y exportar asistencia.

## Enlaces oficiales

- **Repositorio:** https://github.com/juanperez238421-cpu/IJR---Seminario
- **Proyecto de referencia:** https://juanperez238421-cpu.github.io/IJR---Seminario/
- **Monitoreo y asistencia:** https://juanperez238421-cpu.github.io/IJR---Seminario/monitor.html
- **Evaluación individual:** https://juanperez238421-cpu.github.io/IJR---Seminario/progress.html
- **Automatización:** https://github.com/juanperez238421-cpu/IJR---Seminario/actions/workflows/monitor-student-repositories.yml
- **Rama oficial:** `main`
- **Versión:** `1.2.0`

La rama `main` contiene la versión vigente. Los estudiantes deben estudiar la estructura, el flujo y la calidad esperada; no copiar literalmente la solución.

## Monitoreo automático cada 12 horas

El workflow `.github/workflows/monitor-student-repositories.yml` se ejecuta aproximadamente a:

- **07:00 de Colombia**;
- **19:00 de Colombia**.

También puede iniciarse manualmente desde la pestaña **Actions** de GitHub.

En cada ejecución:

1. lee el listado oficial `data/students.json`;
2. consulta el último commit de cada repositorio público vinculado;
3. compara el SHA con la ejecución anterior;
4. identifica líneas base, commits nuevos, repositorios sin cambios, pendientes y errores;
5. actualiza `data/monitor/latest.json`;
6. conserva los cambios detectados en `data/monitor/history.json`;
7. genera `data/monitor/summary.md`;
8. crea un commit automático en este repositorio.

El tablero `monitor.html` actualiza la visualización cada cinco minutos mientras permanece abierto, pero la consulta central y verificable de GitHub se realiza mediante Actions cada 12 horas.

### Repositorios actualmente vinculados

| Estudiante | Grupo | Repositorio | Estado del vínculo |
|---|---|---|---|
| Juan Pablo Arango Giraldo | 11-A | `jp0705git/SeminarioProgramacion2` | Provisional; confirmar en entrevista |
| Jerónimo Rodríguez Peña | 11-A | `jrod917/Carrito` | Provisional; confirmar en entrevista |
| Pedro Pablo Arbeláez Escobar | 11-B | `Pedropae07/practice_seminario` | Provisional; confirmar en entrevista |
| Pablo Jaramillo Palacio | 11-B | `pablitojarita2008-oss/pablitoSeminario` | Confirmado por el contenido del repositorio |

Los demás registros ya existen en la aplicación, pero requieren que el docente agregue `usuario/repositorio` en `data/students.json`:

- Jerónimo Mazo López;
- Samuel Chavarriaga Avendaño;
- Alejandro Rico Páramo;
- Tomás González Giraldo;
- Alejandro Rincón Torres.

## Asistencia

`monitor.html` contiene el listado completo suministrado para el **28 de julio de 2026**:

### 11-A

1. ARANGO GIRALDO JUAN PABLO
2. MAZO LOPEZ JERONIMO
3. RODRIGUEZ PEÑA JERONIMO

### 11-B

1. ARBELAEZ ESCOBAR PEDRO PABLO
2. CHAVARRIAGA AVENDAÑO SAMUEL
3. JARAMILLO PALACIO PABLO
4. RICO PARAMO ALEJANDRO

### 11-C

1. GONZALEZ GIRALDO TOMAS
2. RINCON TORRES ALEJANDRO

La interfaz permite registrar:

- presente;
- llegó tarde;
- ausente;
- excusa;
- nota breve.

La asistencia se guarda en `localStorage` del navegador. Al terminar la clase debe utilizarse **Exportar asistencia** para descargar un JSON verificable. El archivo inicial del 28 de julio se encuentra en `data/attendance/2026-07-28.json`.

## Operación recomendada en clase

1. Abrir `monitor.html`.
2. Verificar la fecha y hora del último monitoreo automático.
3. Seleccionar el grupo y tomar asistencia.
4. Exportar la asistencia al finalizar.
5. Priorizar estudiantes con la etiqueta **Commit nuevo**.
6. Abrir el repositorio y pedir al estudiante ejecutar su proyecto.
7. Pedir una explicación del recorrido entrada → validación → procesamiento → DOM → persistencia.
8. Solicitar una modificación breve en vivo.
9. Abrir `progress.html` y registrar calificación, metas y observaciones.
10. Confirmar los vínculos provisionales o agregar los repositorios pendientes.

## Proyecto de referencia: Robledo Market Lab

Incluye:

- HTML semántico y accesible;
- CSS responsive con catálogo y panel de compra;
- catálogo generado desde objetos JavaScript;
- búsqueda y filtros por categoría;
- carrito con cantidades y eliminación de productos;
- estado centralizado mediante `CartStore`;
- validación de nombre, correo, dirección y confirmación;
- cupón de demostración `ROBLEDO10`;
- cálculo de subtotal, descuento, domicilio y total;
- persistencia con `localStorage`;
- comprobante imprimible;
- pruebas automáticas con Node.js.

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

## Evaluación individual

`progress.html` permite:

- registrar estudiantes, grupos, repositorios y proyectos;
- consultar el último commit público desde el navegador;
- detectar commits pendientes de revisión;
- asignar una ruta de consolidación o especialización CSS;
- marcar diez metas verificables;
- aplicar una rúbrica ponderada en escala de 0,0 a 5,0;
- registrar la siguiente meta y observaciones;
- marcar el SHA revisado;
- exportar e importar el seguimiento en JSON.

La nota utiliza:

| Criterio | Peso |
|---|---:|
| Estado funcional del proyecto | 30 % |
| Competencias visibles en el código | 25 % |
| Explicación individual | 20 % |
| Modificación en vivo | 15 % |
| Git y documentación | 10 % |

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

Páginas:

```text
http://localhost:8000/
http://localhost:8000/monitor.html
http://localhost:8000/progress.html
```

## Ejecutar pruebas y monitoreo manual

Requiere Node.js 18 o superior:

```bash
npm test
npm run monitor
```

`npm run monitor` actualiza los archivos de `data/monitor/`. Desde un equipo local sin `GITHUB_TOKEN`, las consultas públicas tienen un límite menor; GitHub Actions usa automáticamente el token del repositorio.

## Estructura principal

```text
IJR---Seminario/
├── index.html
├── receipt.html
├── monitor.html
├── progress.html
├── css/
│   ├── styles.css
│   ├── monitor.css
│   └── progress.css
├── js/
│   ├── app.js
│   ├── cart-store.js
│   ├── core.js
│   ├── products.js
│   ├── receipt.js
│   ├── storage.js
│   ├── monitor.js
│   ├── progress-core.js
│   └── progress.js
├── data/
│   ├── students.json
│   ├── attendance/
│   │   └── 2026-07-28.json
│   └── monitor/
│       ├── latest.json
│       ├── history.json
│       └── summary.md
├── scripts/
│   └── monitor-students.mjs
├── tests/
│   ├── core.test.js
│   └── progress-core.test.js
├── docs/
├── .github/workflows/
│   ├── tests.yml
│   └── monitor-student-repositories.yml
└── package.json
```

## Nota pedagógica

Los commits muestran evidencia de actividad, pero no prueban por sí solos la competencia individual. La calificación debe confirmar que el estudiante puede:

- ejecutar su proyecto;
- explicar una función;
- identificar el recorrido de los datos;
- corregir o modificar una parte en vivo;
- reconocer qué trabajo realizó personalmente.

## Uso educativo

Este proyecto no procesa pagos reales ni envía evaluaciones o asistencia a servidores externos. La consulta de commits usa repositorios públicos. Las notas y la asistencia se conservan localmente hasta que el docente las exporta.
