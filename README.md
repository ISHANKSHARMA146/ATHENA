# Athena - Company & Job Description Manager

A web application that allows users to create company profiles and manage job descriptions using Firebase for authentication and Hasura for database operations.

## Features

- **User Authentication**: Email-based signup, login, password reset and verification
- **Company Profile Management**: Users can create and edit a single company profile
- **Job Description Management**: Add multiple job descriptions for your company
- **One Company Per User**: System enforces one company per user restriction
- **Multi-step User Flow**: Login → Create/Edit Company Profile → Manage Job Descriptions

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: FastAPI (Python)
- **Authentication**: Firebase Authentication
- **Database**: PostgreSQL via Hasura GraphQL
- **State Management**: LocalStorage for client-side persistence

## Detailed Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js and npm (for Firebase tools if needed)
- PostgreSQL database
- Hasura GraphQL Engine
- Firebase account

### Firebase Setup

1. **Create Firebase Project**:
   - Go to the [Firebase Console](https://console.firebase.google.com/)
   - Click "Add Project" and follow the setup wizard
   - Enable Google Analytics if desired

2. **Enable Authentication**:
   - In your project, navigate to "Authentication" in the left sidebar
   - Go to the "Sign-in method" tab
   - Enable "Email/Password" authentication
   - Enable "Email link" if you want passwordless login

3. **Create Web App**:
   - Click on the "Web" icon (</>) to create a web app
   - Register your app with a nickname (e.g., "Athena Web")
   - Copy the Firebase configuration (we'll use this later)

4. **Generate Service Account Key**:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `service-account.json` in the `firebase` folder

### Hasura Database Setup

1. **Set Up Hasura Instance**:
   - Use Hasura Cloud or set up locally with Docker
   - Connect to your PostgreSQL database
   - Set an admin secret for security

2. **Create Database Tables**:
   - Open Hasura Console
   - Go to the "SQL" tab
   - Run the following SQL script:

```sql
-- Create company_profiles table
CREATE TABLE public.company_profiles (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_id UNIQUE (user_id)
);

-- Create index on user_id
CREATE INDEX idx_company_profiles_user_id ON public.company_profiles (user_id);

-- Create job_descriptions table
CREATE TABLE public.job_descriptions (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES public.company_profiles (id) ON DELETE CASCADE
);

-- Create index on company_id
CREATE INDEX idx_job_descriptions_company_id ON public.job_descriptions (company_id);
```

3. **Track Tables in Hasura**:
   - Go to "Data" tab
   - Find "Untracked tables" and click "Track" for both tables
   
4. **Set Up Relationships**:
   - Go to the `job_descriptions` table
   - Navigate to the "Relationships" tab
   - Add an object relationship:
     - Name: `company`
     - Reference table: `company_profiles`
     - From: `company_id` → To: `id`
   
   - Go to the `company_profiles` table
   - Navigate to the "Relationships" tab
   - Add an array relationship:
     - Name: `job_descriptions`
     - Reference table: `job_descriptions`
     - From: `id` → To: `company_id`

### Environment Configuration

1. **Create .env File**:
   - Copy `.env.example` to `.env`
   - Fill in your Firebase and Hasura credentials:

```
# Firebase Backend Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_SERVICE_ACCOUNT=./firebase/service-account.json

# Firebase Frontend Configuration
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
FIREBASE_PROJECT=your-project-id
FIREBASE_STORAGE_BUCKET=your-project-id.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_MEASUREMENT_ID=your-measurement-id

# Hasura Configuration
HASURA_GRAPHQL_ENDPOINT=https://your-hasura-instance.hasura.app/v1/graphql
HASURA_ADMIN_SECRET=your-hasura-admin-secret

# Application Settings
ENVIRONMENT=development
APP_PORT=8000
```

### Backend Setup

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd athena
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Mac/Linux
   source env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Place Firebase Service Account**:
   - Save the Firebase service account JSON file in the `firebase` folder
   - Ensure the path matches the `.env` file setting

5. **Start the Server**:
   ```bash
   python main.py
   ```

## How the Code Works

### Architecture Overview

The application follows a simple architecture:

1. **Frontend (index.html)**:
   - Contains all UI components and JavaScript code
   - Handles user authentication via Firebase
   - Communicates with backend via fetch API

2. **Backend (FastAPI)**:
   - `main.py`: Entry point that sets up routes and serves the frontend
   - `routes/`: API endpoints for authentication, company, and job descriptions
   - `services/`: Business logic for interacting with Hasura
   - `config/`: Configuration settings

3. **Database (PostgreSQL via Hasura)**:
   - Two main tables: `company_profiles` and `job_descriptions`
   - Relationships between tables to link companies and their job descriptions

### Authentication Flow

1. User signs up or logs in via Firebase Authentication
2. Frontend receives Firebase user token
3. User ID from Firebase is used to identify the user in the database
4. Company profile is linked to Firebase user ID, ensuring one company per user

### User Workflows

#### New User Flow:
1. User signs up with email/password
2. User creates company profile (one-time action)
3. User is redirected to job descriptions page
4. User can add multiple job descriptions

#### Returning User Flow:
1. User logs in with email/password
2. System fetches existing company profile
3. User can edit company profile or manage job descriptions

## Testing the Application

### Step 1: Create a Test User

1. Open browser and navigate to `http://localhost:8000`
2. Click on the "Sign Up" tab
3. Enter email and a strong password
4. Complete the sign-up process
5. Verify your email if required

### Step 2: Create Company Profile

1. After login, you'll be directed to the company profile form
2. Fill in:
   - Company Name
   - Address
   - Description
3. Click "Create Company Profile"
4. You'll see a success message and be redirected to the job descriptions page

### Step 3: Add Job Descriptions

1. In the job descriptions page, fill in:
   - Job Title
   - Description
2. Click "Add Job Description"
3. The job will appear in the list above the form
4. Add more job descriptions as needed

### Step 4: Edit Company Profile

1. From the job descriptions page, click "Edit Company Profile"
2. Update any fields you wish to change
3. Click "Update Company Profile"
4. You'll see a success message

### Step 5: Testing Session Persistence

1. Close the browser and reopen it
2. Navigate to `http://localhost:8000`
3. Log in again
4. You should be directly taken to your job descriptions page
5. Your company profile and job descriptions should still be there

## Key Features and Limitations

### Features
- **Single Company Enforcement**: Users can create only one company profile
- **Multiple Job Descriptions**: Users can add unlimited job descriptions
- **Edit Mode**: Company profiles can be edited but not duplicated
- **Session Persistence**: Company data is stored in localStorage for page refreshes
- **Responsive Design**: Works on different screen sizes

### Limitations
- No job description editing (only creation)
- No image upload functionality
- No multi-user collaboration on company profiles

## Troubleshooting

### Common Issues

1. **Firebase Authentication Issues**:
   - Check that Firebase Authentication is enabled in Firebase Console
   - Verify the Firebase configuration in your `.env` file

2. **Hasura Connection Issues**:
   - Check that your Hasura endpoint is correct in `.env`
   - Verify the admin secret is correct
   - Ensure your database tables are properly created and tracked

3. **Backend Server Issues**:
   - Check Python version (3.7+ required)
   - Ensure all dependencies are installed
   - Verify the .env file is correctly formatted

## Future Enhancements

- Job description editing and deletion
- Company profile image upload
- User profile management
- Advanced search for job descriptions
- Email notifications for activities
- Analytics dashboard

## Security Considerations

- The `.env` file contains sensitive information, never commit it to version control
- The Firebase service account file contains private keys, keep it secure
- In production, restrict CORS settings to trusted domains 