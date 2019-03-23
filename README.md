# Roadside Assistance Project
The aim of this project is to provide a simple webapp that provides users with the ability to register and provide _roadside assistance services_

### Running the project
This project is built with the web framework [Django](https://docs.djangoproject.com/en/2.1/). Here's steps to get it running.

1. Install Python 3
2. Install django version 2.1.5 using pip

```bash
pip3 install django==2.1.5
```

3. Clone this repository into a directory and enter it

```bash
git clone git@github.com:wizzledonker/ezyassist.git
cd ezyassist
```

4. Use python to make migrations (create necessary databases) and import the default plans into the database (default plans are located in assist/fixtures/pricingmodels.json)

```bash
python manage.py makemigrations
python manage.py makemigrations assist
python manage.py migrate
python manage.py loaddata pricingmodels
```

5. Run the server

```bash
python manage.py runserver
```

6. Go to a browser and visit `localhost:8000/assist` to view the website.