from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

mongouri = os.getenv("MONGO_DETAILS")
conn = MongoClient(mongouri)
mydatabase = conn[os.getenv("Database")]
device_collection = mydatabase[os.getenv("collection")]

conf = {
    'bootstrap.servers': os.getenv("bootstrap_servers"),
    'group.id': os.getenv("group_id"),
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # Disable auto-commit of offsets
}

consumer = Consumer(conf)
consumer.subscribe([os.getenv("topic")])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break

        json_str = msg.value().decode('utf-8')

        try:
            document = json.loads(json_str)
            if isinstance(document, dict):
                device_collection.insert_one(document)
            else:
                print("Invalid document format:", document)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        # Commit the offset
        consumer.commit()

except KeyboardInterrupt:
    print("Interrupted. Closing consumer.")
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
    print("Consumer closed.")