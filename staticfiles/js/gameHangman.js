src = "https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"

const letterContainer = document.getElementById("letter-container");
const optionsContainer = document.getElementById("options-container");
const userInputSection = document.getElementById("user-input-section");
const newGameContainer = document.getElementById("new-game-container");
const newGameButton = document.getElementById("new-game-button");
const canvas = document.getElementById("canvas");
const resultText = document.getElementById("result-text");

let options = {
  Linguagens: [
    "Python",
    "JavaScript",
    "Java",
    "TypeScript",
    "Ruby",
    "Kotlin",
    "PHP",
    "Swift",
    "Go",
    "Rust",
    "C#",
    "Scala"
  ],
  Frameworks: [
    "React",
    "Angular",
    "Django",
    "Laravel",
    "Spring",
    "Flutter",
    "Vue",
    "Express",
    "FastAPI",
    "NextJS",
    "Svelte",
    "Bootstrap"
  ],
  "Banco de dados": [
    "MongoDB",
    "PostgreSQL",
    "MySQL",
    "Oracle",
    "Redis",
    "Cassandra",
    "Firebase",
    "Supabase",
    "DynamoDB",
    "MariaDB",
    "SQLite",
    "Neo4j",
    "CouchDB"
  ],
};

//count
let winCount = 0;
let count = 0;

let chosenWord = "";

//Display option buttons
const displayOptions = () => {
  optionsContainer.innerHTML += `<h4>Selecione uma opção</h4>`;
  let buttonCon = document.createElement("div");
  for (let value in options) {
    buttonCon.innerHTML += `<button class="btn-border" onclick="generateWord('${value}')">${value}</button>`;
  }
  optionsContainer.appendChild(buttonCon);
};

//Block all the Buttons
const blocker = () => {
  let optionsButtons = document.querySelectorAll(".options");
  let letterButtons = document.querySelectorAll(".letters");
  //disable all options
  optionsButtons.forEach((button) => {
    button.disabled = true;
  });

  //disable all letters
  letterButtons.forEach((button) => {
    button.disabled.true;
  });
  newGameContainer.classList.remove("hide");
};

//Word Generator
const generateWord = (optionValue) => {
  let optionsButtons = document.querySelectorAll(".options");
  //If optionValur matches the button innerText then highlight the button
  optionsButtons.forEach((button) => {
    if (button.innerText.toLowerCase() === optionValue) {
      button.classList.add("active");
    }
    button.disabled = true;
  });

  //initially hide letters, clear previous word
  letterContainer.classList.remove("hide");
  userInputSection.innerText = "";

  let optionArray = options[optionValue];
  //choose random word
  chosenWord = optionArray[Math.floor(Math.random() * optionArray.length)];
  chosenWord = chosenWord.toUpperCase();

  //replace every letter with span containing dash
  let displayItem = chosenWord.replace(/./g, '<span class="dashes">_</span>');

  //Display each element as span
  userInputSection.innerHTML = displayItem;
};

//Initial Function (Called when page loads/user presses new game)
const initializer = () => {
  winCount = 0;
  count = 0;

  //Initially erase all content and hide letteres and new game button
  userInputSection.innerHTML = "";
  optionsContainer.innerHTML = "";
  letterContainer.classList.add("hide");
  newGameContainer.classList.add("hide");
  letterContainer.innerHTML = "";

  // Função para processar tentativa de letra
  const processGuess = (letter) => {
    if (!chosenWord) return; // Se não houver palavra escolhida, retorna
    
    let charArray = chosenWord.split("");
    let dashes = document.getElementsByClassName("dashes");
    
    if (charArray.includes(letter)) {
      charArray.forEach((char, index) => {
        if (char === letter) {
          dashes[index].innerText = char;
          winCount += 1;
          if (winCount == charArray.length) {
            resultText.innerHTML = `<div class='message'><h2 class='win-msg'>Você venceu!</h2><p>A palavra era: <span>${chosenWord}</span></p></div>`;
            shoot();
            blocker();
            try {
              updateScore(10);
            } catch (error) {
              console.error("Erro ao atualizar pontuação:", error);
            }
          }
        }
      });
    } else {
      count += 1;
      drawMan(count);
      if (count == 6) {
        resultText.innerHTML = `<div class='message'><h2 class='lose-msg'>Você perdeu!</h2><p>A palavra era: <span>${chosenWord}</span></p></div>`;
        blocker();
      }
    }
  };

  // Criar botões de letras
  for (let i = 65; i < 91; i++) {
    let button = document.createElement("button");
    button.classList.add("letters");
    button.innerText = String.fromCharCode(i);
    
    button.addEventListener("click", () => {
      if (!button.disabled) {
        processGuess(button.innerText);
        button.disabled = true;
      }
    });
    
    letterContainer.append(button);
  }

  // Adicionar evento de tecla pressionada
  document.addEventListener("keyup", (e) => {
    const key = e.key.toUpperCase();
    // Verifica se é uma letra de A-Z
    if (/^[A-Z]$/.test(key)) {
      const buttons = document.querySelectorAll('.letters');
      buttons.forEach(button => {
        if (button.innerText === key && !button.disabled) {
          processGuess(key);
          button.disabled = true;
        }
      });
    }
  });

  displayOptions();
  //Call to canvasCreator (for clearing previous canvas and creating initial canvas)
  let { initialDrawing } = canvasCreator();
  //initialDrawing would draw the frame
  initialDrawing();
};

//Canvas
const canvasCreator = () => {
  let context = canvas.getContext("2d");
  context.beginPath();
  context.strokeStyle = "#000";
  context.lineWidth = 2;

  //For drawing lines
  const drawLine = (fromX, fromY, toX, toY) => {
    context.moveTo(fromX, fromY);
    context.lineTo(toX, toY);
    context.stroke();
  };

  const head = () => {
    context.beginPath();
    context.arc(70, 30, 10, 0, Math.PI * 2, true);
    context.stroke();
  };

  const body = () => {
    drawLine(70, 40, 70, 80);
  };

  const leftArm = () => {
    drawLine(70, 50, 50, 70);
  };

  const rightArm = () => {
    drawLine(70, 50, 90, 70);
  };

  const leftLeg = () => {
    drawLine(70, 80, 50, 110);
  };

  const rightLeg = () => {
    drawLine(70, 80, 90, 110);
  };

  //initial frame
  const initialDrawing = () => {
    //clear canvas
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    //bottom line
    drawLine(10, 130, 130, 130);
    //left line
    drawLine(10, 10, 10, 131);
    //top line
    drawLine(10, 10, 70, 10);
    //small top line
    drawLine(70, 10, 70, 20);
  };

  return { initialDrawing, head, body, leftArm, rightArm, leftLeg, rightLeg };
};

//draw the man
const drawMan = (count) => {
  let { head, body, leftArm, rightArm, leftLeg, rightLeg } = canvasCreator();
  switch (count) {
    case 1:
      head();
      break;
    case 2:
      body();
      break;
    case 3:
      leftArm();
      break;
    case 4:
      rightArm();
      break;
    case 5:
      leftLeg();
      break;
    case 6:
      rightLeg();
      break;
    default:
      break;
  }
};

//New Game
newGameButton.addEventListener("click", initializer);
window.onload = initializer;

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