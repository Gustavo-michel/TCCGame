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

        if (response.ok) {
            const data = await response.json();

            document.getElementById('level').innerText = data.level;

            document.getElementById('position').innerText = `${data.position}º`;

            document.getElementById('points').innerText = data.points.toLocaleString();

            data.top_positions.forEach((user, idx) => {
                document.getElementById(`position-${idx + 1}`).querySelector('h2').innerText = `${user.rank}º`;
                document.getElementById(`position-${idx + 1}`).querySelector('p').innerText = user.name;
            });
        } else {
            console.error('Erro ao recuperar os dados do usuário');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
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