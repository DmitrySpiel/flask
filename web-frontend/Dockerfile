# Step 1: Use an Nginx base image
FROM --platform=linux/amd64 nginx:alpine 
# Step 2: Copy the static files (HTML, JS)
COPY . /usr/share/nginx/html

# Nginx automatically serves content from /usr/share/nginx/html