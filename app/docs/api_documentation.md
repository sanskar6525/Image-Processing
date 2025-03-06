# 📌 Image Processing API Documentation

## 🏠 Base URL:
`http://localhost:8000/`

---

# 🚀 **1. API Endpoints**

## **1️⃣ Upload CSV (Start Image Processing)**
### **🔹 Endpoint:** `POST /upload/`
### **🔹 Description:** Upload a CSV file with product and image details.
### **🔹 Request:**
- **Headers:** `Content-Type: multipart/form-data`
- **Body:** `CSV file`

#### **Example Request (cURL)**
```bash
curl -X 'POST' 'http://localhost:8000/upload/' \
     -F 'file=@test.csv'
