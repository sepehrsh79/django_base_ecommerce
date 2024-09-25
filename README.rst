============
DJANGO_BASE_ECOMMERCE
============

django_base_ecommerce provides a robust structure for product models in Django apps,
making it easier to build commerce applications.
Inspired by Django Oscar, this app aims to streamline the creation of business logic for e-commerce platforms,
offering a simple and flexible foundation.
Join us in contributing to a third-party app that helps developers kickstart e-commerce projects faster and more efficiently.


Build the Plugin
-----------

1. install build package ``pip install build``

2. build plugin ``python -m build``


Install 
-----------

1. install plugin locally ``pip install dist/django_base_ecommerce.tar.gz``


Usage
-----------

1. Add "django_base_ecommerce" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_base_ecommerce",
    ]

2. Run ``python manage.py migrate`` to create the tables.

3. Start the development server and visit the admin to create a products.


