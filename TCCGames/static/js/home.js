$(document).ready(function() {

    // Menu-mobile
    $('#btn-mobile').on('click', function () {
        $('#menu-mobile').toggleClass('active');
        $('#btn-mobile').find('i').toggleClass('fa-x');
    });

    // Header-boxshadow
    const sections = $('section');
    const navItems = $('.nav-item');

    $(window).on('scroll', function () {
        const header = $('header');
        const scrollPosition = $(window).scrollTop() - header.outerHeight();

        let activeSectionIndex = 0;

        if (scrollPosition <= 0) {
            header.css('box-shadow', 'none');
        } else {
            header.css('box-shadow', '5px 1px 5px rgba(0, 0, 0, 0.1');
        }

        sections.each(function(i) {
            const section = $(this);
            const sectionTop = section.offset().top - 96;
            const sectionBottom = sectionTop+ section.outerHeight();

            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                activeSectionIndex = i;
                return false;
            }
        })

        navItems.removeClass('active');
        $(navItems[activeSectionIndex]).addClass('active');
    });
});

// pegando o endpoint para mostrar os dados no home data
async function fetchHomeData() {
    try {
        const response = await fetch('/user_data/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Dados recebidos:", data); // Para debug

        // Atualiza os elementos na página
        const levelElement = document.getElementById('level');
        const pointsElement = document.getElementById('points');
        // alert(`Parabéns! Você alcançou o nível ${data.level}`);

        if (levelElement) {
            levelElement.textContent = data.level || 1;
        }

        if (pointsElement) {
            pointsElement.textContent = (data.points || 0).toLocaleString();
        }

    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        // Em caso de erro, define valores padrão
        const levelElement = document.getElementById('level');
        const pointsElement = document.getElementById('points');

        if (levelElement) levelElement.textContent = '1';
        if (pointsElement) pointsElement.textContent = '0';
    }
}

document.addEventListener('DOMContentLoaded', fetchHomeData);
setInterval(fetchHomeData, 10000);

function fetchAndDisplayPositionData() {
    fetch('/position_users/', {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.statusText}`);
            }
            return response.json();
        })
        .then((data) => {
            const userPosition = data.user_position;
            if (userPosition) {
                document.getElementById("level").textContent = userPosition.level || "N/A";
                document.getElementById("position").textContent = userPosition.position || "N/A";
                document.getElementById("points").textContent = userPosition.points || "N/A";
            }

            const top3 = data.top_3 || [];
            for (let i = 0; i < top3.length; i++) {
                const positionElement = document.getElementById(`position-${i + 1}`);
                if (positionElement) {
                    positionElement.querySelector("h2").textContent = `${String(i + 1).padStart(2, "0")}º`;
                    positionElement.querySelector("p").textContent = top3[i].name || "Anônimo";
                }
            }
        })
        .catch((error) => {
            console.error("Erro ao carregar os dados:", error);
        });
}

document.addEventListener("DOMContentLoaded", fetchAndDisplayPositionData);
setInterval(fetchAndDisplayPositionData, 10000);