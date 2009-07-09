"""Pylons environment configuration"""
import os

from pylons import config
import sqlalchemy as sa
from copd_db import model
import copd_db.lib.app_globals as app_globals
import copd_db.lib.helpers
from copd_db.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='copd_db',
                    template_engine='mako', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = copd_db.lib.helpers

    # Customize templating options via this variable
    tmpl_options = config['buffet.template_options']

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    db_path = config["sqlalchemy.dburi"]
    print "using sql database @ %s" % db_path
    engine = sa.create_engine(db_path)
    model.init_model(engine)