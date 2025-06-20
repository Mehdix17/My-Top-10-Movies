# 🎬 My Top 10 Movies

A clean, modern Flask web app to manage your personal list of top 10 favorite movies.  
You can add, edit, delete and rank movies, as well as include ratings, reviews, and poster images.

<br/>

## 🧰 Tech Stack

- 🐍 Python 3
- 🧪 Flask & Flask-Bootstrap 5
- 🗃️ SQLite (with SQLAlchemy ORM)
- 🎨 Jinja2 templating
- ✍️ WTForms for secure form handling
- 📦 dotenv for config management

<br/>

## 🚀 Features

- 📌 Add movies by title
- ✏️ Edit details like rating, review, and ranking
- 🔥 Auto-sort by ranking (from 1 to 10)
- 🖼 Upload poster image via URL
- 🗑 Delete movies from the list
- 💾 Persistent database with SQLAlchemy

<br/>

## 📁 Project Structure

├── main.py \
├── .env \
├── static/ \
│ └── img/ \
├── templates/ \
│ ├── index.html \
│ ├── edit.html \
│ └── add.html \
├── requirements.txt \
└── README.md

<br/>

## 🛠 2. Create and activate a virtual environment (recommended)

python -m venv venv \
source venv/bin/activate  # On Windows: venv\Scripts\activate

<br/>

## 📦 3. Install dependencies

pip install -r requirements.txt

<br/>

## 🔐 4. Add a .env file with:

SECRET_KEY=your_secret_key \
DATABASE_URI=sqlite:///movies.db

<br/>

## ▶️ 5. Run the app

python main.py \
Then go to http://127.0.0.1:5000 in your browser.
