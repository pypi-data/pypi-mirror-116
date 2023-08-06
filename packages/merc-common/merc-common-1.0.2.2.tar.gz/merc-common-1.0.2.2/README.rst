
Merc Common Package
===================

Merc Common is a Django app common package for CRAMS api open source. Detailed documentation is in the "docs" directory.
Souce code is available at https://github.com/CRAMS-Dashboard/crams-api

Quick start
-----------

1. Add "merc_common" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'merc_common',
    ]

2. Include the merc_common URLconf in your project urls.py like this::

    path('merc_common/', include('merc_common.urls')),

3. Run ``python manage.py migrate`` to create the merc_common models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a merc_common (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to test the application.