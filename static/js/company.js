// Company-related functions

// Show company form
function showCompanyForm() {
    document.getElementById('job-container').style.display = 'none';
    document.getElementById('company-container').style.display = 'block';
}

// Load user's company data
async function loadUserCompany(userId) {
    try {
        const response = await fetch(`/company/user/${userId}`);
        const data = await response.json();
        
        if (data.status === 'success' && data.data) {
            // Store company data
            window.currentCompanyId = data.data.id;
            localStorage.setItem('currentCompanyId', data.data.id);
            
            // Set form to edit mode
            document.getElementById('company-form-title').textContent = 'Edit Company Profile';
            
            // Update form fields with company data
            const form = document.getElementById('company-form');
            for (const key in data.data) {
                const input = form.querySelector(`[name="${key}"]`);
                if (input && data.data[key] !== null) {
                    input.value = data.data[key];
                }
            }
            
            document.getElementById('create-company-btn').textContent = 'Update Company Profile';
            document.getElementById('to-job-btn').style.display = 'block';
            
            // Update company name in job page
            document.getElementById('company-name-display').textContent = data.data.name;
            
            return true;
        } else {
            // Set form to create mode
            document.getElementById('company-form-title').textContent = 'Create Company Profile';
            
            // Clear form fields
            const form = document.getElementById('company-form');
            form.reset();
            
            document.getElementById('create-company-btn').textContent = 'Create Company Profile';
            document.getElementById('to-job-btn').style.display = 'none';
            
            return false;
        }
    } catch (error) {
        console.error('Error loading company data:', error);
        return false;
    }
}

// Create or update company profile
async function createOrUpdateCompany() {
    // Get the form data
    const form = document.getElementById('company-form');
    const formData = new FormData(form);
    const company = Object.fromEntries(formData.entries());
    
    // Validate required fields
    if (!company.name) {
        showResponse('company-response', 'Please fill in all required fields', 'error');
        return;
    }

    const responseDiv = document.getElementById('company-response');
    const companyBtn = document.getElementById('create-company-btn');
    const isUpdate = window.currentCompanyId ? true : false;
    
    companyBtn.disabled = true;
    companyBtn.innerHTML = `<span class="loading"></span>${isUpdate ? 'Updating' : 'Creating'} Company Profile...`;
    
    try {
        let url, method;
        
        if (isUpdate) {
            // Update existing company
            url = '/company/update';
            method = 'PUT';
            company.id = parseInt(window.currentCompanyId);
        } else {
            // Create new company
            url = '/company/create';
            method = 'POST';
            company.user_id = auth.currentUser.uid;
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(company)
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            showResponse('company-response', `Company profile ${isUpdate ? 'updated' : 'created'} successfully!`, 'success');
            
            // Store company ID for job descriptions
            window.currentCompanyId = data.data.id;
            localStorage.setItem('currentCompanyId', data.data.id);
            
            // Update UI to edit mode
            document.getElementById('company-form-title').textContent = 'Edit Company Profile';
            document.getElementById('create-company-btn').textContent = 'Update Company Profile';
            document.getElementById('to-job-btn').style.display = 'block';
            
            // Update company name in job page
            document.getElementById('company-name-display').textContent = company.name;
            
            // Show job form if it was a creation
            if (!isUpdate) {
                showJobForm();
            }
        } else {
            throw new Error(data.detail || `Failed to ${isUpdate ? 'update' : 'create'} company profile`);
        }
    } catch (error) {
        showResponse('company-response', 'Error: ' + error.message, 'error');
    } finally {
        companyBtn.disabled = false;
        companyBtn.textContent = isUpdate ? 'Update Company Profile' : 'Create Company Profile';
    }
}

// Show response message
function showResponse(elementId, message, type) {
    const responseDiv = document.getElementById(elementId);
    responseDiv.textContent = message;
    responseDiv.className = `response ${type}`;
} 