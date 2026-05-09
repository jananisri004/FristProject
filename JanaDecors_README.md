# 🎉 JanaDecors — Event Decoration Booking Platform

A full stack event decoration booking platform built with Django and React.js. Users can browse decoration plans, search by event type, and filter by price. Admins manage users, bookings, and inventory through a dedicated admin panel.

**Live Demo → [frist-project-pw0i.onrender.com](https://frist-project-pw0i.onrender.com)**

---

## What It Does

**For users:**
- Browse decoration plans across categories: Music Events, Festivals, Birthdays
- Smart search and price filtering to find the right package
- Book a decoration plan and manage their booking

**For admins:**
- Full admin panel to manage users, bookings, and decor inventory
- Data-driven booking dashboards for tracking orders
- Backend validation via Django ORM to ensure data integrity

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django, Django ORM |
| Frontend | React.js, Bootstrap, HTML5, CSS3 |
| Database | SQLite |
| Auth | Django session-based authentication + OTP flow |
| Deployment | Render (Procfile + runtime.txt) |

---

## Key Features

- **Full stack architecture** — Django REST backend serving a React.js frontend
- **Admin panel** — complete inventory and booking management system
- **Smart search + price filter** — real-time filtering for end users
- **Django ORM validation** — backend data integrity on all booking operations
- **Deployed on Render** — live production environment with deployment pipeline

---

## Project Structure

```
FristProject/
├── Event/          # Core Django app: models, views, URLs for bookings & decor
├── EmailOTP/       # OTP authentication module
├── firstproject/   # Django project settings and root URLs
├── media/          # Uploaded images (decor photos)
├── Photo/          # Static photo assets
├── manage.py
├── requirements.txt
├── runtime.txt
└── procfile
```

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/jananisri004/FristProject.git
cd FristProject

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (for admin panel access)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

Open `http://localhost:8000` for the user app, `http://localhost:8000/admin` for the admin panel.

---

## About the Developer

Built by **Janani Sri S** — Python Full Stack Developer, B.Tech IT 2026, Erode, Tamil Nadu.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/jananisrisenthilkumar)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=flat&logo=netlify&logoColor=white)](https://jananisris-portfolio.netlify.app)
