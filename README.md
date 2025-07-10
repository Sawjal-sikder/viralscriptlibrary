# Basketball Project Setup Guide

Welcome to the Basketball project! This guide will help you set up the project on any device (Windows, macOS, or Linux).

---

##  Prerequisites

Make sure you have the following installed:

- [Python 3.10.11](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)

---

## 🧱 Setup Instructions

### 1. Clone the Repository

``` 
git clone https://github.com/Sawjal-sikder/basketball.git
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
cd basketball
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
