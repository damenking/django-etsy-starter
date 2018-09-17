A Django app to automatically pull listing data from Etsy, store in a database and dynamically display
product listing and detail pages.  This is an incomplete project as I had started it for a business
idea but then realized Etsy already had a service called Pattern which duplicates what I was thinking
about doing.  Putting this out there though in case it can help anyone as a startng point to launch
a website for their Etsy store.  Some additional setup is needed to configure authorization to access private
fields from the Etsy API.

Uses Django and PostgreSQL for the backend with Django Rest Framework for convenient API building.  I personally use Digital Ocean for hosting this sort of thing.  Backend APIs are in the Etsy module. Explore the Etsy API docs to add to the models and
update the Etsy update command script to pull additional data you want. I built out a very simple frontend
with the html templates in web/templates and the javascript in assets/js/src.  Simply use html, css, js and jquery
to build off this example.


Install instructions (Ubuntu + command line):
---------------------------------------------
- Follow instructions to setup a postgres user 'etsy' with password 'etsy' and database called 'etsydb' for development.(https://medium.com/@mohammedhammoud/postgresql-create-user-create-database-grant-privileges-access-aabb2507c0aa)
- Install Python 3, pip and virtualenv

```
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```
- Create project directory then create virtual environment and build web directory
```
mkdir ~/app
cd ~/app
python3 -m venv env
source env/bin/activate
mkdir web
cd web
git init
git pull https://github.com/damenking/django-etsy-starter.git
```
- Install required Python packages
```
pip3 install -r requirements.txt
```
- Edit the web/settings.py file to set ETSY_API_KEY to the 'keystring' value given for an app after setting this up on Etsy (https://www.etsy.com/developers/register)
- Set a new Django secret key and get your Etsy user id based on your exact shop name
```
python manage.py set_secret_key
python manage.py set_etsy_user_id --shop_name <your Etsy shop name>
```
- Update the database tables
```
python manage.py migrate
```
- Pull data from Etsy into the database
```
python manage.py update_from_etsy
```
- Run your developement server and open http://localhost:8000 in your browser.  Navigate to the products
page and you should see a list of your products with thumbnails!
```
./manage.py runserver
```

Deploying production site:
--------------------------
Follow these instructions except for the tasks that have already been done in the previous steps

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

Feel free to contact me at damen.king@gmail.com if you have problems as it can be difficult to get everything set up.
