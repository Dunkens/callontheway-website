// Mobile Navigation Menu
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const body = document.body;
    
    // Toggle mobile menu
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            body.classList.toggle('nav-open');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (navMenu.classList.contains('active') && 
                !navMenu.contains(e.target) && 
                !navToggle.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
            }
        });
        
        // Close menu when pressing Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
            }
        });
    }
    
    // Handle mega dropdown section headings on mobile (AC, Heating, Air Quality)
    const sectionHeadings = document.querySelectorAll('.nav-dropdown-heading');
    
    sectionHeadings.forEach(function(heading) {
        heading.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                e.stopPropagation();
                const section = heading.parentElement;
                section.classList.toggle('section-expanded');
            }
        });
    });
    
    // Handle dropdown menus on mobile
    const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');
    
    dropdownItems.forEach(function(item) {
        const link = item.querySelector('.nav-link');
        
        link.addEventListener('click', function(e) {
            // Only prevent default on mobile (when menu is in mobile mode)
            if (window.innerWidth <= 992) {
                e.preventDefault();
                
                // Close other dropdowns
                dropdownItems.forEach(function(otherItem) {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current dropdown
                item.classList.toggle('active');
            }
        });
    });
    
    // Close mobile menu when clicking a non-dropdown link
    const navLinks = document.querySelectorAll('.nav-menu a:not(.nav-link)');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
            }
        });
    });
    
    // Reset menu state on window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth > 992) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                body.classList.remove('nav-open');
                dropdownItems.forEach(function(item) {
                    item.classList.remove('active');
                });
            }
        }, 250);
    });
});
