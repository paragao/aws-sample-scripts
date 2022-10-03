from datetime import datetime
from random import randint
import json
import base64
import logging
from faker import Faker
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import boto3

# lib used to create fake data such as name, credit card number, etc
fake = Faker()

# logging utilities and AWS X-Ray patching
logger = logging.getLogger()
logger.setLevel(logging.INFO)
xray_recorder.configure(service='Kinesis ingest demo')
patch_all()

# create the boto3 clients to connect to the AWS services
kinesis = boto3.client('kinesis')
firehose = boto3.client('firehose')

# stream name - TODO: get from OS.ENVIRON
firehose_stream_name = 'From-KDS-to-S3'
kinesis_stream_name = 'My_Stream'

# ingest data into the Amazon Kinesis Data Stream
# input - records: object
@xray_recorder.capture('## kinesis ingestion')
def kinesis_ingest(records):
    putRecords = []
    for record in records: 
        data = base64.b64encode(json.dumps(record).encode("ascii"))
        partition = 'demo-' + str(randint(1000, 9999))
        putRecords.append({
            'Data': data,
            'PartitionKey': partition
        }) 

    kinesis_response = kinesis.put_records(
        Records=putRecords,
        StreamName=kinesis_stream_name,
    )

    return kinesis_response

@xray_recorder.capture('## firehose ingestion')
def firehose_ingest(record):
    data = base64.b64encode(json.dumps(record).encode("ascii"))
    firehose_response = firehose.put_record(
        DeliveryStreamName=firehose_stream_name,
        Record={ 
            'Data': data
        }
    )

    return firehose_response

if __name__ == "__main__":
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

    xray_recorder.begin_segment('ingest data')
    response = kinesis_ingest(records)
    xray_recorder.end_segment()

    print('data ingested ')
    