# url-shortener-k8s  
🚀 A FastAPI-based URL shortener microservice, containerized with Docker and deployed on Kubernetes. Simple, scalable, and lightning fast!

## 📌 Overview

This is a simple URL shortener application built using **Python**, **FastAPI**, **PostgreSQL**, **Docker**, and **Kubernetes**. The project demonstrates how to:

- Build a URL shortening service using FastAPI.
- Containerize the application using Docker.
- Deploy and manage the service with Kubernetes.

---

## 📚 Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Docker Setup](#docker-setup)
- [Kubernetes Setup](#kubernetes-setup)
- [Accessing the Application](#accessing-the-application)
- [Running Locally](#running-locally)

---

## 💻 Tech Stack

- **Backend**: FastAPI  
- **Database**: PostgreSQL  
- **Containerization**: Docker  
- **Orchestration**: Kubernetes  

---

## ✅ Prerequisites

Make sure you have the following tools installed:

- [Docker](https://www.docker.com/get-started)
- [Kubernetes (via Docker Desktop or Minikube)](https://kubernetes.io/docs/tasks/tools/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Postman](https://www.postman.com/) (optional, for API testing)

---

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/singh-admin/url-shortener-k8s.git
cd url-shortener-k8s
```

---

## 🐳 Docker Setup

### 2. Build the Docker Image

```bash
docker build -t your-dockerhub-username/url-shortener-app .
```

### 3. Run the Docker Container (Locally)

```bash
docker run -p 8000:8000 your-dockerhub-username/url-shortener-app
```

**📍 App will be accessible at:** `http://localhost:8000`

### 4. Push Docker Image to Docker Hub

```bash
docker push your-dockerhub-username/url-shortener-app
```

---

## ☸️ Kubernetes Setup

### 5. Apply PostgreSQL Deployment

```bash
kubectl apply -f postgres-deployment.yaml
```

### 6. Apply URL Shortener App Deployment

```bash
kubectl apply -f app-deployment.yaml
```

### 7. Apply Service Configuration

```bash
kubectl apply -f shortener-app-service.yaml
```

---

## 🌐 Accessing the Application

Once everything is deployed, find the NodePort to access the app:

```bash
kubectl get svc url-shortener-app
```

Use the NodePort (e.g. `http://localhost:30001`) to access your app in the browser.

---

## 🧪 Running Locally Without Kubernetes

If you prefer to test without Kubernetes:

1. Start PostgreSQL locally or use a service like [ElephantSQL](https://www.elephantsql.com/).
2. Update the `DATABASE_URL` in your `.env` or code.
3. Run the app:

```bash
uvicorn main:app --reload
```
