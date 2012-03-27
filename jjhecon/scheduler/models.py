from django.db import models

class WaitVisit(db.Model):
    hit_id = db.StringProperty()
    assignment_id = db.StringProperty()
    confirmation_code = db.StringProperty()