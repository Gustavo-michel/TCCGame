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

//pegando o endpoint para mostrar os dados no home data
async function fetchHomeData() {
    try {
        const response = await fetch('/home_data/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Função auxiliar para atualizar elemento com segurança
        const updateElement = (id, value) => {
            const element = document.getElementById(id);
            if (element) {
                element.innerText = value;
            } else {
                console.warn(`Elemento com ID '${id}' não encontrado`);
            }
        };

        updateElement('level', data.level);
        updateElement('points', data.points.toLocaleString());
        // updateElement('position', `${data.position}º`);

        // // Atualiza posições do ranking
        // data.top_positions.forEach((user, idx) => {
        //     const positionElement = document.getElementById(`position-${idx + 1}`);
        //     if (positionElement) {
        //         const rankElement = positionElement.querySelector('h2');
        //         const nameElement = positionElement.querySelector('p');
                
        //         if (rankElement) rankElement.innerText = `${user.rank}º`;
        //         if (nameElement) nameElement.innerText = user.name;
        //     } else {
        //         console.warn(`Elemento position-${idx + 1} não encontrado`);
        //     }
        // });

    } catch (error) {
        console.error('Erro ao carregar dados:', error.message);
        // Opcional: Mostrar mensagem de erro para o usuário
        alert('Não foi possível carregar os dados. Por favor, tente novamente mais tarde.');
    }
}

// Pegando token
function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        .split('=')[1];
}

window.onload = fetchHomeData;