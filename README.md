# MyTask — Personal Task & Notes Manager (Flask)

A clean, modern, and secure productivity web app built using **Flask**, featuring **user authentication**, **tasks & notes management**, **profile photo upload**, **search functionality**, **light/dark theme**, and **SweetAlert2 UI**.

This project is perfect for **interview showcase**, **portfolio**, and **Flask backend learning**.

---

## 🚀 Live Demo  
(Add your deployed link here, e.g., Render, Railway, PythonAnywhere) 
https://github.com/programmer22-oss/Task_Manager/blob/main/Task_Manager%20demo.mp4
---

## ✨ Features

### 🔐 Authentication
- User Register / Login / Logout  
- Password hashing using Werkzeug  
- Session management using Flask-Login  

### 📝 Task Manager
- Add, Edit, Delete Tasks  
- User-specific tasks (isolated view)  
- Quick Add form (AJAX + SweetAlert Toast)

### 📒 Notes Manager
- Add, Edit, Delete Notes  
- Styled list view  
- Secure CRUD for each user

### 👤 Profile Page
- Update username  
- Change password  
- Upload profile picture  
- Auto-update DP in navbar  
- Old image auto-delete  

### 🌗 Light / Dark Mode
- LocalStorage-based theme system  
- Smooth UI switching  

### 🔍 Global Search
- Search Tasks + Notes  
- Partial match  
- Case-insensitive  
- Clean results UI  

### 🎨 Modern UI
- Custom CSS with theme variables  
- Responsive Navbar  
- SweetAlert2 for confirm + success  
- Profile cards with animations  
- Sticky top navbar

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Flask**
- **Flask-Login**
- **Flask-SQLAlchemy**
- **Werkzeug**
- **SweetAlert2**
- **HTML / CSS / JavaScript**
- **SQLite (Local)**  
  *(Easy switch to MySQL/PostgreSQL)*

---

## 📂 Project Structure

  task_manager/
  ├── app.py
  ├── requirements.txt
  ├── Procfile
  ├── LICENSE
  ├── .gitignore
  ├── templates/
  │ ├── base.html
  │ ├── index.html
  │ ├── tasks.html
  │ ├── notes.html
  │ ├── search.html
  │ ├── profile.html
  │ └── parts/
  │ ├── header.html
  │ └── footer.html
  └── static/
  ├── css/style.css
  ├── js/script.js
  └── profile_pics/




---

## 🧰 Installation (Local Setup)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/mytask.git
cd mytask
2. Create Virtual Environment
bash
Copy code
python -m venv venv
3. Activate Environment
Windows:

bash
Copy code
venv\Scripts\activate
Mac/Linux:

bash
Copy code
source venv/bin/activate
4. Install Dependencies
bash
Copy code
pip install -r requirements.txt
5. Run App
bash
Copy code
python app.py
6. Open in Browser
cpp
Copy code
http://127.0.0.1:5000/
🔑 Environment Variables (Optional)
Create .env file:

ini
Copy code
SECRET_KEY=your_secret_key
Use inside app.py:

python
Copy code
app.secret_key = os.environ.get("SECRET_KEY", "default_key")
🌍 Deployment (Render / Railway / PythonAnywhere)
Render Steps:
Add repo

Build command: pip install -r requirements.txt

Start command: gunicorn app:app

Add environment variable: SECRET_KEY

Heroku:
makefile
Copy code
web: gunicorn app:app
🧪 Future Improvements (Optional Roadmap)
Search suggestions (AJAX)

Task categories / labels

Pagination

Export tasks to CSV / PDF

Admin panel

🤝 Contributing
Pull requests are welcome. Suggestions are appreciated.
