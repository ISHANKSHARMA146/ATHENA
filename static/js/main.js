// Main JavaScript file for initialization

// Check if the app is running in development mode
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

// Debug log function that only outputs in development
function debug(message, data) {
    if (isDevelopment) {
        console.log(`[Athena Debug] ${message}`, data || '');
    }
}

// Initialize UI themes
function initializeTheme() {
    // Check for stored theme preference
    const savedTheme = localStorage.getItem('athena-theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
        // Default to system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
}

// Lazy load images for better performance
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    // Use IntersectionObserver if available
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.getAttribute('data-src');
                    image.removeAttribute('data-src');
                    imageObserver.unobserve(image);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.getAttribute('data-src');
            img.removeAttribute('data-src');
        });
    }
}

// Enhance form accessibility
function enhanceFormAccessibility() {
    // Add focus states and ARIA attributes
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            // Generate IDs for inputs without them
            if (!input.id) {
                const randomId = 'input-' + Math.random().toString(36).substring(2, 9);
                input.id = randomId;
            }
            
            // Ensure labels are associated with inputs
            const label = input.previousElementSibling;
            if (label && label.tagName === 'LABEL' && !label.htmlFor) {
                label.htmlFor = input.id;
            }
        });
    });
}

// Add responsive design enhancements
function enhanceResponsiveness() {
    // Set viewport height variable for mobile browsers
    const setVH = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    };
    
    // Set initially and on resize
    setVH();
    window.addEventListener('resize', setVH);
}

// Main initialization function
function initializeApp() {
    debug('Initializing application');
    
    // Initialize UI enhancements
    initializeTheme();
    enhanceFormAccessibility();
    enhanceResponsiveness();
    
    // Initialize Firebase
    initializeFirebase();
    
    // Check if user is already logged in and has a company
    const savedCompanyId = localStorage.getItem('currentCompanyId');
    if (savedCompanyId) {
        window.currentCompanyId = savedCompanyId;
        debug('Found saved company ID', savedCompanyId);
    }
    
    // Load component templates
    loadComponents();
    
    // Register service worker if supported
    if ('serviceWorker' in navigator && !isDevelopment) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(registration => {
                    debug('ServiceWorker registered', registration.scope);
                })
                .catch(error => {
                    console.error('ServiceWorker registration failed:', error);
                });
        });
    }
}

// Load HTML components from separate files
function loadComponents() {
    debug('Loading component templates');
    
    const componentRequests = [
        {
            url: '/components/company/company-form.html',
            targetId: 'company-form-container'
        },
        {
            url: '/components/job/job-form.html',
            targetId: 'job-form-container'
        }
    ];
    
    // Use Promise.all to load all components in parallel
    Promise.all(
        componentRequests.map(req => 
            fetch(req.url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to load component: ${req.url}`);
                    }
                    return response.text();
                })
                .then(html => {
                    document.getElementById(req.targetId).innerHTML = html;
                    return { success: true, component: req.targetId };
                })
                .catch(error => {
                    console.error('Error loading component:', error);
                    return { success: false, component: req.targetId, error };
                })
        )
    ).then(results => {
        debug('Components loaded', results);
        
        // Initialize any component-specific logic after loading
        results.forEach(result => {
            if (result.success) {
                if (result.component === 'company-form-container') {
                    // Initialize company form features if needed
                }
                if (result.component === 'job-form-container') {
                    // Initialize job form features if needed
                }
            }
        });
        
        // Lazy load images after components are loaded
        lazyLoadImages();
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeApp); 