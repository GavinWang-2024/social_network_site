<img width="1509" alt="Screenshot 2024-08-06 at 10 03 37 AM" src="https://github.com/user-attachments/assets/045cd465-fe64-4fd1-9f89-edbc917e48a9">
<img width="1509" alt="Screenshot 2024-08-06 at 10 04 19 AM" src="https://github.com/user-attachments/assets/4b453eb0-fcec-4ea3-b52a-7f60e413f9a1">
<img width="1509" alt="Screenshot 2024-08-06 at 10 04 29 AM" src="https://github.com/user-attachments/assets/6ca03e90-b871-4bd8-9e49-c420a7a22d1a">
<img width="1509" alt="Screenshot 2024-08-06 at 10 04 37 AM" src="https://github.com/user-attachments/assets/3e077fad-0687-426f-8558-35a11d0bcacb">


# Social Network Site

This project is a basic social networking site.

## Features

- User authentication (sign up, login, logout)
- Profile management
- Posting status updates
- Liking posts
- Following users
- Basic user interface with HTML and CSS

## Technologies Used

- **Python**: Core programming language
- **Django**: Web framework used for the backend
- **HTML, CSS, Javascript**: Frontend development
- **SQLite**: Database for storing user data and posts

## Project Structure

- `manage.py`: Django management script
- `db.sqlite3`: SQLite database file
- `project4/`: Main Django project folder containing settings and URLs
- `network/`: Django app handling the core social network functionalities

## Getting Started

### Prerequisites

- Python 3.x
- Django 3.x
- SQLite

### Installation

1. Clone the repository:

    ```
    git clone https://github.com/GavinWang-2024/social_network_site.git
    cd social_network_site
    ```

2. Apply migrations:

    ```
    python manage.py makemigrations network
    python manage.py migrate
    ```

4. Run the development server:

    ```
    python manage.py runserver
    ```

5. Access the site at `http://127.0.0.1:8000/`.
