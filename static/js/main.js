// Main JavaScript file for initialization

// Initialize data on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Firebase
    initializeFirebase();
    
    // Check if user is already logged in and has a company
    const savedCompanyId = localStorage.getItem('currentCompanyId');
    if (savedCompanyId) {
        window.currentCompanyId = savedCompanyId;
    }
    
    // The auth state change handler will take care of showing appropriate screens
}); 