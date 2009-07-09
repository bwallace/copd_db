
Installation and Setup
======================

You'll need R and a few python dependencies to install. 

Install ``copd_db`` using easy_install::

    easy_install copd_db

Make a config file as follows::

    paster make-config copd_db config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
