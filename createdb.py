"""
this is only ran to create the database 
initially. This can be done from an interactive 
python3 shell.
"""

#import the database from app
from app import db 
#creates all tables 
db.create_all()
exit()