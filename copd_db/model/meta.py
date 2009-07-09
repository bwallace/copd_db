"""SQLAlchemy Metadata and Session object"""
import sqlalchemy
from sqlalchemy import MetaData

__all__ = ['engine', 'metadata', 'Session']

# SQLAlchemy database engine.  Updated by model.init_model().
engine = None

# SQLAlchemy session manager.  Updated by model.init_model().
Session = None

# Global metadata. If you have multiple databases with overlapping table 
# names, you'll need a metadata for each database.
metadata = MetaData()

arm_t, association_t, publication_t, gene_t, demographic_t =  None, None, None, None, None

''''
We use SQL alchemy to map our tables into these objects (black magic!)
'''
class Arm(object):
	pass

class Association(object):
	pass
	
class Publication(object):
	pass 
	
class Gene(object):
    pass
    
class Demographic(object):
    pass