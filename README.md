# URL Shortener with FastAPI and SQLModel

This is a simple URL shortener application built with **FastAPI** and **SQLModel**.  
The idea came from my curiosity about how platforms like LinkedIn automatically convert posted links into shortened URLs (e.g., `https://lnkd.in/gZ9HZMqm`).  
I wanted to recreate this functionality to understand how it works—while challenging myself to step outside my comfort zone by using FastAPI instead of Django.

---

## 🚀 Features
- Shorten long URLs into compact, easy-to-share links.
- Redirect shortened links to their original destinations.
- Automatically generate random unique slugs.
- Store and retrieve URL mappings from a database.
- Built with **FastAPI** (for backend API) and **SQLModel** (for database ORM).

---

## 🛠 Tech Stack
- **Backend:** FastAPI
- **Database ORM:** SQLModel
- **Database:** SQLite (default, but easily swappable)
- **Language:** Python 3.9+

---

## 📂 Project Structure
project/

│

├── main.

├── models.py

├── requirements.txt

├── test_main.py

└── README.md

**Clone the repository**
```bash
git clone https://github.com/gamergbesh/url-shortener.git
cd url-shortener
```

1. Create virtual Environment
```bash 
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the fastapi server
```bash
uvicorn main:app --reload
```

# Usage

Shorten a URL:
Send a POST request to `/create` with JSON body:

```json
{
    "original_url": "https://example.com"
}
```

### Example 

```bash
POST http://127.0.0.1:8000/create
{
    "original_url": "https://github.com/tiangolo/fastapi"
}
```

#### Response
```json
{
    "original_url": "https://github.com/tiangolo/fastapi",
    "shortened_url": "http://127.0.0.1:8000/abc123"
}
```

Visiting http://127.0.0.1:8000/abc123 will redirect you to the FastAPI GitHub repo.

📖 Lessons Learned

* How URL shortening works under the hood.
* Creating database models and queries with SQLModel.
* Handling HTTP redirects in FastAPI.
* Building APIs outside of my comfort zone with Django.
