# Tablero de seguimiento de estudiantes

## Propósito

`progress.html` permite al docente revisar el avance de los proyectos de grado 11, consultar el último commit público de cada repositorio y registrar una evaluación individual.

El tablero separa dos rutas:

1. **Consolidación funcional:** para estudiantes que aún deben integrar HTML, JavaScript, DOM, validaciones, persistencia y documentación en un solo proyecto.
2. **Especialización CSS:** para el estudiante cuyo proyecto ya presenta el mayor nivel de integración funcional y puede concentrarse en responsive, accesibilidad, estados visuales y componentes reutilizables.

## Qué se consulta en GitHub

La página usa la API pública de GitHub para recuperar:

- SHA del último commit;
- mensaje del commit;
- fecha;
- autor;
- enlace al commit.

La consulta ocurre al abrir la página, al pulsar **Sincronizar GitHub** y cada diez minutos mientras la pestaña está visible.

> GitHub limita las consultas públicas sin autenticación. Si aparece un aviso de límite temporal, se conservan los últimos datos sincronizados y se puede intentar más tarde.

## Qué se guarda localmente

La evaluación no se publica en GitHub. Se conserva en el navegador mediante `localStorage`:

- criterios de evaluación;
- metas completadas;
- siguiente meta;
- observaciones;
- último SHA marcado como revisado;
- estudiantes agregados manualmente.

Use **Exportar JSON** después de cada sesión para crear un respaldo. El archivo puede importarse en otro computador.

## Rúbrica

| Criterio | Peso |
|---|---:|
| Estado funcional del proyecto | 30 % |
| Competencias visibles en el código | 25 % |
| Explicación individual | 20 % |
| Modificación en vivo | 15 % |
| Git y documentación | 10 % |

La nota se calcula en escala de 0,0 a 5,0 únicamente cuando los cinco criterios tienen valor.

## Metas verificables

Cada estudiante se registra frente a diez evidencias:

1. HTML visible y semántico.
2. CSS conectado y organizado.
3. JavaScript conectado correctamente.
4. Eventos vinculados a la interfaz.
5. Renderizado con DOM.
6. Validaciones reales.
7. Funciones de procesamiento reutilizables.
8. Persistencia o navegación con `localStorage`.
9. README con instrucciones.
10. Commits descriptivos.

## Uso durante la entrevista

1. Sincronizar GitHub.
2. Seleccionar al estudiante.
3. Abrir el repositorio y ejecutar el proyecto.
4. Pedir una explicación del flujo de datos.
5. Solicitar una modificación en vivo.
6. Registrar rúbrica y metas.
7. Escribir una siguiente meta concreta.
8. Marcar el commit como revisado.
9. Exportar el JSON al terminar la jornada.

## Alcance de “tiempo real”

El repositorio es una aplicación estática publicada en GitHub Pages. No recibe webhooks ni escribe calificaciones en un servidor. El seguimiento de commits es **casi en tiempo real** mientras la página está abierta; las notas permanecen locales hasta exportarlas.
