export const PROJECTS = {
  'cortes-web-definition': 'ClubHub · Directorio de miembros y categorías',
  'jaramillo-web-definition': 'ReservaHub · Directorio de usuarios de reservas',
  'velasquez-web-definition': 'SoporteHub · Directorio de solicitantes',
  'gomez-gta-v-mod-showcase': 'GTA V Mod Showcase · Comunidad del catálogo'
};
export function validateRecord(input) {
  const alias=String(input.alias||'').trim(), contact=String(input.contact||'').trim().toLowerCase(), category=String(input.category||'').trim();
  if(alias.length<2||alias.length>80)throw Error('El alias debe tener entre 2 y 80 caracteres.');
  if(!/^[^\s@]+@example\.test$/.test(contact)||contact.length>120)throw Error('Usa un contacto sintético @example.test.');
  if(!category||category.length>40)throw Error('La categoría debe tener entre 1 y 40 caracteres.');
  return {alias,contact,category};
}
export function filterRecords(rows, query, status) {
  const q=query.trim().toLocaleLowerCase();
  return rows.filter(r=>(status==='all'||r.status===status)&&`${r.alias} ${r.contact}`.toLocaleLowerCase().includes(q));
}
