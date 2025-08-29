# 👨‍🎓 Face Recognition Attendance System 📸 + ☁️ MongoDB  

This project is a **Face Recognition-based Attendance System** that uses:  
- **OpenCV** for video capture.  
- **face_recognition** library for detecting and recognizing faces.  
- **MongoDB Atlas (Cloud Database)** for storing attendance records securely.  

With this system, you can automatically mark student/employee attendance by recognizing their faces through a webcam, and the records will be saved in the cloud database in real-time.  

---

## 🚀 Features  

- ✅ Real-time face recognition using webcam.  
- ✅ Automatically records **date, time, and status (Present)** in **MongoDB Atlas**.  
- ✅ Prevents duplicate attendance within the same session.  
- ✅ Supports multiple registered users.  
- ✅ Easy integration with cloud for remote access.  

---

## 🛠️ Requirements  

Install dependencies before running the project:  

```bash
pip install opencv-python face-recognition pymongo
