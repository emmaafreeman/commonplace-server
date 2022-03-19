# Commonplace

The goal of this project was to create a customizable system for commonplacing, the process of maintaining a personal encyclopedia. Like a lot of writers, I commonplace using notebooks, but I wanted to simplify the process of indexing/searching for specific entries.

The user can create, update, and delete entries, and view their entries on the home page of the app. They can create topics of their choice and tag each entry with as many topics as they would like. They can then search existing entries by title or keyword, and filter the results by alphabetical order, date created, and/or topic.

Future features will include:
- the ability to view the next/last entry by alphabetical order or date created from the entry detail page
- the ability to link related entries together and view them in a list on the entry detail page
- the ability to upload photos for an entry

This project was an exercise in how to build and interact with my own API. Django is a little daunting, so it took some time to adjust to writing the back-end code. Eventually, it was satisfying to figure out to get it to respond with exactly what I needed on the client side!

### Technologies Used
1. Javascript
2. React.js
3. React Bootstrap
4. Python
5. Django
6. SQLite

### ERD

https://dbdiagram.io/d/6217b0c1485e43354310fe16

### Install Instructions

Open a terminal window and go to the `commonplace-server` directory.

#### pipenv

1. `pip3 install --user pipx`
2. `pipx install pipenv`

#### Start a virtual environment

1. `pipenv shell`

#### Django/Pylint

1. `pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django`

### Starting the server

Open a terminal window and go to the `commonplace-server` directory.

1. `pipenv shell`
2. `python3 manage.py runserver`

### Starting the app in development mode

Go to https://github.com/emmameiervogel/commonplace-client and follow install instructions for the client.

Open a terminal window and go to the `commonplace-client` directory.

1. `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.