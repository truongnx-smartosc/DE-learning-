Node.js Web App Deployment Guide
Overview
This guide outlines the process for deploying a Node.js web application to Google Cloud Platform using Docker and Cloud Run. The deployment process includes building a Docker image, pushing it to Google Container Registry (GCR), and deploying it as a serverless container using Cloud Run.

Prerequisites
Google Cloud SDK installed
Docker installed
A Google Cloud Platform account with billing enabled
A Node.js application with a properly configured Dockerfile
Required APIs
Make sure the following APIs are enabled in your GCP project:

Cloud Run API
Container Registry API
Artifact Registry API
Deployment Steps
1. Authentication and Project Setup
# Login to Google Cloud
gcloud auth login

# Set the GCP project
gcloud config set project alien-proton-389610

# Configure Docker to use GCP credentials
gcloud auth configure-docker
Copy
2. Build and Push Docker Image
# Build Docker image with proper architecture for Cloud Run (AMD64)
docker build --platform linux/amd64 -t nodejs-web-app .

# Tag the image for GCP Container Registry
docker tag nodejs-web-app gcr.io/alien-proton-389610/nodejs-web-app

# Push the image to Container Registry
docker push gcr.io/alien-proton-389610/nodejs-web-app
Copy
3. Deploy to Cloud Run
# Deploy the application to Cloud Run
gcloud run deploy nodejs-service \
  --image gcr.io/alien-proton-389610/nodejs-web-app \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated
Copy
Important Notes
The --platform linux/amd64 flag is crucial when building on ARM-based systems (like M1/M2 Macs) to ensure compatibility with Cloud Run.
The --allow-unauthenticated flag makes your service publicly accessible. Remove this if you want to restrict access.
Cloud Run automatically scales to zero when not in use, helping to minimize costs.
Accessing Your Application
After deployment completes, Cloud Run will provide a URL where your application is accessible. The URL will be in the format:

https://nodejs-service-[hash].run.app
Troubleshooting
Common Issues:
403 Forbidden errors when pushing to GCR

Ensure you’ve run gcloud auth configure-docker
Verify correct project ID and permissions
Container manifest errors

Make sure to build with --platform linux/amd64 flag
Verify Dockerfile is properly configured
IAM Policy issues

If your service isn’t publicly accessible despite using --allow-unauthenticated, run:
gcloud beta run services add-iam-policy-binding \
  --region=asia-southeast1 \
  --member=allUsers \
  --role=roles/run.invoker \
  nodejs-service
Copy
Updating Your Application
To update your application, simply rebuild the Docker image, push it to GCR, and redeploy using the same commands.

Additional Resources
Cloud Run Documentation
Container Registry Documentation
Docker Documentation