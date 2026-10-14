# Clasificación y definición de proyectos — 14 de octubre de 2026

## Fuente y alcance verificado

Repositorio operativo: `juanperez238421-cpu/IJR---Seminario`, revisión base `38a05a2336b75c03d1a57eeb81a40c5fc61da89f`. Se identificó por el taller `t3/projects/student-workshops/rico-paramo`, las pruebas de proyectos específicos, la función `seminar-project-access` y el esquema `seminar_student_projects` de la base conectada `rlfxnjbqxbozjdzkbwlz`.

`Seminario_Goal_Period2` contiene guías anteriores de Rico y otros estudiantes; no es el módulo operativo actual. No se modificó.

La base contiene 12 planes: web 4, Python/datos 4, ciberseguridad 2, CAD/impresión 1 y robótica 1. Rico pertenece a la ruta Python/datos por organización del curso, pero **su producto es animación procedural**, no análisis estadístico ni una página web.

## Productos definidos

| Responsable | Ruta | Producto y alcance | Estado de implementación |
|---|---|---|---|
| Cortés | Web | ClubHub: directorio, categorías y miembros activos | Directorio compartido implementado; especialización de club definida |
| Jaramillo | Web | ReservaHub: usuarios, recursos y reservas sin solapamientos | Directorio compartido implementado; reservas definidas para unidad 6 |
| Velásquez | Web | SoporteHub: solicitantes, responsables y solicitudes con estados | Directorio compartido implementado; soporte definido para unidad 6 |
| Gómez | Web | GTA V Mod Showcase: conserva catálogo y compatibilidad, añade comunidad y favoritos | Directorio compartido implementado; integración temática definida |
| Rico | Python | Animación procedural portátil, configuración externa y lanzador manual | Referencia existente corregida, probada y empaquetada; prueba USB/visual manual pendiente |
| Mazo | Datos | Sports Data Lab: sesiones deportivas sintéticas, rendimiento y consistencia | Plan docente concreto; notebook por construir |
| González | Datos | Mobility Data Lab: recorridos sintéticos, mediana y variabilidad | Plan docente concreto; notebook por construir |
| Rincón | Datos | Gaming Data Lab: catálogo sintético, distribución y tendencias | Plan docente concreto; notebook por construir |
| Arango | Ciberseguridad | Laboratorio local de resiliencia y mitigación de ráfagas | Conserva su proyecto fijo y laboratorio existentes |
| Arbeláez | Ciberseguridad | Access Defense Lab: validación y permisos de dos roles en localhost | Plan concreto; laboratorio por construir |
| Chavarriaga | CAD/3D | DeskStand: soporte paramétrico para dispositivo, medidas y tolerancias | Plan concreto; modelo por construir |
| Rodríguez | Robótica | SafePark: barrera simulada, sensores, estados y parada segura | Plan concreto; simulación por construir |

Los temas nuevos son definiciones docentes realizadas con autorización del usuario; no se atribuyen a elecciones del estudiante. Los datasets sintéticos son alcance del prototipo, no evidencia observada del mundo real. No se inventaron resultados ni avances.

## Cambios aplicados en Supabase

Se actualizaron 10 planes con producto, objetivo, herramientas, playbook y ocho unidades de construcción. Las dos rutas fijas de Rico y Arango se conservaron. Las rutas antes generales pasaron a `fixed`: pueden empezar como asignaciones docentes concretas. `decision_status` permanece sin simular confirmación del estudiante.

No se cambiaron identificadores de estudiantes, slugs de proyectos, registros de progreso, decisiones históricas ni el sistema de acceso institucional. Se verificó que el progreso específico existente estaba vacío antes de las actualizaciones. Las páginas existentes no recibieron cambios de HTML, CSS ni JavaScript.

La migración aditiva `20261014160833_seminar_web_user_directory_v1` creó tres tablas nuevas protegidas con RLS. La cuenta de prueba indicada por el usuario fue habilitada para los cuatro directorios. No se alteraron contraseñas ni cuentas Auth.

## Evidencia de validación

- 12/12 pruebas seleccionadas de directorio, Rico y workspace: correctas.
- Prueba SQL real: administrador, lector, usuario no asignado, anónimo, aislamiento entre proyectos, contacto único/sintético, prohibición de autoascenso, reasignación y borrado. Fixtures revertidos.
- Asesores de Supabase: sin avisos asociados a los nuevos objetos; hay avisos en objetos anteriores fuera de este cambio.
- Suite general: 49/50 en Windows; falla anterior por ruta `/C:/...` en un test. El servidor señalado pasó `node --check` directamente.
- Rico: cuatro pruebas de configuración/portabilidad y tres pruebas de renderizado headless correctas; modo `--verify` ejecuta diez frames.

La referencia web cubre el núcleo de administración. Las reservas, solicitudes, favoritos y especializaciones siguen como incrementos de cada proyecto. La publicación del código nuevo requiere integrar la rama de GitHub; los planes y el esquema de Supabase ya están aplicados.

Guía ejecutable: `user-admin-reference/README.md`. Referencia oficial de acceso: https://supabase.com/docs/guides/database/postgres/row-level-security
