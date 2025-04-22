Detailed Guide: Running Node.js Application on GCP VM with Docker and BigQuery
Objectives
Create a Virtual Machine (VM) on Google Cloud Platform
Deploy a Node.js application in a Docker container on the VM
Integrate the application with BigQuery for data querying
Part 1: Environment Setup
1. Create a VM on GCP
# Create VM with Container-Optimized OS (Docker pre-installed)
gcloud compute instances create nodejs-docker-vm \
  --zone=asia-southeast1-a \
  --machine-type=e2-medium \
  --image-family=cos-stable \
  --image-project=cos-cloud \
  --tags=http-server \
  --scopes=cloud-platform
Copy
2. Create firewall rule to allow HTTP/HTTPS
# Open port 8080 for web application
gcloud compute firewall-rules create allow-nodejs-app \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8080 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server
Copy
3. SSH into the VM
gcloud compute ssh nodejs-docker-vm --zone=asia-southeast1-a
Copy
Part 2: Create Node.js Application on the VM
1. Create project directory
# Navigate to home directory and create project folder
mkdir -p ~/nodejs-bigquery-app
cd ~/nodejs-bigquery-app
Copy
2. Create package.json file
cat > package.json << 'EOF'
{
  "name": "nodejs-bigquery-app",
  "version": "1.0.0",
  "description": "Node.js app with BigQuery integration",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "@google-cloud/bigquery": "^7.3.0"
  }
}
EOF
Copy
3. Create app.js file
cat > app.js << 'EOF'
const express = require('express');
const {BigQuery} = require('@google-cloud/bigquery');

const app = express();
const port = process.env.PORT || 8080;

// Initialize BigQuery client - using Default Application Credentials
const bigquery = new BigQuery();

// Main endpoint
app.get('/', (req, res) => {
  res.send('Hello from Docker on GCP VM! Try /query to run a BigQuery query.');
});

// Endpoint for BigQuery queries
app.get('/query', async (req, res) => {
  try {
    const query = `
      SELECT name, count
      FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
      WHERE state = 'TX'
      ORDER BY count DESC
      LIMIT 10
    `;
    
    console.log('Executing query...');
    const [rows] = await bigquery.query({query});
    
    console.log('Query results:', rows);
    res.json({
      message: 'Top 10 most popular names in Texas',
      data: rows
    });
  } catch (error) {
    console.error('Query error:', error);
    res.status(500).json({
      error: 'BigQuery query failed',
      details: error.message
    });
  }
});

// Start server
app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
EOF
Copy
4. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-slim

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Start application
CMD ["node", "app.js"]
EOF
Copy
Part 3: Build and Run Docker Container
1. Build Docker image
# In the directory containing Dockerfile
docker build -t nodejs-bigquery-app .
Copy
2. Run container
# Run container with port forwarding and privileged access to use Google Cloud credentials
docker run -d \
  -p 8080:8080 \
  --name nodejs-app \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --volume /tmp:/tmp \
  --volume /home/chronos/.config:/root/.config \
  nodejs-bigquery-app
Copy
Part 4: Test the Application
1. Get VM’s IP address
# On the VM
EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
echo "Application has been deployed at: http://$EXTERNAL_IP:8080"
Copy
2. Check endpoints
Access http://<EXTERNAL_IP>:8080 to check the homepage
Access http://<EXTERNAL_IP>:8080/query to execute BigQuery query
Part 5: Troubleshooting and Debugging
Check container logs
# View logs directly
docker logs nodejs-app

# View logs continuously
docker logs -f nodejs-app
Copy
Check running containers
docker ps
Copy
Enter the container for debugging
docker exec -it nodejs-app /bin/bash
Copy
If you encounter BigQuery permission errors
If you experience errors when accessing BigQuery, ensure the VM has sufficient permissions:

# Stop and remove the old container
docker stop nodejs-app
docker rm nodejs-app

# Add BigQuery access permissions to VM
gcloud compute instances set-scopes nodejs-docker-vm \
  --scopes=https://www.googleapis.com/auth/bigquery \
  --zone=asia-southeast1-a

# Restart the VM
gcloud compute instances stop nodejs-docker-vm --zone=asia-southeast1-a
gcloud compute instances start nodejs-docker-vm --zone=asia-southeast1-a

# Reconnect and run the container
gcloud compute ssh nodejs-docker-vm --zone=asia-southeast1-a
cd ~/nodejs-bigquery-app
docker run -d \
  -p 8080:8080 \
  --name nodejs-app \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --volume /tmp:/tmp \
  --volume /home/chronos/.config:/root/.config \
  nodejs-bigquery-app
Copy
Extension: Using the Application with Your Own Dataset
1. Create dataset and table in BigQuery
# Create dataset
bq --location=asia-southeast1 mk \
  --dataset \
  alien-proton-389610:nodejs_app_dataset

# Create table from CSV file (if available)
bq load \
  --source_format=CSV \
  alien-proton-389610:nodejs_app_dataset.sample_table \
  ./data.csv \
  name:STRING,value:INTEGER
Copy
2. Update the query in app.js
# Open editor to modify app.js
vi app.js

# Change the query in the /query endpoint
# const query = `
#   SELECT *
#   FROM \`alien-proton-389610.nodejs_app_dataset.sample_table\`
#   LIMIT 10
# `;
Copy
3. Rebuild image and run container
docker build -t nodejs-bigquery-app .
docker stop nodejs-app
docker rm nodejs-app
docker run -d \
  -p 8080:8080 \
  --name nodejs-app \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --volume /tmp:/tmp \
  --volume /home/chronos/.config:/root/.config \
  nodejs-bigquery-app
Copy
Important Notes
Access Permissions: The VM must have BigQuery access. When creating the VM, --scopes=cloud-platform provides full access.

Container-Optimized OS: This is a Linux image optimized for running containers, with Docker pre-installed.

Application Default Credentials: The container will use the VM’s credentials to access BigQuery.

BigQuery Costs: Note that BigQuery queries may incur costs depending on the amount of data processed.

Secure Deployment: In a production environment, you should use HTTPS and add appropriate security measures.

Do you need specific guidance on any part of this process?