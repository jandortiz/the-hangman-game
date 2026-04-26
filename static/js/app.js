// Acceso a las pantallas.
const startScreen = document.getElementById("screen-start");
const gameScreen = document.getElementById("screen-game");
const resultScreen = document.getElementById("screen-result");


// Acceso a los botones.
const buttonStart = document.getElementById("start-btn");
const buttonPlayAgain = document.getElementById("play-again-btn");
const buttonKeyboards = document.getElementById("keyboard");
// const toggleButton = document.getElementById("theme-toggle");
const toggleButtons = document.querySelectorAll(".theme-btn");


for (changeButton of toggleButtons) {
	changeButton.addEventListener("click", toggleTheme);
}

// Acceso a los display.
const displayWord = document.getElementById("word-display");
const displayAttempts = document.getElementById("attempts-display");


// Accesos variados.
const textHint = document.getElementById("hint-text");
const lettersWrong = document.getElementById("wrong-letters");
const hangmanContainer = document.getElementById("hangman-container");

// Acceso a los resultados.
const resultMessage = document.getElementById("result-message");
const resultWord = document.getElementById("result-word");
const resultHangman = document.getElementById("result-hangman");

// Variable para guardar el estado de la partida.
let gameId = null;



// Event listener al botón para comenzar el juego.
buttonStart.addEventListener("click", startGame);




renderHangman(0, document.getElementById("start-hangman"));





async function startGame() {
	resultScreen.style.display = "none";
	

	const response = await fetch("/api/game/new", {method: "POST"});
	const data = await response.json();
	console.log(data);

	gameId = data.game_id;
	console.log(gameId);

	startScreen.style.display = "none";
	gameScreen.style.display = "flex";
	renderHangman(0, hangmanContainer);

	textHint.textContent = data.hint;
	displayAttempts.textContent = `${data.attempts_remaining} attempts`;
	


	updateWordDisplay(data.masked_word, displayWord);

	renderKeyboard();
}




buttonKeyboards.addEventListener("click", handleGuess);




async function handleGuess(e){
	const clickerButton = e.target;

	if (!clickerButton.dataset.key) return

	const letter = clickerButton.dataset.key;

	const response = await fetch(`/api/game/${gameId}/guess`, {
		method: "POST",
		headers: {"Content-Type": "application/json"},
		body: JSON.stringify({letter: letter})
	});

	const data = await response.json();

	updateWordDisplay(data.masked_word, displayWord);
	displayAttempts.textContent = `${data.attempts_remaining} attempts`;
	renderHangman(6 - data.attempts_remaining, hangmanContainer);

	if (data.correct) {
		clickerButton.classList.add("correct");
		clickerButton.disabled = true;
		console.log("CORRECTO");
	} else {
		clickerButton.classList.add("wrong");
		clickerButton.disabled = true;
		console.log("INCORRECTO");

	}

	if (data.status != "playing") {
		showResult(data);
	}
}


buttonPlayAgain.addEventListener("click", startGame);


// FUNCIONES UTILITARIAS.

function renderKeyboard() {
	buttonKeyboards.innerHTML = "";
	const rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];
	
	for (const keyboardRow of rows) {
		const rowDiv = document.createElement("div");
		rowDiv.classList.add("keyboard-row");
		
		for (const keyboardLetter of keyboardRow) {
			const buttonEl = document.createElement("button");
			
			buttonEl.textContent = keyboardLetter;
			buttonEl.setAttribute("data-key", keyboardLetter.toLowerCase());
			buttonEl.classList.add("key");
			
			rowDiv.appendChild(buttonEl);
		}
		buttonKeyboards.appendChild(rowDiv);
	}
}



function updateWordDisplay(maskedWord, displayContainer){
	displayContainer.innerHTML = "";

	for (const caracter of maskedWord) {
		if (caracter != " "){
			const span = document.createElement("span");
			span.textContent = caracter;
			displayContainer.appendChild(span);
			if (caracter === "_") {
				span.textContent = "";
			}
		}

		
	}
}


function showResult(data){
	gameScreen.style.display = "none";
	resultScreen.style.display = "flex";


	if (data.status === "won"){
		resultMessage.textContent = "YOU WON!!!";
		buttonPlayAgain.style.background = "var(--accent)";
		resultMessage.style.color = "var(--accent)";
		renderHangman(0, resultHangman);

	} else {
		resultMessage.textContent = "YOU LOST!!!";
		buttonPlayAgain.style.background = "var(--error)";
		resultMessage.style.color = "var(--error)";
		renderHangman(6, resultHangman);
	}

	updateWordDisplay(data.word, resultWord);

}


// ── Función para dibujar la figura del ahorcado ──────────────
// Traduce el diseño React original a vanilla JS.
// Recibe el número de errores (0-6) y un contenedor DOM donde insertar el SVG.
function renderHangman(mistakes, container) {
	const cx = 125; // centro horizontal del personaje

	// ── Caras expresivas según el número de errores ──
	// La cara cambia para darle personalidad al muñeco:
	// 0-1 errores: sonriente | 2-4: preocupado | 5-6: pánico
	function getFace() {
			const fc = "var(--accent)";

			if (mistakes <= 1) {
					// Cara sonriente :)
					return `
							<g opacity="0.75">
									<circle cx="${cx - 5}" cy="37" r="2" fill="${fc}"/>
									<circle cx="${cx + 5}" cy="37" r="2" fill="${fc}"/>
									<path d="M${cx - 6} 43 Q${cx} 47 ${cx + 6} 43"
											stroke="${fc}" stroke-width="2" fill="none" stroke-linecap="round"/>
							</g>`;
			}

			if (mistakes <= 4) {
					// Cara preocupada :|
					return `
							<g opacity="0.75">
									<circle cx="${cx - 5}" cy="37" r="2" fill="${fc}"/>
									<circle cx="${cx + 5}" cy="37" r="2" fill="${fc}"/>
									<path d="M${cx - 8} 33 Q${cx - 5} 31 ${cx - 2} 33"
											stroke="${fc}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
									<path d="M${cx + 2} 33 Q${cx + 5} 31 ${cx + 8} 33"
											stroke="${fc}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
									<line x1="${cx - 6}" y1="44" x2="${cx + 6}" y2="44"
											stroke="${fc}" stroke-width="2" stroke-linecap="round"/>
							</g>`;
			}

			// Cara de pánico X_X
			return `
					<g opacity="0.75">
							<path d="M${cx - 8} 34 L${cx - 3} 39 M${cx - 3} 34 L${cx - 8} 39"
									stroke="${fc}" stroke-width="2" stroke-linecap="round"/>
							<path d="M${cx + 3} 34 L${cx + 8} 39 M${cx + 8} 34 L${cx + 3} 39"
									stroke="${fc}" stroke-width="2" stroke-linecap="round"/>
							<ellipse cx="${cx}" cy="45" rx="4" ry="3" fill="${fc}"/>
					</g>`;
	}

	// ── Las 6 partes del cuerpo (aparecen una por error) ──
	const fc = "var(--accent)";
	const bodyParts = [
			// 1. Cabeza + cara
			`<g>
					<circle cx="${cx}" cy="37" r="14" stroke="${fc}" stroke-width="2" fill="none" opacity="0.75"/>
					${getFace()}
			</g>`,
			// 2. Cuerpo
			`<rect x="${cx - 7}" y="51" width="14" height="30" rx="6" fill="${fc}" opacity="0.75"/>`,
			// 3. Brazo izquierdo
			`<path d="M${cx - 7} 60 Q${cx - 22} 63 ${cx - 28} 72"
					stroke="${fc}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.75"/>`,
			// 4. Brazo derecho
			`<path d="M${cx + 7} 60 Q${cx + 22} 63 ${cx + 28} 72"
					stroke="${fc}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.75"/>`,
			// 5. Pierna izquierda
			`<path d="M${cx - 3} 81 Q${cx - 10} 95 ${cx - 16} 108"
					stroke="${fc}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.75"/>`,
			// 6. Pierna derecha
			`<path d="M${cx + 3} 81 Q${cx + 10} 95 ${cx + 16} 108"
					stroke="${fc}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.75"/>`,
	];

	// ── Nudo o cuerda según si hay errores ──
	const ropeEnd = mistakes >= 1
			? `<path d="M119 16 Q118 24 125 26 Q132 24 131 16 Q131 10 125 10 Q120 10 119 14"
					stroke="var(--color)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`
			: `<line x1="125" y1="16" x2="125" y2="26"
					stroke="var(--color)" stroke-width="3" stroke-linecap="round" stroke-dasharray="3 3"/>`;

	// ── Tomar solo las partes según el número de errores ──
	const visibleParts = bodyParts.slice(0, mistakes).join("");

	// ── SVG completo ──
	const svg = `
			<svg viewBox="0 0 200 180" width="190" height="180">
					<!-- Tapete decorativo -->
					<rect x="36" y="163" width="108" height="14" rx="4" fill="${fc}" opacity="0.12"/>
					<rect x="40" y="165" width="100" height="10" rx="3" fill="none"
							stroke="${fc}" stroke-width="1" opacity="0.25"/>
					<line x1="48" y1="168" x2="136" y2="168"
							stroke="${fc}" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.3"/>

					<!-- Pies de la base -->
					<line x1="52" y1="163" x2="44" y2="163"
							stroke="var(--color)" stroke-width="4" stroke-linecap="round"/>
					<line x1="122" y1="163" x2="130" y2="163"
							stroke="var(--color)" stroke-width="4" stroke-linecap="round"/>

					<!-- Base -->
					<line x1="47" y1="163" x2="128" y2="163"
							stroke="var(--color)" stroke-width="4" stroke-linecap="round"/>

					<!-- Poste vertical -->
					<line x1="75" y1="163" x2="75" y2="10"
							stroke="var(--color)" stroke-width="4" stroke-linecap="round"/>

					<!-- Viga horizontal -->
					<line x1="75" y1="10" x2="125" y2="10"
							stroke="var(--color)" stroke-width="4" stroke-linecap="round"/>

					<!-- Diagonal de refuerzo -->
					<line x1="75" y1="38" x2="97" y2="10"
							stroke="var(--color)" stroke-width="2.5" stroke-linecap="round"/>

					<!-- Soga -->
					<line x1="125" y1="10" x2="125" y2="16"
							stroke="var(--color)" stroke-width="4" stroke-linecap="round"/>

					<!-- Nudo o cuerda -->
					${ropeEnd}

					<!-- Partes del cuerpo -->
					${visibleParts}
			</svg>`;

	container.innerHTML = svg;
}


function toggleTheme() {
	let currentTheme = document.documentElement.getAttribute("data-theme");
	console.log("Estoy en toggleTheme")
	console.log(currentTheme);
	// const allButtons = document.querySelectorAll(".theme-btn");

	if (currentTheme != "dark") {
		document.documentElement.setAttribute("data-theme", "dark");
		
		for (changeButton of toggleButtons) {
			changeButton.textContent = "☀";
		}
		localStorage.setItem("theme", "dark");
	} else {
		document.documentElement.removeAttribute("data-theme");
		for (changeButton of toggleButtons) {
			changeButton.textContent = "☾";
		}
		localStorage.setItem("theme", "light");
	}
}



if (localStorage.getItem("theme") === "dark") {
	document.documentElement.setAttribute("data-theme", "dark");
	for (changeButton of toggleButtons) {
		changeButton.textContent = "☀";
	}
} else {
	document.documentElement.setAttribute("data-theme", "light");
	for (changeButton of toggleButtons) {
		changeButton.textContent = "☾";
	}
}

document.getElementById("footer-year").textContent = new Date().getFullYear();