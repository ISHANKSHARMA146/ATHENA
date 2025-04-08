// Authentication related functions

// Show auth form
function showAuthForm(formType) {
    // Hide all forms
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Show selected form
    document.getElementById(`${formType}-form`).classList.add('active');
    
    // Update tabs
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    if (formType === 'login' || formType === 'signup') {
        document.querySelector(`.auth-tab:nth-child(${formType === 'login' ? 1 : 2})`).classList.add('active');
    }
}

// Validate password requirements
function validatePassword() {
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
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
    
    // Enable/disable signup button
    const signupBtn = document.getElementById('signup-btn');
    signupBtn.disabled = !(hasLength && hasUppercase && hasLowercase && hasNumber && hasSpecial && passwordsMatch);
}

// Sign in function
async function signIn() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const signInBtn = document.getElementById('login-btn');
    
    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }

    signInBtn.disabled = true;
    signInBtn.innerHTML = '<span class="loading"></span>Signing in...';
    
    try {
        await auth.signInWithEmailAndPassword(email, password);
    } catch (error) {
        alert('Error signing in: ' + error.message);
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
        alert('Please enter both email and password');
        return;
    }

    signupBtn.disabled = true;
    signupBtn.innerHTML = '<span class="loading"></span>Creating account...';
    
    try {
        const userCredential = await auth.createUserWithEmailAndPassword(email, password);
        await userCredential.user.sendEmailVerification();
        alert('Account created successfully! Please check your email for verification.');
        showAuthForm('login');
    } catch (error) {
        alert('Error creating account: ' + error.message);
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
        alert('Please enter your email');
        return;
    }

    resetBtn.disabled = true;
    resetBtn.innerHTML = '<span class="loading"></span>Sending reset link...';
    
    try {
        await auth.sendPasswordResetEmail(email);
        alert('Password reset link sent to your email');
        showAuthForm('login');
    } catch (error) {
        alert('Error sending reset link: ' + error.message);
    } finally {
        resetBtn.disabled = false;
        resetBtn.textContent = 'Send Reset Link';
    }
} 