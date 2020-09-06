<h1 align="center"> 👜 Buy Bay 🌊 </h1>

<p style="font-family:courier;color:blue;font-size:130%;"><b> E-commerce app with Django for Fun! </b></p>


<p align="center">
<a href="">
<img alt="BuyBay " src="https://i.imgur.com/JaI1BKk.png%0A%20:target:%20https://github.com/pydanny/cookiecutter-django/%0A%20:alt:%20BuyBay">
</a>

<p align="center">
<a href="https://github.com/pydanny/cookiecutter-django/">
<img alt="Cookiecutter Django " src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg">
</a>

<a href="https://github.com/ambv/black">
<img alt="Black code style" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>

<a href="https://choosealicense.com/licenses/unlicense/">
<img alt="License: unlicense" src="https://img.shields.io/badge/License-Unlicense-brightgreen">
</a>
</p>


Template
--------

Used [Template](https://mdbootstrap.com/freebies/jquery/e-commerce/).

Settings
--------

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.
-   To create an **superuser account**, start in the root folder and use this command:

        $ docker-compose -f ./local.yml run --rm app ./manage.py migrate createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

-   To run any django command inside the docker environment, start in the root folder and use this command:

        $ docker-compose -f ./local.yml run --rm app ./manage.py migrate **...django_command...**

Deployment
----------

The following details how to deploy this application.

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
