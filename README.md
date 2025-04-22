Node.js Web App Deployment Guide
This guide outlines the process for deploying a Node.js web application to Google Cloud Platform using Docker and Cloud Run. The deployment process includes building a Docker image, pushing it to Google Container Registry (GCR), and deploying it as a serverless container using Cloud Run.

Overview
Deploying your Node.js application on Google Cloud Platform leverages Docker for containerization and Cloud Run for managed, serverless container hosting. This approach streamlines scaling and reduces infrastructure management.

Prerequisites
Google Cloud SDK installed

Docker installed

A Google Cloud Platform account with billing enabled

A Node.js application with a properly configured Dockerfile

Required APIs
Ensure the following APIs are enabled in your GCP project:

Cloud Run API

Container Registry API

Artifact Registry API

Deployment Steps
1. Authentication and Project Setup
Authenticate with your Google Cloud account and set the project. Then configure Docker to use your GCP credentials:

bash
Sao chép
Chỉnh sửa
# Login to Google Cloud
gcloud auth login

# Set the GCP project
gcloud config set project alien-proton-389610

# Configure Docker to use GCP credentials
gcloud auth configure-docker
2. Build and Push Docker Image
Build your Docker image for the correct architecture and tag it for the Container Registry:

bash
Sao chép
Chỉnh sửa
# Build Docker image with proper architecture for Cloud Run (AMD64)
docker build --platform linux/amd64 -t nodejs-web-app .

# Tag the image for GCP Container Registry
docker tag nodejs-web-app gcr.io/alien-proton-389610/nodejs-web-app

# Push the image to Container Registry
docker push gcr.io/alien-proton-389610/nodejs-web-app
3. Deploy to Cloud Run
Deploy your application to Cloud Run:

bash
Sao chép
Chỉnh sửa
# Deploy the application to Cloud Run
gcloud run deploy nodejs-service \
  --image gcr.io/alien-proton-389610/nodejs-web-app \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated
Important Notes
Architecture flag:
The --platform linux/amd64 flag is crucial when building on ARM-based systems (like M1/M2 Macs) to ensure compatibility with Cloud Run.

Access settings:
The --allow-unauthenticated flag makes your service publicly accessible. Remove this flag if you want to restrict access.

Scalability:
Cloud Run automatically scales to zero when not in use, helping to minimize costs.

Accessing Your Application
After deployment completes, Cloud Run will provide a URL where your application is accessible. The URL will be in the following format:

bash
Sao chép
Chỉnh sửa
https://nodejs-service-[hash].run.app
Troubleshooting
Common Issues
403 Forbidden errors when pushing to GCR:

Ensure you’ve run gcloud auth configure-docker.

Verify that the correct project ID and permissions are set.

Container manifest errors:

Make sure to build with the --platform linux/amd64 flag.

Confirm that your Dockerfile is properly configured.

IAM Policy issues:

If your service isn’t publicly accessible despite using --allow-unauthenticated, run:

bash
Sao chép
Chỉnh sửa
gcloud beta run services add-iam-policy-binding \
  --region=asia-southeast1 \
  --member=allUsers \
  --role=roles/run.invoker \
  nodejs-service
Updating Your Application
To update your application:

Rebuild the Docker image.

Push the new image to GCR.

Redeploy using the same commands provided above.

Additional Resources
Cloud Run Documentation

Container Registry Documentation

Docker Documentation

This README provides a clear and concise guide for deploying your Node.js web app using Docker and Cloud Run on Google Cloud Platform. Adjust the project IDs, image tags, and region settings as needed for your environment.