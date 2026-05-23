# 🚀 AI Resume Analyzer (Flask Project)

## 👩‍💻 Developed By:
**Name:** Muzdalfa  

---

## 📌 Project Overview
This is a web-based AI Resume Analyzer built using Flask. It allows users to register, login, upload their CVs, and get automated skill analysis. The system also includes an Admin panel for managing job postings using CRUD operations.

---

## ⚙️ Technologies Used
- Python  
- Flask  
- SQLite (SQLAlchemy)  
- Flask-Bcrypt  
- HTML, CSS  
- PDFPlumber (for CV text extraction)  

---

## 👤 User Roles

### 1. Normal User
- Register account  
- Login system  
- Upload CV (PDF)  
- View AI analysis result (skills found & missing)  

### 2. Admin User
- Login (username: admin, password: admin123)  
- Manage Jobs (Add / Update / Delete)  
- View all job postings  

---

## 🔑 Features
- Secure Login & Registration system  
- Role-based authentication (Admin/User)  
- CV upload and PDF text extraction  
- Skill-based CV analysis  
- Job CRUD system (Create, Read, Update, Delete)  
- Access control (Unauthorized users blocked)  

---

## 📊 How CV Analyzer Works
1. User uploads CV (PDF format)  
2. System extracts text using PDFPlumber  
3. Skills are matched (Python, Flask, SQL, HTML, CSS)  
4. Score is calculated based on matching skills  
5. Result shows:
   - Found Skills  
   - Missing Skills  
   - Final Score  

---

## 🔐 Admin Login Details
Username: admin
Password: admin123


---

## 📁 Project Structure
AI_Resume_Analyzer/
│
├── app.py
├── database.db
├── uploads/
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── index.html
│ ├── result.html
│ ├── admin.html
│ ├── access.html
│
├── static/
│ └── style.css
│
└── README.md

---

## 🎯 Conclusion
This project demonstrates a complete Flask-based web application with authentication, role-based access control, CRUD operations, and AI-based resume analysis system.

It is designed as a beginner-to-intermediate level final project for learning full-stack Python development.

---

## ✨ Thank You
