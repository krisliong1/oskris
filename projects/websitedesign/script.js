// ===== PROFESSIONAL WEBSITE INTERACTIONS =====
// Modern vanilla JavaScript for optimal performance

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSmoothScrolling();
    initHeaderScroll();
    initAnimationObserver();
    initFormHandling();
    initPerformanceOptimizations();
    initAnalytics();
});

// ===== SMOOTH SCROLLING =====
function initSmoothScrolling() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });

                // Track scroll clicks
                trackEvent('Navigation', 'Smooth Scroll', this.getAttribute('href'));
            }
        });
    });
}

// ===== HEADER SCROLL EFFECTS =====
function initHeaderScroll() {
    const header = document.querySelector('.header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Add/remove scrolled class for styling
        if (currentScroll > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Hide/show header on scroll
        if (currentScroll > lastScroll && currentScroll > 100) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        
        lastScroll = currentScroll;
    });
}

// ===== INTERSECTION OBSERVER FOR ANIMATIONS =====
function initAnimationObserver() {
    // Create intersection observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Track section views
                const sectionName = entry.target.id || entry.target.className;
                trackEvent('Section View', sectionName, window.location.pathname);
            }
        });
    }, observerOptions);

    // Observe sections for animation
    const animateElements = document.querySelectorAll(
        '.pain-card, .service-card, .testimonial-card, .pricing-card, .portfolio-item, .about-content'
    );
    
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

// ===== FORM HANDLING =====
function initFormHandling() {
    // WhatsApp contact tracking
    document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp"]').forEach(link => {
        link.addEventListener('click', function() {
            trackEvent('Contact', 'WhatsApp Click', this.href);
        });
    });

    // Email contact tracking
    document.querySelectorAll('a[href*="mailto"]').forEach(link => {
        link.addEventListener('click', function() {
            trackEvent('Contact', 'Email Click', this.href);
        });
    });

    // Button click tracking
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            const buttonType = this.className.includes('primary') ? 'Primary' : 'Secondary';
            trackEvent('Button Click', buttonType, buttonText);
        });
    });
}

// ===== PERFORMANCE OPTIMIZATIONS =====
function initPerformanceOptimizations() {
    // Lazy load images
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });

    // Preload critical resources
    preloadCriticalResources();

    // Optimize scrolling performance
    let ticking = false;
    function updateScrollElements() {
        // Update any scroll-dependent elements here
        ticking = false;
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateScrollElements);
            ticking = true;
        }
    });
}

function preloadCriticalResources() {
    // Preload critical fonts
    const fontLinks = [
        'https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZJhjp-Ek-_EeA.woff2'
    ];

    fontLinks.forEach(href => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'font';
        link.type = 'font/woff2';
        link.crossOrigin = 'anonymous';
        link.href = href;
        document.head.appendChild(link);
    });
}

// ===== ANALYTICS & TRACKING =====
function initAnalytics() {
    // Track page load time
    window.addEventListener('load', function() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        trackEvent('Performance', 'Page Load Time', loadTime);
    });

    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', throttle(() => {
        const scrollPercent = Math.round((window.pageYOffset / (document.body.scrollHeight - window.innerHeight)) * 100);
        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;
            if (maxScroll % 25 === 0) { // Track every 25%
                trackEvent('Scroll Depth', `${maxScroll}%`, window.location.pathname);
            }
        }
    }, 1000));

    // Track time on page
    let startTime = Date.now();
    window.addEventListener('beforeunload', function() {
        const timeOnPage = Math.round((Date.now() - startTime) / 1000);
        trackEvent('Engagement', 'Time on Page', timeOnPage);
    });
}

// ===== UTILITY FUNCTIONS =====
function trackEvent(category, action, label, value) {
    // Google Analytics 4 / Google Tag Manager tracking
    if (typeof gtag === 'function') {
        gtag('event', action, {
            event_category: category,
            event_label: label,
            value: value
        });
    }
    
    // Backup console logging for development
    if (window.location.hostname === 'localhost') {
        console.log('Track Event:', { category, action, label, value });
    }
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// ===== MOBILE MENU (IF NEEDED) =====
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!menuToggle.contains(event.target) && !navMenu.contains(event.target)) {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });
    }
}

// ===== ACCESSIBILITY ENHANCEMENTS =====
function initAccessibility() {
    // Add focus visible polyfill behavior
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('user-is-tabbing');
        }
    });

    document.addEventListener('mousedown', function() {
        document.body.classList.remove('user-is-tabbing');
    });

    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
        position: absolute;
        left: -10000px;
        top: auto;
        width: 1px;
        height: 1px;
        overflow: hidden;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.cssText = `
            position: static;
            width: auto;
            height: auto;
            overflow: visible;
            background: var(--primary);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            z-index: 9999;
        `;
    });

    skipLink.addEventListener('blur', function() {
        this.style.cssText = `
            position: absolute;
            left: -10000px;
            top: auto;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
    });

    document.body.insertBefore(skipLink, document.body.firstChild);
}

// ===== PROGRESSIVE ENHANCEMENT =====
// Add CSS for JavaScript-enabled features
document.documentElement.classList.add('js-enabled');

// Add animation classes
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    .header.scrolled {
        background: rgba(255, 255, 255, 0.98) !important;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1) !important;
    }
    
    .js-enabled .portfolio-overlay {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .skip-link:focus {
        position: static !important;
        width: auto !important;
        height: auto !important;
        overflow: visible !important;
    }
    
    .user-is-tabbing *:focus {
        outline: 2px solid var(--accent-bright) !important;
        outline-offset: 2px !important;
    }
`;
document.head.appendChild(style);

// Initialize accessibility enhancements
initAccessibility();

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    trackEvent('JavaScript Error', e.message, e.filename + ':' + e.lineno);
});

// ===== CRITICAL PERFORMANCE METRICS =====
// Core Web Vitals tracking
function trackCoreWebVitals() {
    // Largest Contentful Paint (LCP)
    if (typeof PerformanceObserver !== 'undefined') {
        const lcpObserver = new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1];
            trackEvent('Core Web Vitals', 'LCP', Math.round(lastEntry.startTime));
        });
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

        // First Input Delay (FID)
        const fidObserver = new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            entries.forEach((entry) => {
                trackEvent('Core Web Vitals', 'FID', Math.round(entry.processingStart - entry.startTime));
            });
        });
        fidObserver.observe({ entryTypes: ['first-input'] });

        // Cumulative Layout Shift (CLS)
        let clsScore = 0;
        const clsObserver = new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            entries.forEach((entry) => {
                if (!entry.hadRecentInput) {
                    clsScore += entry.value;
                }
            });
        });
        clsObserver.observe({ entryTypes: ['layout-shift'] });

        // Track CLS on page unload
        window.addEventListener('beforeunload', () => {
            trackEvent('Core Web Vitals', 'CLS', Math.round(clsScore * 1000) / 1000);
        });
    }
}

// Initialize Core Web Vitals tracking
trackCoreWebVitals();

// ===== CONVERSION OPTIMIZATION =====
// Track conversion funnel
function trackConversionFunnel() {
    // Track when users view pricing
    const pricingSection = document.querySelector('#pricing');
    if (pricingSection) {
        const pricingObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    trackEvent('Conversion Funnel', 'Viewed Pricing', 'Pricing Section');
                    pricingObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        pricingObserver.observe(pricingSection);
    }

    // Track contact section views
    const contactSection = document.querySelector('#contact');
    if (contactSection) {
        const contactObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    trackEvent('Conversion Funnel', 'Viewed Contact', 'Contact Section');
                    contactObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        contactObserver.observe(contactSection);
    }
}

trackConversionFunnel();

// Console welcome message
console.log('%c🦞 Oskris Professional Website Design', 'color: #2196F3; font-size: 16px; font-weight: bold;');
console.log('%cBuilt with professional standards for optimal performance and conversion.', 'color: #666; font-size: 12px;');