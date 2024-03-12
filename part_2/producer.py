import random
from faker import Faker
import pika

from models import Contact

fake = Faker()

def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='HW08_p2', exchange_type='direct')
    channel.queue_declare(queue='email', durable=True)
    channel.queue_declare(queue='sms', durable=True)
    channel.queue_bind(exchange='HW08_p2', queue='email') 
    channel.queue_bind(exchange='HW08_p2', queue='sms') 
    
    num_contacts = 100  
 
    for _ in range(num_contacts):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        pref_mode = random.choice(['sms', 'email'])
        contact = Contact(full_name=name, email=email, phone=phone,
                          pref_mode=pref_mode)
        contact.save()
        print(f"Contact {name}:({phone}, {email}) successfully added.")

        message_body = str(contact.id)
        
        if pref_mode == 'email':            
            channel.basic_publish(exchange='', routing_key='email', body=message_body)
            print(f"Sent message for contact {name}: ({email})")
        else:
            channel.basic_publish(exchange='', routing_key='sms', body=message_body)
            print(f"Sent message for contact {name}: ({phone})")

    connection.close()


if __name__ == "__main__":
    main()
