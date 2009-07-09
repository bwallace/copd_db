import pdb
import sqlalchemy as sa
from sqlalchemy import orm

from copd_db.model import meta

def init_model(engine):
    """Call me at the beginning of the application.
       'bind' is a SQLAlchemy engine or connection, as returned by
       sa.create_engine, sa.engine_from_config, or engine.connect().
    """

    sm = orm.sessionmaker(autoflush=True, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    meta.publication_t = sa.Table("publication", meta.metadata, autoload=True, autoload_with=engine)
    meta.arm_t = sa.Table("arm", meta.metadata, autoload=True, autoload_with=engine)
    meta.association_t = sa.Table("association", meta.metadata, autoload=True, autoload_with=engine)
    meta.gene_t = sa.Table("gene", meta.metadata, autoload=True, autoload_with=engine)
    meta.demographic_t = sa.Table("demographics", meta.metadata, autoload=True, autoload_with=engine)
    
    # map tables to objects via the ORM
    orm.mapper(meta.Publication, meta.publication_t)
    orm.mapper(meta.Arm, meta.arm_t)
    orm.mapper(meta.Association, meta.association_t)
    orm.mapper(meta.Gene, meta.gene_t)
    orm.mapper(meta.Demographic, meta.demographic_t)
    