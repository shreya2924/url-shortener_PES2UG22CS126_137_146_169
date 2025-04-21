# url-shortener_PES2UG22CS126_137_146_169
# 🚀 Load-Balanced URL Shortener (Cloud Computing Mini Project)

This project is a scalable, containerized **URL Shortener** service built using **Flask**, Docker, and deployed using **Kubernetes**. It demonstrates core concepts of cloud computing like containerization, orchestration, NodePort and Ingress service exposure, and horizontal scaling.

> 📚 Part of UE22CS351B – Cloud Computing, Semester 6 (2025)

---

## 📌 Project Overview

<details>
<summary>Click to expand</summary>

Users can submit a long URL and receive a shortened version in return. This shortened link can then redirect users to the original URL. The system ensures **load balancing**, **scalability**, and **fault tolerance** using Kubernetes and Docker.

### 🧠 Key Features

- Simple frontend to accept URLs and display shortened links.
- Short UUID-based key generation.
- In-memory key-value storage (dictionary; can be extended to Redis/DB).
- Dockerized Flask app.
- Kubernetes deployment with:
  - Multiple replicas
  - ConfigMap for environment management
  - NodePort and Ingress for external access
- Horizontal scaling using replica sets.

</details>

---

## 🛠️ Tech Stack




| Component         | Technology          |
|------------------|---------------------|
| Backend API      | Python Flask        |
| URL Shortener ID | `shortuuid`         |
| Containerization | Docker              |
| Orchestration    | Kubernetes (kubectl)|
| Load Balancer    | NodePort & Ingress  |
| Env Mgmt         | ConfigMap           |



---

## 📂 Project Structure
.  
├── app.py                          # Flask application  
├── Dockerfile                     # Docker config for the app  
├── requirements.txt               # Python dependencies  
├── url-shortener-configmap.yaml  # Kubernetes ConfigMap  
├── url-shortener-deployment.yaml # Kubernetes Deployment  
├── url-shortener-service.yaml    # Kubernetes Service (NodePort)  
└── Project_1 - Load_Balanced_URL_Shortener.pdf # Project Brief  

## 🐳 Docker Instructions
<details>
### 1️⃣ Build Docker Image
docker build -t url-shortener .
### 2️⃣ Run Docker Container Locally
docker run -p 8080:8080 url-shortener
</details>

## ☸️ Kubernetes Instructions
<details>
### ⚠️ Ensure Docker Desktop or Minikube is running and kubectl is configured.
### 1️⃣ Apply ConfigMap
kubectl apply -f url-shortener-configmap.yaml
### 2️⃣ Deploy Application
kubectl apply -f url-shortener-deployment.yaml
### 3️⃣ Expose Service via NodePort
kubectl apply -f url-shortener-service.yaml
### 4️⃣ Access the App
Open your browser at:  
http://<NodeIP>:30080  
If using Minikube, get the IP using:  
minikube ip
</details>

## 📈 Scaling the App
<details>
You can manually scale the app or use HPA.

### Manual Scaling:  
kubectl scale deployment url-shortener --replicas=5   
### Autoscaling via HPA
kubectl autoscale deployment url-shortener --cpu-percent=50 --min=2 --max=10  
</details>
## 🔍 Monitoring & Logs
<details>  
kubectl get pods  
kubectl logs <pod-name>
</details>
## 🧪 Testing
<details>
### ✅ Manual Testing
Open the UI in browser (NodePort or Ingress URL).  

Enter a long URL (e.g., https://example.com).  

Click Shorten.  

Copy the shortened URL.  

Paste in browser → It should redirect to original URL.  

Try with non-existent short links → Should show 404-style page.  

### 🧪 API Testing (Optional)
Use curl or Postman:  
curl -X POST http://<host>:<port>/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
     
### 💣 Load/Stress Testing
Use Apache Benchmark:  
ab -n 1000 -c 10 http://<host>:<port>/  
Or use locust for interactive load testing.

</details>
## 📥 Dependencies
<details> 
From requirements.txt:  


flask  
shortuuid  
Install locally:  
pip install -r requirements.txt 
</details>
