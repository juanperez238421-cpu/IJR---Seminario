# Administración de usuarios: referencia ejecutable

Esta aplicación implementa el núcleo de los cuatro proyectos web de Seminario 11: directorio persistente, consulta, búsqueda, edición, archivo/restauración, permisos por proyecto y auditoría. No modifica las páginas existentes.

## Ejecutar

Desde la raíz del repositorio:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Abrir uno de estos enlaces:

- `http://127.0.0.1:8765/t3/projects/user-admin-reference/index.html?project=cortes-web-definition`
- `http://127.0.0.1:8765/t3/projects/user-admin-reference/index.html?project=jaramillo-web-definition`
- `http://127.0.0.1:8765/t3/projects/user-admin-reference/index.html?project=velasquez-web-definition`
- `http://127.0.0.1:8765/t3/projects/user-admin-reference/index.html?project=gomez-gta-v-mod-showcase`

La cuenta de prueba indicada por el docente ya tiene permisos de administrador en los cuatro proyectos. Iniciar sesión con su contraseña existente. No se cambió su contraseña, su identidad ni sus otros permisos.

La sesión se conserva solo en memoria; una recarga requiere iniciar sesión de nuevo. Los registros permanecen en PostgreSQL. La búsqueda filtra registros cargados; se cargan 100 por página mediante «Cargar más».

## Modelo y permisos

- `seminar_web_memberships`: rol `admin` o `viewer` por proyecto y cuenta Auth. Solo el servidor/docente modifica membresías.
- `seminar_web_directory`: usuarios del producto con alias, contacto sintético `@example.test`, categoría y estado. No son cuentas Auth ni estudiantes institucionales.
- `seminar_web_directory_events`: historial de creación/cambio, sin guardar contraseñas, tokens ni campos personales.
- Administrador: crear, consultar, editar, archivar y restaurar. Lector: consultar. Anónimo/sin membresía: sin acceso.
- No hay borrado físico ni autoasignación de permisos desde el navegador.

La base aplicó `seminar_web_user_directory_v1`, versión `20261014160833`, el 14 de octubre de 2026. **No volver a ejecutar `schema.sql` en esta base.** Es una referencia del esquema aplicado. `plans.sql` conserva las actualizaciones de contenido realizadas, con comprobaciones del estado previo; no es un script que se deba ejecutar de nuevo.

Para otra cuenta de prueba existente, el docente puede ejecutar desde SQL Editor:

```sql
insert into public.seminar_web_memberships(project_slug,user_id,role)
select 'cortes-web-definition', id, 'viewer'
from auth.users where lower(email) = lower('CUENTA_DE_PRUEBA')
on conflict(project_slug,user_id) do update set role=excluded.role;
```

Usar exclusivamente cuentas de prueba verificadas. No incluir claves secretas en `config.js`; solo URL y clave publicable.

## Trabajo específico por producto

La referencia construye el **directorio compartido**, no los cuatro productos completos:

- ClubHub: ampliar categorías y consulta de miembros.
- ReservaHub: recursos, reservas y prevención transaccional de solapamientos.
- SoporteHub: solicitudes, responsables y transiciones de estado.
- GTA V: conservar catálogo, filtros y compatibilidad; añadir favoritos por usuario.

Esas ampliaciones están definidas en la unidad 6 de cada plan. Los planes no marcan unidades como terminadas ni simulan decisiones del estudiante.

## Validación

```powershell
node --test tests/web-user-directory.test.js tests/rico-project-pages.test.js tests/specific-project-workspace.test.js
```

Las 12 pruebas seleccionadas pasaron. `verify-rls.sql` comprobó la base real con fixtures dentro de una transacción revertida: administración, auditoría, lector, aislamiento, acceso anónimo, contacto único, contacto sintético, impedimento de autoascenso, reasignación de proyecto y borrado. Se ejecutó sobre el directorio vacío antes de habilitar la cuenta; para repetirlo, usar una base de pruebas vacía.

La suite completa tuvo 49/50 pruebas correctas en Windows: un test anterior construye una ruta `/C:/...` no válida. La validación directa `node --check t3/tracks/cybersecurity/lab/app/server.js` pasó. No se alteró esa página ni su servidor.

Los asesores de Supabase no señalaron los nuevos objetos. La base compartida conserva avisos de objetos anteriores; este trabajo no constituye una auditoría global de toda la plataforma. Referencia: https://supabase.com/docs/guides/database/postgres/row-level-security
