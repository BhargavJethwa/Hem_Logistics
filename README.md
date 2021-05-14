# HEM_LOGISTICS

## Steps to setup the environment

### Create virtual environment:

`python3 -m pip install --upgrade pip` <br />
`pip3 install virtualenv` <br />
`virtualenv -p python3 venv` <br />

### Activate virtual environment:

`source venv/bin/activate`

### Installing required packages:

`pip3 install -r requirements.txt`

## Runing the app on local server

`python manage.py makemigrate` <br />
`python manage.py migrate` <br />
`python manage.py runserver` <br />

## Superuser details

Username : `admin` <br />
Password : `admin` <br />