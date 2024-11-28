let container = document.querySelector(".container");
let winScreen = document.querySelector(".win-screen");
let submitButton = document.querySelector(".submit");

let maxGuesses = 6; // Número máximo de tentativas
let inputCount = 0;
let finalWord = ""; // Palavra atual sendo digitada
let tryCount = 0; // Número de tentativas feitas

// Lista de palavras possíveis (relacionadas a programação)
let words = [
    "ARRAY",
    "CLASS",
    "DEBUG",
    "ERROR",
    "FLOAT",
    "INPUT",
    "LINUX",
    "MACRO",
    "MYSQL",
    "PARSE",
    "PRINT",
    "PROXY",
    "QUERY",
    "REACT",
    "REDIS",
    "REGEX",
    "SCOPE",
    "SHELL",
    "STACK",
    "STYLE",
    "SWIFT",
    "TABLE",
    "THROW",
    "TOKEN",
    "TUPLE",
    "TYPES",
    "UNITY",
    "VALUE",
    "WHILE",
    "XPATH",
    "YIELD",
    "ASYNC",
    "BREAK",
    "CATCH",
    "CONST",
    "FETCH",
    "FINAL",
    "MAVEN",
    "QUEUE",
    "WRITE"
];

// Seleciona uma palavra aleatória
let word = words[Math.floor(Math.random() * words.length)];

// Cria a grade de inputs
const createInputs = () => {
    for (let i = 0; i < maxGuesses; i++) {
        let inputGroup = document.createElement("div");
        inputGroup.classList.add("input-group");
        
        for (let j = 0; j < 5; j++) {
            let input = document.createElement("input");
            input.type = "text";
            input.maxLength = 1;
            input.classList.add("input-box");
            input.disabled = i !== 0; // Habilita apenas a primeira linha
            inputGroup.appendChild(input);
        }
        
        container.appendChild(inputGroup);
    }
};

// Verifica a palavra inserida
const validateWord = async () => {
    let inputs = document.querySelectorAll(".input-group")[tryCount].querySelectorAll(".input-box");
    let successCount = 0;
    
    for (let i = 0; i < 5; i++) {
        let letter = inputs[i].value.toLowerCase();
        
        // Verifica se a letra está na posição correta
        if (letter === word[i].toLowerCase()) {
            inputs[i].classList.add("correct");
            successCount++;
        }
        // Verifica se a letra existe na palavra
        else if (word.toLowerCase().includes(letter)) {
            inputs[i].classList.add("exists");
        }
        // Letra incorreta
        else {
            inputs[i].classList.add("incorrect");
        }
        
        inputs[i].disabled = true;
    }
    
    // Incrementa tentativa
    tryCount += 1;
    
    // Se acertou todas as letras
    if (successCount === 5) {
        // Mostra tela de vitória
        winScreen.classList.remove("hide");
        winScreen.innerHTML = `
            <div class='message'><h2 class='win-msg'>Você venceu!</h2><p>Você acertou em: <span>${tryCount}</span> tentativas</p></div>
            <button class="btn-green" onclick="location.reload()">Novo Jogo</button>`;
        // Adiciona pontos
        const pointsEarned = 100;
        getUserId().then(userId => {
            if (userId) {
                updateScore(userId, pointsEarned);
            }
        });
    }
    // Se acabaram as tentativas
    else if (tryCount === maxGuesses) {
        winScreen.classList.remove("hide");
        winScreen.innerHTML = `
            <div class='message'><h2 class='lose-msg'>Você perdeu!</h2><p>A palavra era: <span>${word}</span></p></div>
            <button class="btn-green" onclick="location.reload()">Tentar Novamente</button>`;
    }
    // Próxima tentativa
    else {
        let nextInputs = document.querySelectorAll(".input-group")[tryCount].querySelectorAll(".input-box");
        nextInputs.forEach(input => input.disabled = false);
        inputCount = 0;
    }
};

// Eventos de input
const eventListeners = () => {
    container.addEventListener("input", (e) => {
        if (e.target.classList.contains("input-box")) {
            let value = e.target.value.toUpperCase();
            e.target.value = value;
            
            if (value && e.target.nextElementSibling) {
                e.target.nextElementSibling.focus();
                inputCount++;
            }
        }
    });

    // Permite usar backspace para voltar
    container.addEventListener("keydown", (e) => {
        if (e.target.classList.contains("input-box")) {
            if (e.key === "Backspace" && !e.target.value && e.target.previousElementSibling) {
                e.target.previousElementSibling.focus();
                inputCount--;
            }
        }
    });

    // Mostra botão de enviar quando palavra completa
    container.addEventListener("input", () => {
        let inputs = document.querySelectorAll(".input-group")[tryCount].querySelectorAll(".input-box");
        finalWord = "";
        
        inputs.forEach((input) => {
            finalWord += input.value.toLowerCase();
        });
        
        if (finalWord.length === 5) {
            submitButton.classList.remove("hide");
        } else {
            submitButton.classList.add("hide");
        }
    });

    submitButton.addEventListener("click", validateWord);
};

// Inicializa o jogo
window.onload = () => {
    createInputs();
    eventListeners();
};