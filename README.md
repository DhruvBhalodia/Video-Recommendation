# 🎬 Video Recommendation System 🎯  

An AI-powered video recommendation system that suggests videos based on user preferences, watch history, and content similarity. Built using **React.js, Node.js/Spring Boot, Python (ML), and MongoDB/MySQL**.

---

## 🚀 Features  
✅ Personalized video recommendations using ML 🤖  
✅ User authentication & watch history tracking 🔐  
✅ Interactive UI with **React.js + Tailwind CSS** 🎨  
✅ RESTful APIs with **Node.js/Express** ⚡  
✅ **Microservices-based architecture** (Backend & ML Recommendation Engine)  

---

## 🏗️ Tech Stack  
### **Frontend:**  
- React.js, Tailwind CSS  

### **Backend:**  
- Node.js + Express 
- MongoDB / MySQL (Database)  

### **Machine Learning Microservice:**  
- Python (Flask/FastAPI)  
- Pandas, NumPy, Scikit-learn, TensorFlow  

---

## 🔧 Installation & Setup  

### 1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-username/video-recommendation-app.git
cd video-recommendation-app
```

### 2️⃣ **Backend Setup**  
```bash
cd backend
npm install
```

### 3️⃣ **Frontend Setup**  
```bash
cd frontend
npm install
npm start
```

### 4️⃣ **ML Recommendation Service Setup**  
```bash
cd ml-service
pip install -r requirements.txt
python app.py
```

---

## 📜 API Endpoints  

### **1️⃣ Backend (Node.js/Spring Boot)**  
| Endpoint               | Method | Description |
|------------------------|--------|-------------|
| `/signup`             | POST   | Register a new user |
| `/login`              | POST   | Authenticate user |
| `/videos`             | GET    | Fetch all videos |
| `/recommendations/:userId` | GET | Fetch personalized recommendations |

### **2️⃣ ML Microservice (Python)**  
| Endpoint               | Method | Description |
|------------------------|--------|-------------|
| `/recommend`          | POST   | Generates video recommendations |

---

## 📜 License  
This project is licensed under the **MIT License**.  

---
