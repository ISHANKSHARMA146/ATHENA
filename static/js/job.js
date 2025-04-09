// Job Description related functions

// Global variables for file upload
let selectedFile = null;

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
    
    // Load JD upload component if not already loaded
    const uploadContainer = document.getElementById('jd-upload-container');
    if (!uploadContainer) {
        fetch('/components/job/jd-upload.html')
            .then(response => response.text())
            .then(html => {
                // Create a container for the upload component
                const uploadDiv = document.createElement('div');
                uploadDiv.id = 'jd-upload-container';
                uploadDiv.innerHTML = html;
                
                // Insert before the job form
                const jobFormContainer = document.getElementById('job-form-container');
                jobFormContainer.parentNode.insertBefore(uploadDiv, jobFormContainer);
            });
    }
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

// JD Upload Functions
function triggerFileInput() {
    document.getElementById('jd-file-input').click();
}

function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('upload-box').classList.add('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('upload-box').classList.remove('drag-over');
    
    if (event.dataTransfer.files.length) {
        const file = event.dataTransfer.files[0];
        processSelectedFile(file);
    }
}

function handleFileSelect(event) {
    if (event.target.files.length) {
        const file = event.target.files[0];
        processSelectedFile(file);
    }
}

function processSelectedFile(file) {
    // Check file type
    const validTypes = [
        'application/pdf', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword',
        'image/jpeg',
        'image/png'
    ];
    
    if (!validTypes.includes(file.type)) {
        alert('Invalid file type. Please upload PDF, DOCX, DOC, JPG, or PNG files.');
        return;
    }
    
    // Check file size (max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (file.size > maxSize) {
        alert('File is too large. Maximum size is 5MB.');
        return;
    }
    
    // Store file in global variable
    selectedFile = file;
    
    // Update UI
    document.getElementById('file-name').textContent = file.name;
    document.getElementById('file-size').textContent = formatFileSize(file.size);
    document.getElementById('file-info').style.display = 'flex';
    document.getElementById('upload-jd-btn').disabled = false;
    
    // Hide previous results if any
    document.getElementById('processing-results').style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
}

function removeFile() {
    selectedFile = null;
    document.getElementById('jd-file-input').value = '';
    document.getElementById('file-info').style.display = 'none';
    document.getElementById('upload-jd-btn').disabled = true;
}

async function uploadJobDescription() {
    if (!selectedFile) {
        alert('Please select a file to upload');
        return;
    }
    
    // Disable upload button and show progress
    const uploadBtn = document.getElementById('upload-jd-btn');
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Processing...';
    
    const uploadProgress = document.getElementById('upload-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressStatus = document.getElementById('progress-status');
    
    uploadProgress.style.display = 'block';
    progressFill.style.width = '10%';
    progressStatus.textContent = 'Uploading file...';
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Extract stage
        progressFill.style.width = '30%';
        progressStatus.textContent = 'Extracting information...';
        
        const extractResponse = await fetch('/jd/extract', {
            method: 'POST',
            body: formData
        });
        
        const extractData = await extractResponse.json();
        if (extractData.status !== 'success') {
            throw new Error(extractData.detail || 'Failed to extract job description');
        }
        
        // Enhancement stage
        progressFill.style.width = '70%';
        progressStatus.textContent = 'Enhancing job description...';
        
        const enhanceResponse = await fetch('/jd/enhance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(extractData.data)
        });
        
        const enhanceData = await enhanceResponse.json();
        if (enhanceData.status !== 'success') {
            throw new Error(enhanceData.detail || 'Failed to enhance job description');
        }
        
        // Display results
        progressFill.style.width = '100%';
        progressStatus.textContent = 'Completed';
        
        // Store the enhanced data for later use
        window.enhancedJobData = enhanceData.data;
        
        // Display the extracted data
        displayExtractedData(enhanceData.data);
        
    } catch (error) {
        console.error('Error processing job description:', error);
        progressStatus.textContent = 'Error: ' + error.message;
        progressFill.style.backgroundColor = '#ff4d4d';
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload & Process';
    }
}

function displayExtractedData(data) {
    const extractedDataContainer = document.getElementById('extracted-data');
    const processingResults = document.getElementById('processing-results');
    
    // Format the data for display
    let html = '';
    
    // Enhanced JD data
    const enhancedJd = data.enhanced_jd;
    html += `<h4>Job Title: ${enhancedJd.job_title}</h4>`;
    html += `<p><strong>Industry:</strong> ${enhancedJd.industry_name}</p>`;
    html += `<p><strong>Experience Required:</strong> ${enhancedJd.min_work_experience || 'Not specified'} years</p>`;
    
    html += '<h4>Role Summary:</h4>';
    html += `<p>${enhancedJd.role_summary}</p>`;
    
    html += '<h4>Responsibilities:</h4>';
    html += '<ul>';
    enhancedJd.responsibilities.slice(0, 5).forEach(resp => {
        html += `<li>${resp}</li>`;
    });
    if (enhancedJd.responsibilities.length > 5) {
        html += `<li>...and ${enhancedJd.responsibilities.length - 5} more</li>`;
    }
    html += '</ul>';
    
    html += '<h4>Required Skills:</h4>';
    html += '<ul>';
    enhancedJd.required_skills.slice(0, 5).forEach(skill => {
        html += `<li>${skill}</li>`;
    });
    if (enhancedJd.required_skills.length > 5) {
        html += `<li>...and ${enhancedJd.required_skills.length - 5} more</li>`;
    }
    html += '</ul>';
    
    // Update the UI
    extractedDataContainer.innerHTML = html;
    processingResults.style.display = 'block';
}

function useExtractedResults() {
    if (!window.enhancedJobData) {
        alert('No extracted data available');
        return;
    }
    
    // Get the job form data
    const formData = window.enhancedJobData.job_form_data;
    
    // Get the job form and fill it with the extracted data
    const form = document.getElementById('job-form');
    
    // For each field in the form, set the value if available in formData
    for (const input of form.elements) {
        if (input.name && formData[input.name] !== undefined) {
            if (input.tagName === 'TEXTAREA') {
                input.value = formData[input.name] || '';
            } else if (input.tagName === 'INPUT') {
                input.value = formData[input.name] || '';
            }
        }
    }
    
    // Hide the upload container and scroll to the form
    document.getElementById('jd-upload-container').style.display = 'none';
    document.getElementById('job-form-container').scrollIntoView({ behavior: 'smooth' });
    
    // Show success message
    showResponse('job-response', 'Job description data has been filled in the form. Review and submit when ready.', 'success');
}

function editExtractedResults() {
    if (!window.enhancedJobData) {
        alert('No extracted data available');
        return;
    }
    
    // Hide the upload container and show the form
    document.getElementById('jd-upload-container').style.display = 'none';
    
    // Pre-fill with basic data
    const formData = window.enhancedJobData.job_form_data;
    const form = document.getElementById('job-form');
    
    // Fill in just the title and summary to start
    const titleInput = form.querySelector('[name="title"]');
    if (titleInput) titleInput.value = formData.title || '';
    
    const summaryInput = form.querySelector('[name="job_summary"]');
    if (summaryInput) summaryInput.value = formData.job_summary || '';
    
    // Scroll to the form
    document.getElementById('job-form-container').scrollIntoView({ behavior: 'smooth' });
    
    // Show hint message
    showResponse('job-response', 'You can now manually edit the job description form.', 'info');
}

// Helper function to show/hide response messages
function showResponse(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = 'response ' + type;
    element.style.display = 'block';
    
    // Hide after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
} 