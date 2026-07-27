/**
 * MODERN ANIMATIONS
 * Sistema de animaciones dinámicas para mejorar la experiencia de usuario
 */

(function() {
    'use strict';

    // ============================================================================
    // INTERSECTION OBSERVER - Animaciones al hacer scroll
    // ============================================================================
    
    function initScrollAnimations() {
        // Animaciones muy sutiles al hacer scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -30px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    entry.target.style.opacity = '1';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Solo observar elementos que necesitan animación
        const elements = document.querySelectorAll('.card, .chart-card, .stat-card');
        elements.forEach((el) => {
            el.style.opacity = '0';
            observer.observe(el);
        });
    }

    // ============================================================================
    // RIPPLE EFFECT - Efecto de onda en botones
    // ============================================================================
    
    function createRipple(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;

        ripple.style.width = ripple.style.height = `${diameter}px`;
        ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
        ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
        ripple.classList.add('ripple');

        const rippleEffect = button.getElementsByClassName('ripple')[0];
        if (rippleEffect) {
            rippleEffect.remove();
        }

        button.appendChild(ripple);
    }

    function initRippleEffect() {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', createRipple);
        });
    }

    // ============================================================================
    // SMOOTH SCROLL - Scroll suave para anclas
    // ============================================================================
    
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href !== '#' && href !== '#!') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    // ============================================================================
    // COUNTER ANIMATION - Animación sutil de números
    // ============================================================================
    
    function animateCounter(element, target, duration = 800) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = Math.round(target);
                clearInterval(timer);
            } else {
                element.textContent = Math.round(current);
            }
        }, 16);
    }

    function initCounterAnimations() {
        // Deshabilitado por defecto para mantener sobriedad
        // Se puede activar con data-counter="true"
        const counters = document.querySelectorAll('[data-counter="true"]');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.textContent.replace(/[^0-9]/g, ''));
                    if (!isNaN(target) && target > 0) {
                        entry.target.textContent = '0';
                        animateCounter(entry.target, target);
                    }
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }

    // ============================================================================
    // PROGRESS BAR ANIMATION - Animación de barras de progreso
    // ============================================================================
    
    function initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const width = entry.target.style.width || entry.target.getAttribute('aria-valuenow') + '%';
                    entry.target.style.width = '0%';
                    
                    setTimeout(() => {
                        entry.target.style.width = width;
                    }, 100);
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => observer.observe(bar));
    }

    // ============================================================================
    // CARD SUBTLE HOVER - Efecto hover sutil en cards
    // ============================================================================
    
    function initCardHover() {
        // Efecto hover muy sutil, sin efectos 3D exagerados
        // El CSS ya maneja el hover básico
    }

    // ============================================================================
    // LOADING SKELETON - Skeleton screens para carga
    // ============================================================================
    
    function showLoadingSkeleton(container) {
        const skeleton = `
            <div class="loading-skeleton" style="height: 20px; margin-bottom: 10px;"></div>
            <div class="loading-skeleton" style="height: 20px; width: 80%; margin-bottom: 10px;"></div>
            <div class="loading-skeleton" style="height: 20px; width: 60%;"></div>
        `;
        container.innerHTML = skeleton;
    }

    function hideLoadingSkeleton(container, content) {
        container.innerHTML = content;
    }

    // ============================================================================
    // TOAST NOTIFICATIONS - Notificaciones modernas
    // ============================================================================
    
    function showToast(message, type = 'info', duration = 3000) {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type} fade-in-down`;
        toast.innerHTML = `
            <div class="toast-icon">
                <i class="bi bi-${getToastIcon(type)}"></i>
            </div>
            <div class="toast-message">${message}</div>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="bi bi-x"></i>
            </button>
        `;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(container);
        return container;
    }

    function getToastIcon(type) {
        const icons = {
            'success': 'check-circle-fill',
            'error': 'x-circle-fill',
            'warning': 'exclamation-triangle-fill',
            'info': 'info-circle-fill'
        };
        return icons[type] || icons.info;
    }

    // ============================================================================
    // PARALLAX EFFECT - Efecto parallax en headers
    // ============================================================================
    
    function initParallax() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.parallax || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // ============================================================================
    // LAZY LOAD IMAGES - Carga diferida de imágenes
    // ============================================================================
    
    function initLazyLoad() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('fade-in');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // ============================================================================
    // TYPING EFFECT - Efecto de escritura
    // ============================================================================
    
    function typeWriter(element, text, speed = 50) {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }

    // ============================================================================
    // CONFETTI EFFECT - Efecto de confeti para celebraciones
    // ============================================================================
    
    function createConfetti() {
        const colors = ['#667eea', '#764ba2', '#f093fb', '#10b981', '#f59e0b'];
        const confettiCount = 50;
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${Math.random() * 100}%;
                top: -10px;
                opacity: ${Math.random()};
                transform: rotate(${Math.random() * 360}deg);
                animation: confetti-fall ${2 + Math.random() * 3}s linear forwards;
                z-index: 9999;
            `;
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 5000);
        }
    }

    // Agregar animación de confeti al CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes confetti-fall {
            to {
                transform: translateY(100vh) rotate(720deg);
                opacity: 0;
            }
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .toast-notification {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 300px;
            max-width: 500px;
        }
        
        .toast-icon {
            font-size: 24px;
        }
        
        .toast-success { border-left: 4px solid #10b981; }
        .toast-success .toast-icon { color: #10b981; }
        
        .toast-error { border-left: 4px solid #ef4444; }
        .toast-error .toast-icon { color: #ef4444; }
        
        .toast-warning { border-left: 4px solid #f59e0b; }
        .toast-warning .toast-icon { color: #f59e0b; }
        
        .toast-info { border-left: 4px solid #3b82f6; }
        .toast-info .toast-icon { color: #3b82f6; }
        
        .toast-message {
            flex: 1;
            font-weight: 500;
        }
        
        .toast-close {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.2s;
        }
        
        .toast-close:hover {
            opacity: 1;
        }
        
        .fade-out {
            animation: fadeOut 0.3s ease-out forwards;
        }
        
        @keyframes fadeOut {
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }
    `;
    document.head.appendChild(style);

    // ============================================================================
    // INICIALIZACIÓN
    // ============================================================================
    
    function init() {
        // Esperar a que el DOM esté completamente cargado
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('🎨 Inicializando sistema electoral...');

        // Inicializar solo animaciones sutiles y profesionales
        initScrollAnimations();
        initSmoothScroll();
        initCounterAnimations();
        initProgressBars();
        initLazyLoad();

        console.log('✅ Sistema electoral inicializado');
    }

    // Exportar funciones útiles al objeto global
    window.ModernAnimations = {
        showToast,
        createConfetti,
        typeWriter,
        showLoadingSkeleton,
        hideLoadingSkeleton,
        animateCounter
    };

    // Inicializar
    init();

})();
