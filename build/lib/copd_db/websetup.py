"""Setup the copd_db application"""
import logging

from paste.deploy import appconfig
from pylons import config

from copd_db.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup copd_db here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
