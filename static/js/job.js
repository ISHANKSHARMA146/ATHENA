// Job Description related functions

// Show job form
function showJobForm() {
    document.getElementById('company-container').style.display = 'none';
    document.getElementById('job-container').style.display = 'block';
    
    // Display company name in job page
    const companyName = document.querySelector('#company-form [name="name"]').value;
    if (companyName) {
        document.getElementById('company-name-display').textContent = companyName;
    }
    
    // Load job descriptions when showing the job form
    loadCompanyJobs();
}

// Load company's job descriptions
async function loadCompanyJobs() {
    // Try to get companyId from window object or localStorage
    const companyId = window.currentCompanyId || localStorage.getItem('currentCompanyId');
    
    if (!companyId) {
        return;
    }
    
    const jobList = document.getElementById('job-list');
    jobList.innerHTML = '<p class="loading-jobs">Loading job descriptions...</p>';
    
    try {
        const response = await fetch(`/jd/company/${companyId}`);
        const data = await response.json();
        
        jobList.innerHTML = ''; // Clear loading message
        
        if (data.status === 'success') {
            window.currentCompanyId = companyId; // Ensure it's set in memory
            
            if (!data.data || data.data.length === 0) {
                jobList.innerHTML = '<p class="no-jobs">No job descriptions added yet.</p>';
                return;
            }
            
            data.data.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.className = 'job-item';
                
                // Create job title
                const title = document.createElement('h3');
                title.textContent = job.title;
                
                // Create job details section
                const details = document.createElement('div');
                details.className = 'job-details';
                
                // Add all non-null job properties to details
                for (const [key, value] of Object.entries(job)) {
                    if (value !== null && key !== 'id' && key !== 'company_id' && key !== 'title' && 
                        key !== 'created_at' && key !== 'updated_at') {
                        const detail = document.createElement('p');
                        const label = key.replace(/_/g, ' ');
                        detail.innerHTML = `<strong>${label.charAt(0).toUpperCase() + label.slice(1)}:</strong> ${value}`;
                        details.appendChild(detail);
                    }
                }
                
                // Append elements to job item
                jobElement.appendChild(title);
                jobElement.appendChild(details);
                jobList.appendChild(jobElement);
            });
        } else {
            jobList.innerHTML = '<p class="error">Error loading job descriptions</p>';
        }
    } catch (error) {
        console.error('Error loading job descriptions:', error);
        jobList.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

// Submit job function
async function submitJob() {
    // Try to get companyId from window object or localStorage
    const companyId = window.currentCompanyId || localStorage.getItem('currentCompanyId');
    
    if (!companyId) {
        alert('Please create a company profile first');
        showCompanyForm();
        return;
    }

    // Get the form data
    const form = document.getElementById('job-form');
    const formData = new FormData(form);
    const job = Object.fromEntries(formData.entries());
    
    // Add company ID to the job data
    job.company_id = parseInt(companyId);
    
    // Validate required fields
    if (!job.title) {
        showResponse('job-response', 'Please fill in the job title', 'error');
        return;
    }

    const submitJobBtn = document.getElementById('submit-job-btn');
    
    submitJobBtn.disabled = true;
    submitJobBtn.innerHTML = '<span class="loading"></span>Adding Job Description...';
    
    try {
        const response = await fetch('/jd/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(job)
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            showResponse('job-response', 'Job description added successfully!', 'success');
            
            // Clear form
            form.reset();
            
            // Reload job list
            loadCompanyJobs();
        } else {
            throw new Error(data.detail || 'Failed to add job description');
        }
    } catch (error) {
        showResponse('job-response', 'Error: ' + error.message, 'error');
    } finally {
        submitJobBtn.disabled = false;
        submitJobBtn.textContent = 'Add Job Description';
    }
} 