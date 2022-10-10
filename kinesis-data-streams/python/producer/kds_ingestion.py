from datetime import datetime
from random import randint
import json
import logging
import os
import boto3
from faker import Faker
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# lib used to create fake data such as name, credit card number, etc
fake = Faker()

# logging utilities and AWS X-Ray patching for observability
logger = logging.getLogger()
logger.setLevel(logging.INFO)
xray_recorder.configure(service=os.environ['SERVICE_NAME'])
patch_all()

# create the boto3 clients to connect to the AWS services and get the stream name from a lambda environment variable
kinesis = boto3.client('kinesis')
kinesis_stream_name = os.environ['KINESIS_STREAM']

# ingest data into the Amazon Kinesis Data Stream
# input - records: object
@xray_recorder.capture('## kinesis ingestion')
def kinesis_ingest(records):
    '''
    Receive an array of records and create an aggregated object. 
    Interate on the array to create an unique partition key and normalize the data

    params:
        records: array of record
    '''
    normalized_records = []
    for record in records: 
        data = json.dumps(record).encode("ascii")
        partition = 'demo-' + str(randint(1000, 9999))
        normalized_records.append({
            'Data': data,
            'PartitionKey': partition
        }) 

    kinesis_response = kinesis.put_records(
        Records=normalized_records,
        StreamName=kinesis_stream_name,
    )

    return kinesis_response

@xray_recorder.capture('## main logic')
def main_logic(): 
    '''
    Main business logic. Create a set of records and send it to be ingested.
    '''
    print('ingesting a serie of records into Kinesis Data Stream')
    records = []
    for _ in range(100):
        record = {
            "name": fake.name(),
            "address": fake.address(),
            "country": fake.country_code(),
            "credit_card_number": fake.credit_card_number(),
            "credit_card_expire": fake.credit_card_expire(),
            "credit_card_provider": fake.credit_card_provider(),
            "phone": fake.phone_number(),
            "job": fake.job(),
            "company": fake.company(),
            "account_iban": fake.iban(),
            "bank_country": fake.bank_country(),
            "date": datetime.now().isoformat(),
            "transaction_value": randint(5, 500)
        }
        records.append(record)

    xray_recorder.begin_subsegment('ingest data')
    response = kinesis_ingest(records)
    xray_recorder.end_subsegment()

    return response

def lambda_handler(event, context):
    '''
    Lambda logic. Runs the business logic.
    '''
    main_logic()

    return 'data ingested'
