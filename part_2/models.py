from mongoengine import connect, Document, StringField, BooleanField

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
domain = config.get('DB', 'DOMAIN')
db = config.get('DB', 'DB_NAME')


connect(host=f"""mongodb+srv://{user}:{password}@{domain}/{db}?retryWrites=true&w=majority""", ssl=True)


class Contact(Document):
    full_name = StringField(required=True, max_length=50)
    email = StringField(required=True, max_length=50)    
    phone = StringField(required=True, max_length=50)
    msg_sent = BooleanField(default=False)
    pref_mode = StringField(required=True)
    meta = {"collection": "contacts"}