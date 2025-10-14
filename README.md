# 🧺 Urban Laundromat  
### A Laundry Pickup & Delivery Management System  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![REST%20API](https://img.shields.io/badge/REST-API-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🚀 Overview  

**Urban Laundromat** is a full-stack Django-based Laundry Pickup and Delivery Management System.  
It enables customers to request laundry services, track order progress, and receive real-time updates — all from a simple, elegant dashboard.  
Admins can update orders, send notifications, and manage users easily.

---

## 🧩 Tech Stack  

| Layer | Technology |
|-------|-------------|
| **Backend** | Django, Django REST Framework, SimpleJWT |
| **Frontend** | Django Templates (HTML, CSS, JS), Bootstrap 5, Axios |
| **Database** | SQLite (default) |
| **Deployment Ready** | Render / Vercel (Frontend), Railway / ElephantSQL (Backend) |

---

## 🏗️ Project Structure  

laundry/
├── api_urls.py  # API endpoints (register, login, orders, notifications)
├── frontend_urls.py  # Frontend routes (login, register, orders, home)
├── models.py  # User, Order, Notification models
├── serializers.py  # API data serializers
├── views.py  # API views logic (CRUD operations)

templates/
├── base.html # Shared base layout
├── index.html # Landing page
├── login.html # Login page (JWT auth)
├── register.html # Registration page
├── orders.html # Orders dashboard

---

## 🔐 Authentication Flow  

Implemented using **JWT (JSON Web Tokens)**  

| Endpoint | Purpose |
|-----------|----------|
| `POST /api/auth/register/` | Register a new user |
| `POST /api/auth/token/` | Login (returns access + refresh tokens) |
| `POST /api/auth/token/refresh/` | Refresh access token |

**Frontend Flow**
- Tokens stored securely in `localStorage`
- Redirects logged-in users directly to `/orders/`
- Blocks guests from accessing the dashboard
- Logout clears all tokens and session data

---

## ✨ Features Implemented  

### 🧱 Backend (API)
- Custom `User` model (Customer / Admin roles)  
- JWT authentication endpoints  
- CRUD for Orders and Notifications  
- Admin API to send notifications  
- Laundry order workflow: `Pending → Picked Up → Washing → Ironing → Delivered`

### 🎨 Frontend (UI)
- **`base.html`** for consistent layout  
- **Landing page:** Modern animated hero section  
- **Login & Register pages:** Glassmorphism design, smooth transitions  
- **Orders Dashboard:**
  - Fetches orders dynamically from API
  - Animated progress bars for order tracking
  - Refresh button for live updates
  - JWT access check & redirect protection

### 🔒 Access Control
| User Type | Access |
|------------|--------|
| Guest | Redirected to login |
| Logged-in | Full dashboard access |
| Logged-in user visiting login/register | Auto-redirected to `/orders/` |
| Logout | Clears tokens and returns to login |

## 🧾 How to Run Locally  

### 1️⃣ Clone Repository
git clone https://github.com/yourusername/urban-laundromat.git
cd urban-laundromat


2️⃣ Setup Virtual Environment
python -m venv venv
source venv/Scripts/activate  # Windows
# OR
source venv/bin/activate      # macOS/Linux


3️⃣ Install Dependencies
pip install -r requirements.txt


4️⃣ Run Migrations
python manage.py migrate


5️⃣ Start Development Server
python manage.py runserver 8000

6️⃣ Access the App
Component	URL
Frontend	http://127.0.0.1:8000/
API	http://127.0.0.1:8000/api/
