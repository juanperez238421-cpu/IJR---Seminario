-- Seminar 11: individualized student-facing project playbooks.
-- Mirrors the production migration seminar_project_playbook_content_v9.

alter table public.seminar_student_projects
  add column if not exists content_sections jsonb not null default '[]'::jsonb;

comment on column public.seminar_student_projects.content_sections is
  'Student-facing project playbook sections. Structured teacher content shown only through the constrained Seminar project access flow.';

do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'seminar_student_projects_content_sections_check'
      and conrelid = 'public.seminar_student_projects'::regclass
  ) then
    alter table public.seminar_student_projects
      add constraint seminar_student_projects_content_sections_check
      check (
        jsonb_typeof(content_sections) = 'array'
        and jsonb_array_length(content_sections) <= 12
      );
  end if;
end
$$;

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"START HERE","title":"1. Tu reto: proteger un servicio local","body":"Construye una aplicación web que funcione únicamente en tu equipo o sandbox local. Primero mide su comportamiento normal; después añade controles defensivos para limitar ráfagas de solicitudes y registrar lo que ocurre.","items":["Define el activo protegido: endpoint, datos y comportamiento esperado.","Declara el alcance autorizado: localhost / 127.0.0.1. No se prueban servicios externos.","Elige métricas: solicitudes por segundo, latencia, respuestas permitidas y bloqueadas."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional","body":"El MVP debe demostrar defensa antes y después de aplicar controles.","items":["Servicio local con al menos un endpoint de prueba.","Simulador de tráfico acotado por tasa y duración, apuntando solo a localhost.","Rate limiter con respuesta clara cuando se supera el límite.","Log de eventos y una vista sencilla de métricas."]},
  {"kicker":"BUILD","title":"3. Primer bloque de construcción","body":"Organiza el proyecto para poder probar cada componente de forma independiente.","items":["Separa servicio, simulador, configuración, logs y documentación.","Registra una línea base con tráfico normal antes de implementar la defensa.","Implementa límites configurables y un período de cooldown/backoff.","Documenta el flujo Client → App → RateLimiter → Response → AuditLog."]},
  {"kicker":"QA / SAFETY","title":"4. Pruebas obligatorias","body":"Las pruebas deben validar resiliencia y seguridad sin convertirse en una herramienta de ataque.","items":["Tráfico normal: no debe bloquearse indebidamente.","Ráfaga controlada: debe activar el límite y quedar registrada.","Entrada inválida: debe producir una respuesta segura y predecible.","El simulador debe rechazar hosts externos o configuraciones fuera del sandbox.","Los logs no deben guardar contraseñas, tokens ni secretos."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"Tu conclusión debe apoyarse en datos de la prueba, no solo en una demostración visual.","items":["Tabla activo–amenaza–control–evidencia.","UML o diagrama de flujo de solicitudes.","Comparación de métricas antes/después.","Matriz de pruebas con resultado esperado y observado.","Repositorio y demostración local en vivo."]}
]
$json$::jsonb
where project_slug = 'arango-web-resilience-defense-lab';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"START HERE","title":"1. Convierte el tema GTA V en un producto de información","body":"El proyecto no es una colección de archivos para descargar: es una aplicación web que organiza información estructurada sobre mods, requisitos, dependencias y compatibilidad.","items":["Define el usuario: jugador que quiere saber qué mod puede usar y con qué versión.","Selecciona categorías del catálogo y una regla clara para incluir cada registro.","Usa enlaces de referencia; no redistribuyas cracks, ejecutables ni contenido sin permiso."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional","body":"El MVP debe permitir descubrir un mod y decidir si es compatible.","items":["Catálogo con al menos un conjunto representativo de registros estructurados.","Campos mínimos: nombre, categoría, versión, requisitos, dependencias y compatibilidad.","Búsqueda por texto y filtros combinables.","Vista de detalle y favoritos persistentes."]},
  {"kicker":"BUILD","title":"3. Modelo de datos y lógica","body":"La calidad del proyecto dependerá más del modelo y de la lógica de compatibilidad que de la decoración.","items":["Diseña un esquema JSON para Mod, Category, Dependency y CompatibilityRule.","Genera tarjetas y detalles desde datos, no copiando HTML manual para cada mod.","Implementa filtros como funciones reutilizables.","Explica por qué una combinación versión/dependencia se considera compatible o no."]},
  {"kicker":"QA","title":"4. Casos que debes probar","body":"La aplicación debe comportarse bien cuando la información sea incompleta o no haya coincidencias.","items":["Búsqueda sin resultados y filtros incompatibles entre sí.","Registro con imagen, dependencia o versión faltante.","Versión desconocida o requisito no definido.","Favoritos después de recargar la página.","Uso en móvil y navegación con teclado."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"Debes poder justificar tanto el diseño visual como el modelo de información.","items":["Esquema de datos/UML y wireframe.","Repositorio y despliegue público.","Ejemplos reales del motor de búsqueda/filtros/compatibilidad.","Matriz de QA y correcciones realizadas.","Demostración completa desde catálogo hasta detalle y favorito."]}
]
$json$::jsonb
where project_slug = 'gomez-gta-v-mod-showcase';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"START HERE","title":"1. Diseña una experiencia visual portátil","body":"El objetivo es crear una pieza visual procedural en Python que pueda ejecutarse offline desde una carpeta portátil o memoria USB mediante un lanzador visible y controlado.","items":["Decide si será una animación lineal o una experiencia interactiva.","Define estilo, duración/resolución y tres efectos visuales principales.","Elige Pygame o Manim según el tipo de experiencia y justifica la decisión."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional","body":"El MVP debe funcionar sin internet y sin depender de rutas absolutas del computador de desarrollo.","items":["Al menos tres escenas/efectos procedurales reutilizables.","Archivo de configuración o parámetros editables.","Carga de recursos mediante rutas relativas.","Lanzador manual visible y README de ejecución.","Build empaquetado o entorno Python portátil claramente documentado."]},
  {"kicker":"BUILD","title":"3. Arquitectura sugerida","body":"Separa la lógica visual de la configuración y del mecanismo de lanzamiento.","items":["Modela responsabilidades como Scene, Effect, Timeline/Controller, Config y Launcher.","Haz que cada efecto reciba parámetros en lugar de valores quemados.","Controla semilla, tiempo o frame rate cuando la reproducibilidad sea importante.","Incluye fallback claro si falta un asset."]},
  {"kicker":"QA","title":"4. Pruebas de portabilidad","body":"No basta con que funcione en la carpeta original del proyecto.","items":["Ejecuta desde una ruta diferente y, si es posible, desde una unidad removible.","Desconecta internet y repite la prueba.","Prueba asset faltante o configuración inválida.","Comprueba que el lanzador no use autostart, tareas ocultas ni cambios permanentes del sistema.","Verifica rendimiento y salida limpia al cerrar."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"La defensa debe demostrar arquitectura, calidad visual y portabilidad real.","items":["Storyboard y UML/diagrama de escena.","Código fuente y carpeta/build portátil.","Matriz de pruebas offline y de rutas.","Capturas o video del resultado.","Cambio en vivo de un parámetro visual y nueva ejecución."]}
]
$json$::jsonb
where project_slug = 'rico-portable-python-visual-show';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"DEFINE","title":"1. Empieza por una pregunta, no por una librería","body":"Tu proyecto debe responder una pregunta concreta usando datos. Antes de programar, define qué quieres averiguar, qué dataset lo permite y qué resultado sería útil.","items":["Escribe una pregunta que pueda responderse con variables observables.","Identifica fuente, licencia, fecha y alcance del dataset.","Define variable principal, unidades y población representada.","Decide si el producto final será notebook, dashboard, informe o combinación."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional de analista","body":"El MVP es un análisis reproducible de principio a fin.","items":["Carga del dataset desde una ruta o fuente documentada.","Diccionario de datos.","Limpieza justificada de tipos, faltantes, duplicados e inconsistencias.","Estadística descriptiva pertinente.","Al menos tres visualizaciones que ayuden a responder la pregunta.","Conclusión y limitaciones."]},
  {"kicker":"BUILD","title":"3. Estructura tu notebook como una investigación","body":"Cada bloque de código debe tener una razón y cada gráfica una interpretación.","items":["Importación y validación inicial.","Limpieza en pasos reproducibles, evitando editar datos manualmente.","EDA: distribución, grupos y relaciones relevantes.","Visualizaciones con títulos, unidades y etiquetas.","Modelo o ML solo si aporta algo que el análisis descriptivo no resuelve."]},
  {"kicker":"QA","title":"4. Control de calidad del análisis","body":"Un resultado que no puede reproducirse o que interpreta mal los datos no es un resultado válido.","items":["Reinicia el entorno y ejecuta todo desde cero.","Verifica tipos, unidades y valores faltantes después de limpiar.","Evita escalas/gráficas que distorsionen la comparación.","Distingue correlación de causalidad.","Comprueba que cada conclusión tenga una tabla, estadística o gráfica que la respalde."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"Tu presentación debe contar una historia de datos completa y verificable.","items":["Pregunta y fuente del dataset.","Notebook reproducible y diccionario de datos.","Evidencia antes/después de la limpieza.","Tres o más visualizaciones justificadas.","Hallazgos, limitaciones y una operación en vivo sobre los datos."]}
]
$json$::jsonb
where project_mode = 'guided_definition' and track_slug = 'data-science';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"DEFINE","title":"1. Define usuario, problema y acción principal","body":"Antes de elegir colores o framework, concreta quién usará la aplicación, qué problema resolverá y qué podrá hacer el usuario que hoy no puede hacer con una página estática.","items":["Describe un usuario realista y una necesidad concreta.","Prioriza tres funciones indispensables del MVP.","Define qué datos necesita la aplicación y de dónde provienen.","Escribe un criterio verificable de éxito."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional web","body":"El MVP debe incluir un flujo de usuario completo y persistencia o consumo de datos cuando el proyecto lo necesite.","items":["Interfaz responsiva con navegación clara.","Una acción principal completa: crear, buscar, reservar, registrar, comparar, organizar u otra equivalente.","Datos en JSON/API/localStorage o backend justificado.","Estados vacíos, validación y mensajes de error útiles."]},
  {"kicker":"BUILD","title":"3. Construye por capas","body":"Separa estructura, presentación, lógica y datos para que el proyecto pueda crecer sin volverse frágil.","items":["Wireframe e información de pantallas antes del código final.","HTML semántico y CSS responsivo.","JavaScript organizado en funciones con responsabilidades claras.","Modelo de datos explícito para las entidades del proyecto.","Persistencia o integración de datos probada desde el flujo principal."]},
  {"kicker":"QA","title":"4. Casos que debes probar","body":"Prueba el producto como si fueras un usuario nuevo y como si los datos no fueran perfectos.","items":["Primera visita sin datos guardados.","Datos inválidos, campos vacíos o búsqueda sin resultados.","Recarga de página y persistencia del estado cuando aplique.","Diseño en móvil y pantalla de escritorio.","Navegación por teclado y foco visible en controles."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"Debes poder explicar por qué construiste cada parte y demostrar que funciona.","items":["User story/backlog priorizado.","Wireframe y UML/modelo de datos.","Repositorio GitHub y URL desplegada.","Matriz de pruebas con fallos encontrados y correcciones.","Demo en vivo del flujo principal y de una condición de error."]}
]
$json$::jsonb
where project_mode = 'guided_definition' and track_slug = 'web';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"DEFINE","title":"1. Define la misión del robot","body":"Tu proyecto empieza por una misión concreta y medible. Describe el entorno, qué debe percibir el sistema, qué decisión toma y qué salida o movimiento produce.","items":["Define misión, entorno y usuario.","Identifica entradas/sensores y salidas/actuadores.","Escribe estados del sistema y condiciones de transición.","Incluye un estado seguro ante fallo o pérdida de señal."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional","body":"El MVP debe cerrar el ciclo Sensor → Controller → Actuator, incluso si al principio usas simulación.","items":["Lectura de al menos una entrada real o simulada.","Máquina de estados o lógica de control explícita.","Una salida observable: motor, LED, servo, display o simulación.","Registro serial/log de estado y una condición de seguridad."]},
  {"kicker":"BUILD","title":"3. Del diagrama al prototipo","body":"Valida primero la lógica y luego integra hardware.","items":["Diagrama de bloques y tabla de estados/transiciones.","Prueba de sensor o señal de entrada de forma aislada.","Prueba de actuador o salida de forma aislada.","Integración controlada con umbrales configurables.","Documentación de pines, alimentación y dependencias."]},
  {"kicker":"QA / SAFETY","title":"4. Pruebas obligatorias","body":"El robot debe comportarse de manera predecible en límites y fallos.","items":["Arranque y apagado seguro.","Sensor desconectado, lectura fuera de rango o dato imposible.","Valores exactamente en los límites de decisión.","Bloqueo/timeout de una acción.","Transición al estado seguro sin comportamiento inesperado."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"La defensa debe mostrar que el comportamiento fue diseñado y probado, no improvisado.","items":["Diagrama de bloques y máquina de estados.","Esquema de conexiones o simulación.","Repositorio con código comentado por responsabilidades.","Matriz de escenarios y resultados.","Demostración en vivo o video del prototipo."]}
]
$json$::jsonb
where project_mode = 'guided_definition' and track_slug = 'robotics';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"DEFINE / SAFETY","title":"1. Define el activo y la defensa","body":"El proyecto debe ser defensivo y estar limitado a sistemas propios, laboratorios locales o datos sintéticos. Elige un activo, una amenaza concreta y el control que vas a implementar.","items":["Declara por escrito el alcance autorizado.","Elige un activo: login local, formulario, conjunto de logs o servicio sandbox.","Describe amenaza, impacto y control defensivo.","No se escanean, atacan ni prueban servicios de terceros."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional defensivo","body":"El MVP debe demostrar un control de seguridad y producir evidencia observable.","items":["Un escenario local/sintético reproducible.","Control defensivo: validación, rate limiting, autenticación endurecida o detección basada en reglas.","Registro de eventos sin secretos.","Pruebas de caso permitido y caso bloqueado/alertado."]},
  {"kicker":"BUILD","title":"3. Diseña la evidencia antes de programar","body":"Cada control debe estar conectado con una amenaza y con una forma de medir si funcionó.","items":["Crea tabla Amenaza → Control → Evidencia.","Dibuja arquitectura y puntos donde se valida/registra.","Usa datos sintéticos o entradas propias para las pruebas.","Mantén límites, umbrales y reglas en configuración cuando sea posible."]},
  {"kicker":"QA / SAFETY","title":"4. Pruebas obligatorias","body":"Las pruebas deben validar robustez sin crear capacidad ofensiva contra terceros.","items":["Caso válido y caso inválido/malformado.","Caso exactamente en el límite del control.","Caso repetido para comprobar logging y rate/threshold.","Logs sin contraseñas, tokens o información sensible.","Confirmación de que el entorno no acepta objetivos externos."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"Debes poder explicar la relación entre riesgo, implementación y resultado.","items":["Declaración de alcance autorizado.","Threat model sencillo y arquitectura.","Código del control defensivo.","Evidencia antes/después o permitido/bloqueado.","Matriz de pruebas y limitaciones conocidas."]}
]
$json$::jsonb
where project_mode = 'guided_definition' and track_slug = 'cybersecurity';

update public.seminar_student_projects
set content_sections = $json$
[
  {"kicker":"DEFINE","title":"1. Parte de un problema físico real","body":"No diseñes una pieza decorativa al azar. Define quién la usará, qué debe sostener/unir/organizar, qué dimensiones condicionan el diseño y cómo sabrás si encaja.","items":["Describe función, usuario y objeto con el que interactúa.","Toma medidas críticas y registra unidades.","Define restricciones: tamaño, orientación, tolerancia y material.","Elige qué dimensiones serán parámetros editables."]},
  {"kicker":"MVP","title":"2. Producto mínimo funcional 3D","body":"El MVP es un modelo paramétrico verificable y listo para fabricar.","items":["Croquis o esquema con cotas clave.","Modelo CAD paramétrico con variables identificables.","Comprobación de encajes y colisiones.","Exportación STL.","Configuración de slicing y al menos una iteración documentada."]},
  {"kicker":"BUILD","title":"3. Flujo de trabajo recomendado","body":"Avanza de medidas y restricciones hacia geometría, no al revés.","items":["Tabla de parámetros y tolerancias.","Geometría base y restricciones antes de detalles.","Prueba dimensional digital o con plantilla.","Revisión de orientación de impresión y soportes.","Iteración después de detectar un problema real de ajuste o fabricación."]},
  {"kicker":"QA","title":"4. Control de calidad antes de imprimir","body":"Un STL válido no garantiza una pieza útil.","items":["Espesores mínimos y zonas frágiles.","Tolerancia de encaje entre piezas.","Geometría cerrada y sin errores evidentes.","Orientación, soportes y tiempo/material estimado.","Comparación entre medida nominal y medida esperada del prototipo."]},
  {"kicker":"EVIDENCE","title":"5. Evidencia para la defensa final","body":"Tu defensa debe mostrar el razonamiento que conecta necesidad, parámetros y objeto final.","items":["Croquis con medidas y tabla de parámetros.","Capturas del historial/modelo CAD.","STL y captura del slicer.","Antes/después de una iteración.","Foto/video del prototipo si se imprime y reflexión sobre ajuste."]}
]
$json$::jsonb
where project_mode = 'guided_definition' and track_slug = '3d-programming';

update public.seminar_student_projects
set updated_at = clock_timestamp()
where jsonb_array_length(content_sections) > 0;
