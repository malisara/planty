# Planty 

Planty is an online marketplace web application where users can register and post plant ads. The project is my first non-tutorial Django application.

It was developed on Windows OS with Python 3.9.5

## Requirements:
- Python 3.0 or newer verison
- Python requirements are listed in the [requirements](requirements.txt) file

## Installation:
To run the project for the first time run the following:
```bash
# Clone the project
git clone https://github.com/malisara/planty.git

# Move into the 'planty' directory 
cd planty

# Create a virtual Python environment (make sure to use at least Python 3)
python -m venv <venv_name>

# Activate virtual environment
.\<venv_name>\Scripts\activate

# Install the requirements
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Run the local server
python manage.py runserver
```

## Features:
- Landing page with an overview of plant categories and a few most recently published ads. Non-logged-in users have an option to register or log in.
![Landing page](readme/landing_page.gif)

---

- Explore page where users can filter ads based on category, price, and date posted. There is also a basic text search functionality. Users can also sort ads in four different ways (based on price and date).
![Explore page](readme/explore.gif)

---

-  User reviews page, where visitors can write a new review or edit an existing one.
![Reviews page](readme/reviews.gif)

---

- Messages page where users can view all their chats. They can also open a specific chat, and reply to messages from others.
![Messages page](readme/messages.gif)

---

- Registration and login page. Users can register with a username, email, and password.

- CRUD operations for plant ads. Users can create new ads, consisting of a title, price, image, and description. They can also edit or delete their ads.

- A profile page that shows all user's ads, basic information, and their reviews. Users can change their profile image, username, email, and first and last name.

## Technologies I used:
- Django ORM
- Django signals
- Django context processors
- Django class-based views
- Django messages
- Django auth
- Pillow image library
- Javascript

## Future work:
- Reset password functionality
- Improve search capabilities
- Add unit tests
