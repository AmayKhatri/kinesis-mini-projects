!pip install boto3 awscli

import getpass

# Input AWS credentials and region
aws_access_key_id = getpass.getpass('Enter AWS Access Key ID: ')
aws_secret_access_key = getpass.getpass('Enter AWS Secret Access Key: ')
aws_region = input('Enter AWS Region: ')

!aws configure set aws_access_key_id $aws_access_key_id
!aws configure set aws_secret_access_key $aws_secret_access_key
!aws configure set default.region $aws_region

stream_name = 'weatherstream'

!aws kinesis create-stream --stream-name weatherstream

!aws kinesis describe-stream-summary --stream-name weatherstream


import json
import time
import random
# Initialize Kinesis client
kinesis_client = boto3.client('kinesis', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

def put_weather_data(city, temperature, humidity, wind_speed,rainfall_probability):
    try:
        data = {
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": int(time.time()),
            "additionalData": {"wind speed in m/s": wind_speed_data,
            "rainfall_probability in %": rainfall_probability}
        }
        print(data)
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey=city
        )
        print(f"Weather data written to Kinesis. SequenceNumber: {response['SequenceNumber']}, ShardId: {response['ShardId']}, Data: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami"]

    for _ in range(10):
        city = random.choice(cities)
        temperature = round(random.uniform(10, 30), 2)
        humidity = round(random.uniform(40, 80), 2)
        wind_speed_data = round(random.uniform(1, 10), 2)
        avg_rainfall_probability = (random.randint(0, 100))
      

        put_weather_data(city, temperature, humidity, wind_speed_data, avg_rainfall_probability)
        time.sleep(2)  # Simulating periodic data transmission
