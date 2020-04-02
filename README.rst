djfirebirdsql
==============

Django firebird https://firebirdsql.org/ database backend.

I referrerd django-firebird database backend https://github.com/maxirobaina/django-firebird .

Requirements
-------------

* Django 3.x
* Firebird 2,1> at 4.0 beta1
* Python 3.x
* pyfirebirdsql (https://github.com/nakagami/pyfirebirdsql) recently released.

Installation
--------------

::
    $ pip install firebirdsql 
    $ git clone https://github.com/maiconsaraiva/djfirebirdsql.git
    $ python -m pip install -e PATH_TO_CLONED\djfirebirdsql

Database settings example
------------------------------

::

    DATABASES = {
        'default': {
            'ENGINE': 'djfirebirdsql',
            'NAME': '/path/to/database.fdb',
            'HOST': ...,
            'USER': ...,
            'PASSWORD': ...,
        }
    }
