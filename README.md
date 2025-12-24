# OC Project 9: LITReview

This project is carried out as part of the OpenClassrooms training program. 
LITReview is a website where users can request and publish reviews about books and articles.
Users can interact through tickets, reviews, and subscriptions to build a personalized review feed.

## Tech stack
- Python 3.10+
- Django
- HTML
- CSS

## Features
- Authentication:
    - User signup
    - User login
- Posts:
    - Create tickets to request reviews
    - Write reviews in response to tickets
    - Create a ticket and a review at the same time
    - Modify and delete tickets and reviews created by the current user
- Subscription:
    - Follow other users
    - View the list of users followed by the current user
    - View the list of users who follow the current user

## Installation
1. Clone the repository:
```bash
git clone https://github.com/anselmlys/OC_P9_LITReview.git
```

2. Move into the project directory, create and activate a virtual environment:
```bash
python -m venv env

# On Windows:
.\env\Scripts\activate

# On macOS / Linux:
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
  
> Note: A pre-populated SQLite database is included for demonstration purposes.
Running migrations is not required.
  
4. Move into "litreview" folder and run the development server:
```bash
python manage.py runserver
```

5. Website will be available at:  
http://127.0.0.1:8000/

## Demo accounts

This repository includes a pre-populated SQLite database (`db.sqlite3`) with demo users so the application can be tested immediately.

### Login
All demo users share the same password:

- Password: `S3cret!!`

Example usernames:
- `JaneDoe`
- `JoneDoe`
- `Unknown`

### Admin
- username: `admin`
- password: `S3cret!!`

> Note: These credentials are provided for evaluation/demo purposes only.

## Layout
The layout of this website is based on the following wireframe provided by OpenClassrooms:  
https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/Python%20FR/P7%20-%20D%C3%A9veloppez%20une%20application%20Web%20en%20utilisant%20Django/LITReview%20-%20Wireframes%20-%20FR.html

## Dependencies
- Python 3.10+
- See requirements.txt file

## Notes
This app is designed for educational purposes only.

## Author
Anselmlys
