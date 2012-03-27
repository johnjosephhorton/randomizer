from google.appengine.ext import db
from google.appengine.ext.db import polymodel
        
class Redirection(polymodel.PolyModel):
    experiment_name = db.StringProperty(required = False)
    landing_hash = db.StringProperty()
    admin_hash = db.StringProperty()
    
class StratifiedRedirection(Redirection):
    # the last visited target URL
    last_target_index = db.IntegerProperty(default = -1)
    
class Target(db.Model):
    url = db.LinkProperty()
    redirection = db.ReferenceProperty(Redirection)
    
class Visit(db.Model):
    redirection = db.ReferenceProperty(Redirection)
    target = db.ReferenceProperty(Target)
    ip = db.StringProperty()