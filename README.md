# Lab_mosquito
Linebot for reporting specific diseases (Dengue, Flu...)

## Getting Started

### Prerequisites

- Python 3.6
- Django 1.10
- Heroku CLI
- Postgres

### Installing

Creating a project
```
$ django-admin startproject {{project_name}}
```
Creating a app in the project
```
$ python manage.py startapp {{app_name}}
```
### Database setup and Creating models

Database setup
```
$ python manage.py migrate
```
Creating models
1. Change your models (in models.py)
2. create migrations for those changes
```
$  python manage.py makemigrations
```
3. apply those changes to the database
```
$  python manage.py migrate
```

### Playing with the API

Interactive Python shell and play around with the free API Django
```
$ python manage.py shell
```
