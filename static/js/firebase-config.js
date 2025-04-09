// Firebase Configuration and Authentication
let firebaseConfig = null;
let auth = null;
let currentUser = null;

// Show loading indicator
function showLoading(message = 'Loading...') {
    const loadingEl = document.createElement('div');
    loadingEl.className = 'global-loading';
    loadingEl.innerHTML = `
        <div class="loading-spinner"></div>
        <p>${message}</p>
    `;
    document.body.appendChild(loadingEl);
    
    // Add loading class to body for potential styling
    document.body.classList.add('is-loading');
}

// Hide loading indicator
function hideLoading() {
    const loadingEl = document.querySelector('.global-loading');
    if (loadingEl) {
        // Fade out effect
        loadingEl.classList.add('fade-out');
        setTimeout(() => {
            loadingEl.remove();
            document.body.classList.remove('is-loading');
        }, 300);
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `toast-notification ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Automatically remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Fetch Firebase config from backend
async function initializeFirebase() {
    try {
        showLoading('Initializing application...');
        
        const response = await fetch('/api/config/firebase');
        if (!response.ok) {
            throw new Error('Failed to fetch Firebase configuration');
        }
        
        firebaseConfig = await response.json();
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        auth = firebase.auth();
        
        // Set persistence to LOCAL (default) to keep user logged in
        // even when the page refreshes
        await auth.setPersistence(firebase.auth.Auth.Persistence.LOCAL);
        
        // Monitor auth state
        auth.onAuthStateChanged((user) => {
            currentUser = user; // Store user in global var
            
            const authStatus = document.getElementById('auth-status');
            const authContainer = document.getElementById('auth-container');
            const companyContainer = document.getElementById('company-container');
            const header = document.getElementById('header');
            
            if (user) {
                // Update header
                document.getElementById('header-user-email').textContent = user.email;
                
                // Show header with fade-in effect
                header.style.display = 'block';
                setTimeout(() => header.classList.add('visible'), 10);
                
                // Update auth status
                authStatus.textContent = `Logged in as: ${user.email}`;
                authStatus.className = 'auth-status logged-in';
                
                // Hide auth container with smooth transition
                authContainer.classList.add('fade-out');
                setTimeout(() => {
                    authContainer.style.display = 'none';
                    authContainer.classList.remove('fade-out');
                }, 300);
                
                // Check if user has a company
                loadUserCompany(user.uid).then(hasCompany => {
                    if (hasCompany) {
                        // User has a company, go to job descriptions
                        const jobContainer = document.getElementById('job-container');
                        
                        companyContainer.style.display = 'none';
                        jobContainer.style.display = 'block';
                        setTimeout(() => jobContainer.classList.add('visible'), 10);
                        
                        loadCompanyJobs();
                        showToast('Welcome back!', 'success');
                    } else {
                        // User doesn't have a company, show company form
                        companyContainer.style.display = 'block';
                        setTimeout(() => companyContainer.classList.add('visible'), 10);
                        
                        document.getElementById('job-container').style.display = 'none';
                        showToast('Please complete your company profile', 'info');
                    }
                    
                    hideLoading();
                }).catch(error => {
                    console.error('Error loading user company:', error);
                    showToast('Failed to load profile data', 'error');
                    hideLoading();
                });
            } else {
                // Hide header with smooth transition
                header.classList.remove('visible');
                setTimeout(() => header.style.display = 'none', 300);
                
                // Update auth status
                authStatus.textContent = 'Not logged in';
                authStatus.className = 'auth-status logged-out';
                
                // Show login container with fade-in effect
                authContainer.style.display = 'block';
                setTimeout(() => authContainer.classList.add('visible'), 10);
                
                // Hide other containers
                companyContainer.style.display = 'none';
                document.getElementById('job-container').style.display = 'none';
                
                // Clear company data on logout
                localStorage.removeItem('currentCompanyId');
                window.currentCompanyId = null;
                
                hideLoading();
            }
        });
    } catch (error) {
        console.error('Error initializing Firebase:', error);
        hideLoading();
        showToast('Failed to initialize application. Please refresh the page.', 'error');
    }
}

// Sign out function
async function signOut() {
    try {
        showLoading('Signing out...');
        await auth.signOut();
        
        // Clear any stored company data
        window.currentCompanyId = null;
        localStorage.removeItem('currentCompanyId');
        
        showToast('Signed out successfully', 'success');
    } catch (error) {
        console.error('Error signing out:', error);
        showToast('Error signing out: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Get current user (helper function)
function getCurrentUser() {
    return currentUser;
} 