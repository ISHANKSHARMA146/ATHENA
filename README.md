# ATHENA AI - Job Description Processing System

ATHENA AI is a FastAPI application that allows users to upload, extract, and enhance job descriptions using AI.

## Features

- Upload job descriptions in PDF, DOCX, or image formats
- AI-powered extraction of key information from job descriptions
- Enhancement of job descriptions with detailed role information
- Integration with Firebase for authentication and storage
- Responsive web interface with modern components

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_AUTH_DOMAIN=your_domain.firebaseapp.com
   FIREBASE_PROJECT=your_project_id
   FIREBASE_STORAGE_BUCKET=your_bucket.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   FIREBASE_APP_ID=your_app_id
   FIREBASE_MEASUREMENT_ID=your_measurement_id
   ```

3. Run the development server:
   ```bash
   python main.py
   ```

## Vercel Deployment

This application is configured for deployment on Vercel's serverless platform.

### Environment Variables for Vercel

Configure the following environment variables in your Vercel project settings:

- `OPENAI_API_KEY` - Your OpenAI API key
- `FIREBASE_PROJECT_ID` - Your Firebase project ID
- `FIREBASE_API_KEY` - Your Firebase API key
- `FIREBASE_AUTH_DOMAIN` - Your Firebase auth domain
- `FIREBASE_PROJECT` - Your Firebase project ID
- `FIREBASE_STORAGE_BUCKET` - Your Firebase storage bucket
- `FIREBASE_MESSAGING_SENDER_ID` - Your Firebase messaging sender ID
- `FIREBASE_APP_ID` - Your Firebase app ID
- `FIREBASE_MEASUREMENT_ID` - Your Firebase measurement ID
- `FIREBASE_SERVICE_ACCOUNT_JSON` - The contents of your Firebase service account JSON file

### Deployment Steps

1. Connect your repository to Vercel
2. Configure the environment variables listed above
3. Deploy! Vercel will automatically use the configuration in `vercel.json`

### Vercel Limitations

Note the following limitations when running on Vercel:

1. DOC file processing is not supported in the serverless environment (DOCX and PDF are supported)
2. OCR for images is not available (users are prompted to convert to PDF/DOCX)
3. File logging is disabled in production - logs go to Vercel's log system
4. Serverless functions are limited to 10 seconds execution time and 1GB memory

## Project Structure

- `api/` - Vercel serverless function entry point
- `templates/` - HTML templates for the web interface
- `static/` - Static assets (CSS, JavaScript, images)
- `routes/` - API routes for different features
- `services/` - Service classes for business logic
- `utils/` - Utility functions
- `models/` - Data models and schemas 