import socket
from confluent_kafka import Producer
import os
from dotenv import load_dotenv

load_dotenv()

# Kafka broker configuration
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((os.getenv("host"), int(os.getenv("port"))))

# Create a Producer instance
producer_config = {
    'bootstrap.servers': os.getenv('bootstrap_servers'),
}
producer = Producer(producer_config)

while True:
    try:
        message = server.recv(1024).decode('utf-8')
        producer.produce(os.getenv("topic"), key="key", value=message)
      
    except socket.timeout:
        print("No messages received in the last 10 seconds.")
    except ConnectionResetError:
        print("Connection reset by peer.")
        break


# Wait for any outstanding messages to be delivered and delivery reports received
producer.flush()

# Close the producer
producer.close()
server.close()