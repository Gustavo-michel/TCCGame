src = "https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"

let container = document.querySelector(".container");
let winScreen = document.querySelector(".win-screen");
let submitButton = document.querySelector(".submit");

let maxGuesses = 6; // Número máximo de tentativas
let inputCount = 0;
let finalWord = ""; // Palavra atual sendo digitada
let tryCount = 0; // Número de tentativas feitas

let words = [
    "ARRAY",
    // "CLASS",
    // "DEBUG",
    // "ERROR",
    // "FLOAT",
    // "INPUT",
    // "LINUX",
    // "MACRO",
    // "MYSQL",
    // "PARSE",
    // "PRINT",
    // "PROXY",
    // "QUERY",
    // "REACT",
    // "REDIS",
    // "REGEX",
    // "SCOPE",
    // "SHELL",
    // "STACK",
    // "STYLE",
    // "SWIFT",
    // "TABLE",
    // "THROW",
    // "TOKEN",
    // "TUPLE",
    // "TYPES",
    // "UNITY",
    // "VALUE",
    // "WHILE",
    // "XPATH",
    // "YIELD",
    // "ASYNC",
    // "BREAK",
    // "CATCH",
    // "CONST",
    // "FETCH",
    // "FINAL",
    // "MAVEN",
    // "QUEUE",
    // "WRITE"
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
        submitButton.classList.add("hide");
        winScreen.innerHTML = `
            <div class='message'><h2 class='win-msg'>Você venceu!</h2><p>Você acertou em: <span>${tryCount}</span> tentativas</p></div>
            <button class="btn-green" onclick="location.reload()">Novo Jogo</button>`;
        shoot();
        console.log("Atualizando pontuação...");
        try {
            updateScore(10);
        } catch (error) {
            console.error("Erro ao atualizar pontuação:", error);
        }
    }
    // Se acabaram as tentativas
    else if (tryCount === maxGuesses) {
        winScreen.classList.remove("hide");
        submitButton.classList.add("hide");
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

    // Permite usar backspace para voltar e Enter para enviar
    container.addEventListener("keydown", (e) => {
        if (e.target.classList.contains("input-box")) {
            if (e.key === "Backspace" && !e.target.value && e.target.previousElementSibling) {
                e.target.previousElementSibling.focus();
                inputCount--;
            } else if (e.key === "Enter" && finalWord.length === 5) {
                validateWord();
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

// Confetti animaton
function shoot() {

    var defaults = {
      spread: 360,
      ticks: 100,
      gravity: 0,
      decay: 1,
      startVelocity: 10,
      colors: ['FFE400', 'FFBD00', 'E89400', 'FFCA6C', 'FDFFB8']
    };
  
  
    confetti({
      ...defaults,
      particleCount: 30,
      scalar: 1.5,
      shapes: ['star']
    });
  
    confetti({
      ...defaults,
      particleCount: 10,
      scalar: 1,
      shapes: ['circle']
    });
  }

// Inicializa o jogo
window.onload = () => {
    createInputs();
    eventListeners();
};

// Get Endpoint
async function updateScore(pointsEarned) {
    try {
        const response = await fetch('/update_score/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            credentials: 'include',
            body: JSON.stringify({ points_earned: pointsEarned })
        });
  
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Erro ao atualizar pontuação');
        }
  
        const data = await response.json();
        // document.getElementById('points').innerText = data.points;
        // document.getElementById('level').innerText = data.level;
        // alert(`Parabéns! Você alcançou o nível ${data.level}`);
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro ao atualizar pontuação. Por favor, tente novamente.");
    }
  }
  
  function getCSRFToken() {
      const cookieValue = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken'));
      
      if (!cookieValue) {
          return null;
      }
      
      return cookieValue.split('=')[1];
  }