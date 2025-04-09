// Authentication related functions

// Show auth form with smooth transitions
function showAuthForm(formType) {
    // Hide all forms with fade effect
    const forms = document.querySelectorAll('.auth-form');
    forms.forEach(form => {
        if (form.classList.contains('active')) {
            form.classList.add('fade-out');
            setTimeout(() => {
                form.classList.remove('active', 'fade-out');
            }, 200);
        } else {
            form.classList.remove('active');
        }
    });
    
    // Show selected form with fade-in effect
    setTimeout(() => {
        const targetForm = document.getElementById(`${formType}-form`);
        targetForm.classList.add('active');
    }, 250);
    
    // Update tabs
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    if (formType === 'login' || formType === 'signup') {
        document.querySelector(`.auth-tab:nth-child(${formType === 'login' ? 1 : 2})`).classList.add('active');
    }
}

// Real-time email validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Input validation for login form
function validateLoginForm() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const signInBtn = document.getElementById('login-btn');
    
    const isEmailValid = validateEmail(email);
    const isPasswordValid = password.length >= 6;
    
    // Update UI for email validation
    const emailInput = document.getElementById('login-email');
    emailInput.classList.toggle('input-error', email && !isEmailValid);
    emailInput.classList.toggle('input-success', email && isEmailValid);
    
    // Enable/disable sign in button
    signInBtn.disabled = !(isEmailValid && isPasswordValid);
}

// Add input listeners for login form
function setupLoginValidation() {
    const emailInput = document.getElementById('login-email');
    const passwordInput = document.getElementById('login-password');
    
    emailInput.addEventListener('input', validateLoginForm);
    passwordInput.addEventListener('input', validateLoginForm);
}

// Validate password requirements with real-time feedback
function validatePassword() {
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const emailInput = document.getElementById('signup-email');
    const email = emailInput.value;
    
    // Email validation
    const isEmailValid = validateEmail(email);
    emailInput.classList.toggle('input-error', email && !isEmailValid);
    emailInput.classList.toggle('input-success', email && isEmailValid);
    
    // Password requirements
    const hasLength = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const passwordsMatch = password === confirmPassword && password !== '';
    
    // Update requirement indicators
    document.getElementById('length-req').classList.toggle('valid', hasLength);
    document.getElementById('uppercase-req').classList.toggle('valid', hasUppercase);
    document.getElementById('lowercase-req').classList.toggle('valid', hasLowercase);
    document.getElementById('number-req').classList.toggle('valid', hasNumber);
    document.getElementById('special-req').classList.toggle('valid', hasSpecial);
    document.getElementById('match-req').classList.toggle('valid', passwordsMatch);
    
    // Update confirm password input styling
    if (confirmPassword) {
        document.getElementById('confirm-password').classList.toggle('input-error', !passwordsMatch);
        document.getElementById('confirm-password').classList.toggle('input-success', passwordsMatch);
    }
    
    // Enable/disable signup button
    const signupBtn = document.getElementById('signup-btn');
    signupBtn.disabled = !(hasLength && hasUppercase && hasLowercase && hasNumber && hasSpecial && passwordsMatch && isEmailValid);
}

// Sign in function
async function signIn() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const signInBtn = document.getElementById('login-btn');
    
    if (!email || !password) {
        showToast('Please enter both email and password', 'error');
        return;
    }

    signInBtn.disabled = true;
    signInBtn.innerHTML = '<span class="loading"></span>Signing in...';
    
    try {
        await auth.signInWithEmailAndPassword(email, password);
    } catch (error) {
        let errorMessage = 'Error signing in';
        
        // Provide more user-friendly error messages
        if (error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
            errorMessage = 'Invalid email or password';
        } else if (error.code === 'auth/too-many-requests') {
            errorMessage = 'Too many failed login attempts. Please try again later.';
        } else if (error.code === 'auth/user-disabled') {
            errorMessage = 'This account has been disabled. Please contact support.';
        } else {
            errorMessage = error.message;
        }
        
        showToast(errorMessage, 'error');
    } finally {
        signInBtn.disabled = false;
        signInBtn.textContent = 'Sign In';
    }
}

// Sign up function
async function signUp() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const signupBtn = document.getElementById('signup-btn');
    
    if (!email || !password) {
        showToast('Please enter both email and password', 'error');
        return;
    }

    signupBtn.disabled = true;
    signupBtn.innerHTML = '<span class="loading"></span>Creating account...';
    
    try {
        const userCredential = await auth.createUserWithEmailAndPassword(email, password);
        await userCredential.user.sendEmailVerification();
        showToast('Account created successfully! Please check your email for verification.', 'success');
        showAuthForm('login');
    } catch (error) {
        let errorMessage = 'Error creating account';
        
        // Provide more user-friendly error messages
        if (error.code === 'auth/email-already-in-use') {
            errorMessage = 'This email is already registered. Please sign in or reset your password.';
        } else if (error.code === 'auth/invalid-email') {
            errorMessage = 'Please enter a valid email address.';
        } else if (error.code === 'auth/weak-password') {
            errorMessage = 'Please choose a stronger password.';
        } else {
            errorMessage = error.message;
        }
        
        showToast(errorMessage, 'error');
    } finally {
        signupBtn.disabled = false;
        signupBtn.textContent = 'Create Account';
    }
}

// Reset password function
async function resetPassword() {
    const email = document.getElementById('reset-email').value;
    const resetBtn = document.getElementById('reset-btn');
    
    if (!email) {
        showToast('Please enter your email', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showToast('Please enter a valid email address', 'error');
        return;
    }

    resetBtn.disabled = true;
    resetBtn.innerHTML = '<span class="loading"></span>Sending reset link...';
    
    try {
        await auth.sendPasswordResetEmail(email);
        showToast('Password reset link sent to your email', 'success');
        showAuthForm('login');
    } catch (error) {
        let errorMessage = 'Error sending reset link';
        
        // Provide more user-friendly error messages
        if (error.code === 'auth/user-not-found') {
            errorMessage = 'No account found with this email address.';
        } else if (error.code === 'auth/invalid-email') {
            errorMessage = 'Please enter a valid email address.';
        } else {
            errorMessage = error.message;
        }
        
        showToast(errorMessage, 'error');
    } finally {
        resetBtn.disabled = false;
        resetBtn.textContent = 'Send Reset Link';
    }
}

// Toggle password visibility
function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    const eyeIcon = event.currentTarget.querySelector('.eye-icon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.textContent = '👁️‍🗨️'; // Closed eye
    } else {
        passwordInput.type = 'password';
        eyeIcon.textContent = '👁️'; // Open eye
    }
}

// Initialize auth form validations
document.addEventListener('DOMContentLoaded', function() {
    setupLoginValidation();
    
    // Add input listeners for signup form
    const signupEmail = document.getElementById('signup-email');
    const signupPassword = document.getElementById('signup-password');
    const confirmPassword = document.getElementById('confirm-password');
    
    signupEmail.addEventListener('input', validatePassword);
    signupPassword.addEventListener('input', validatePassword);
    confirmPassword.addEventListener('input', validatePassword);
    
    // Add input listener for reset form
    const resetEmail = document.getElementById('reset-email');
    resetEmail.addEventListener('input', function() {
        const isValid = validateEmail(this.value);
        this.classList.toggle('input-error', this.value && !isValid);
        this.classList.toggle('input-success', this.value && isValid);
        document.getElementById('reset-btn').disabled = !isValid;
    });
}); 