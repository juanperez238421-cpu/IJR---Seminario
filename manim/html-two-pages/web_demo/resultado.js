// 1. Leer la cadena de consulta que aparece después del signo ?
const params = new URLSearchParams(window.location.search);

// 2. Recuperar cada valor usando el mismo nombre definido en el formulario
const nombreRecibido = params.get("nombre");
const edadTexto = params.get("edad");
const cursoRecibido = params.get("curso");
const temaRecibido = params.get("tema");

// 3. Limpiar y normalizar texto
const nombre = toTitleCase((nombreRecibido || "Estudiante").trim());
const curso = (cursoRecibido || "Sin curso").trim();
const tema = (temaRecibido || "No indicado").trim();

// 4. Convertir y validar la edad
const edad = Number.parseInt(edadTexto, 10);
const edadValida = Number.isFinite(edad) && edad >= 5 && edad <= 100;
const proximaEdad = edadValida ? edad + 1 : null;
const categoria = !edadValida
  ? "Edad no válida"
  : edad >= 18
    ? "Mayor de edad"
    : "Menor de edad";

// 5. Escribir los resultados dentro de los elementos preparados en HTML
document.querySelector("#saludo").textContent = `Hola, ${nombre}`;
document.querySelector("#resumen").textContent =
  "La segunda página leyó, validó y transformó los datos recibidos.";
document.querySelector("#curso").textContent = curso;
document.querySelector("#edad").textContent = edadValida ? `${edad} años` : "—";
document.querySelector("#proxima-edad").textContent = edadValida
  ? `${proximaEdad} años`
  : "—";
document.querySelector("#categoria").textContent = categoria;

const mensaje = document.querySelector("#mensaje");
mensaje.textContent = edadValida
  ? `Tema favorito: ${tema}. El próximo año tendrás ${proximaEdad} años.`
  : `Tema favorito: ${tema}. Regresa al formulario y escribe una edad entre 5 y 100.`;
mensaje.classList.toggle("error", !edadValida);

function toTitleCase(value) {
  return value
    .toLocaleLowerCase("es")
    .replace(/(^|\s)\p{L}/gu, (letter) => letter.toLocaleUpperCase("es"));
}
