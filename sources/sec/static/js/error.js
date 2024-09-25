document.addEventListener('DOMContentLoaded', (event) => {
    const error = document.querySelector('.alert.alert-danger');

    if (error) {
        setTimeout(() => {
            error.style.transition = 'opacity 0.5s';
            error.style.opacity = '0';
            setTimeout(() => {
                error.remove();
            }, 500); 
        }, 2000); 
    }
});