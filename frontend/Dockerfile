# Stage 1: Build the React application
FROM node:20-alpine as builder

# Set up the directory structure to mimic the local environment
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./frontend/
COPY ai_agent/ ./ai_agent/
COPY frontend/ ./frontend/

# Set the working directory for the build
WORKDIR /app/frontend

# Install dependencies
RUN npm install

# Build the application
# This will now find ../ai_agent/ because the WORKDIR is /app/frontend
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the build output from the builder stage
# The output is in /app/frontend/dist
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Copy the README file to be served
COPY README.md /usr/share/nginx/html/

# Copy the custom Nginx configuration
# This path is relative to the build context (the project root)
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]