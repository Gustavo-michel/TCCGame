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

// Chama a função quando a página carrega
document.addEventListener('DOMContentLoaded', fetchHomeData);

// Atualiza os dados a cada 30 segundos (opcional)
setInterval(fetchHomeData, 30000);