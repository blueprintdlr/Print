@echo off

:: Install virtualenv
pip install virtualenv

:: Create and navigate to project directory
mkdir project
cd project

:: Create virtual environment and activate it
virtualenv env
call env\Scripts\activate.bat

:: Install required packages
pip install django reportlab pywin32 django-bootstrap5

:: Clone the GitHub repository
git clone https://github.com/blueprintdlr/Print.git

:: Navigate to the cloned repository and run the server
cd print
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
