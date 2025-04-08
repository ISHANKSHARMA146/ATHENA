// Firebase Configuration and Authentication
let firebaseConfig = null;
let auth = null;

// Fetch Firebase config from backend
async function initializeFirebase() {
    try {
        const response = await fetch('/api/config/firebase');
        firebaseConfig = await response.json();
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        auth = firebase.auth();
        
        // Monitor auth state
        auth.onAuthStateChanged((user) => {
            const authStatus = document.getElementById('auth-status');
            const authContainer = document.getElementById('auth-container');
            const companyContainer = document.getElementById('company-container');
            const header = document.getElementById('header');
            
            if (user) {
                // Update header
                document.getElementById('header-user-email').textContent = user.email;
                header.style.display = 'block';
                
                // Update auth status
                authStatus.textContent = `Logged in as: ${user.email}`;
                authStatus.className = 'auth-status logged-in';
                
                // Hide auth container
                authContainer.style.display = 'none';
                
                // Check if user has a company
                loadUserCompany(user.uid).then(hasCompany => {
                    if (hasCompany) {
                        // User has a company, go to job descriptions
                        document.getElementById('job-container').style.display = 'block';
                        companyContainer.style.display = 'none';
                        loadCompanyJobs();
                    } else {
                        // User doesn't have a company, show company form
                        companyContainer.style.display = 'block';
                        document.getElementById('job-container').style.display = 'none';
                    }
                });
            } else {
                // Hide header
                header.style.display = 'none';
                
                // Update auth status
                authStatus.textContent = 'Not logged in';
                authStatus.className = 'auth-status logged-out';
                
                // Show login container
                authContainer.style.display = 'block';
                companyContainer.style.display = 'none';
                document.getElementById('job-container').style.display = 'none';
                
                // Clear company data on logout
                localStorage.removeItem('currentCompanyId');
                window.currentCompanyId = null;
            }
        });
    } catch (error) {
        console.error('Error initializing Firebase:', error);
        alert('Error initializing the application. Please try again later.');
    }
}

// Sign out function
async function signOut() {
    try {
        await auth.signOut();
        // Clear any stored company data
        window.currentCompanyId = null;
        localStorage.removeItem('currentCompanyId');
    } catch (error) {
        alert('Error signing out: ' + error.message);
    }
} 