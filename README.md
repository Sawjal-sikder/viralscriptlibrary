# 🧠 Viral Scripts Library

Welcome to the **Viral Scripts Library** project!  
This is a Django-based web application where users can upload, manage, and explore viral scripts for various purposes.  
This guide will help you set up and run the project on your local machine.

---

## 📦 Prerequisites

Make sure you have the following installed on your system:

- [Python 3.10.11+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)

---

## ⚙️ Setup Instructions

Follow the steps below to run the project locally:

### 1. Clone the Repository

```bash
```
```[
git clone https://github.com/Sawjal-sikder/viralscriptlibrary
```

### 2. Create a Virtual Environment

For Windows:
```
python -m venv venv
venv\Scripts\activate

```
For macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```
Change Dir
```
cd viralscriptlibrary
```

### 3. Install Dependencies

```
pip install -r requirements.txt

```
### 4. Apply Migrations


```
python manage.py makemigrations
python manage.py migrate

```
### 5. Create a Superuser (Admin)


```
python manage.py createsuperuser

```
### 6. Run the Development Server


```
python manage.py runserver

```
