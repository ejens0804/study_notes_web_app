// File: static/js/main.js

// Highlight active navigation link
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Card animation function
function updateCard(card) {
    card.style.transform = 'scale(0.95)';
    setTimeout(() => {
        card.style.transform = 'scale(1)';
    }, 200);
}