function updateUserName() {
    const nameInput = document.getElementById("name").value;

    if (!nameInput) {
        alert("Por favor, informe um nome.");
        return;
    }

    fetch('/update_name/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ name: nameInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Erro: ${data.error}`);
        } else {
            alert(data.message);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar o nome:', error);
        alert('Ocorreu um erro ao tentar atualizar o nome.');
    });
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