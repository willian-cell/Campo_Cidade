// Animações para o site Campo Cidade

// Função para animação suave ao rolar para seções específicas
function smoothScroll() {
    document.querySelectorAll('a.nav-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Função para animação de fade-in nas seções ao serem vistas
function fadeInOnScroll() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });

    document.querySelectorAll('.fade-section').forEach(section => {
        observer.observe(section);
    });
}

// Adicionar classe de fade para as seções
function applyFadeClasses() {
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('fade-section');
    });
}

// Função para animação do cabeçalho ao rolar a página
function animateHeaderOnScroll() {
    const header = document.querySelector('header');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// Adicionar classes de estilo para animações via JavaScript
function addAnimationStyles() {
    const style = document.createElement('style');
    style.innerHTML = `
        .fade-section {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }

        .fade-in {
            opacity: 1;
            transform: translateY(0);
        }

        header.scrolled {
            background-color: #28a745 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    `;
    document.head.appendChild(style);
}

// Inicializar todas as animações ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    smoothScroll();
    applyFadeClasses();
    fadeInOnScroll();
    animateHeaderOnScroll();
    addAnimationStyles();
});
