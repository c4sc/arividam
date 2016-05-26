arividam
==============================

A school news and information portal

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


LICENSE: MIT


Settings
------------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Development
-----------

Setup with Docker
^^^^^^^^^^^^^^^^^

Use the dev.yml file along with `docker-compose` as detailed in the Deployment/Docker section below.

*Getting Started*::

    $ docker-compose -f dev.yml build
    $ docker-compose -f dev.yml up
    $ docker-compose -f dev.yml run django python manage.py migrate
    $ docker-compose -f dev.yml run django python manage.py createsuperuser

    $ docker inspect arividam_django | grep IPAddress

Use the IP address from the last step to access the running Django instance at http://<ip_address_from_above>:8000/


Setup without Docker
^^^^^^^^^^^^^^^^^^^^

Create a database and user with access. Copy env.example to .env and customize DATABASE_URL using the following format: 

* SQLite format: sqlite:///PATH
* MySQL: mysql://USER:PASSWORD@HOST:PORT/DATABASE_NAME
* Postgres: postgres://USER:PASSWORD@HOST:PORT/DATABASE_NAME

Then run::

    $ python manage.py migrate
    $ python manage.py runserver


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use `MailHog`_ when generating the project a local SMTP server with a web interface will be available.

.. _mailhog: https://github.com/mailhog/MailHog

To start the service, make sure you have nodejs installed, and then type the following::

    $ npm install
    $ grunt serve

(After the first run you only need to type ``grunt serve``) This will start an email server that listens on ``127.0.0.1:1025`` in addition to starting your Django project and a watch task for live reload.

To view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

The email server will exit when you exit the Grunt task on the CLI with Ctrl+C.





Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at http://getsentry.com or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.




Deployment
----------





Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


