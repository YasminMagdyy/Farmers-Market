document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations for all pages
    initScrollAnimations();
    initNavbarScroll();
    initSmoothScrolling();
    
    // Page-specific initializations
    if (document.querySelector('.blog-list-container')) {
        initBlogListAnimations();
    }
    
    if (document.querySelector('.home-gif-banner')) {
        initHomePageAnimations();
    }
});

function initScrollAnimations() {
    // Generic scroll animations for elements with .scroll-animate class
    const scrollElements = document.querySelectorAll('.scroll-animate');
    
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                scrollObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    scrollElements.forEach(element => {
        scrollObserver.observe(element);
    });
}

function initBlogListAnimations() {
    // Blog list specific animations (alternating left/right)
    const blogPosts = document.querySelectorAll('.blog-post');
    
    const blogObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 150);
                blogObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });

    blogPosts.forEach(post => {
        blogObserver.observe(post);
    });
}

function initHomePageAnimations() {
    // Homepage specific animations
    const carousel = document.getElementById('testimonial-carousel');
    if (carousel) {
        // Initialize Bootstrap carousel if exists
        new bootstrap.Carousel(carousel, {
            interval: 5000,
            pause: 'hover'
        });
    }
}

function initNavbarScroll() {
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function initSmoothScrolling() {
    // Smooth scrolling for all anchor links
    document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(targetId);
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
}
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link');

    // Function to set active tab based on current URL
    const setActiveTab = () => {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            const linkPath = new URL(link.href, window.location.origin).pathname;
            if (linkPath === currentPath || (currentPath === '/' && linkPath.includes('home'))) {
                link.classList.add('active');
            } else {
                link.classList.remove('active', 'flipping');
            }
        });
    };

    // Set active tab on page load
    setActiveTab();

    // Handle click events for nav links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Remove flipping and active from all links
            navLinks.forEach(l => l.classList.remove('flipping', 'active'));

            // Add flipping and active to clicked link
            link.classList.add('flipping', 'active');

            // Remove flipping after animation (400ms)
            setTimeout(() => {
                link.classList.remove('flipping');
            }, 400); // Changed from 400 to 600 to match CSS transition duration
        });
    });

    // Update active tab on popstate (browser back/forward)
    window.addEventListener('popstate', setActiveTab);
});