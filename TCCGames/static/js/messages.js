document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.messages');
    
    messages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.5s ease-in-out forwards';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000); // mensagem desaparece após 5 segundos
    });
});