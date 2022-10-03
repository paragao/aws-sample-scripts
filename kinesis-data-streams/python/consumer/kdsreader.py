from base64 import b64decode
import json
import logging 
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
xray_recorder.configure(service='kinesis ingest demo')
patch_all()

ddb = boto3.resource('dynamodb')
table = ddb.Table('kinesis-ingest')

@xray_recorder.capture('lambda main parsing kinesis data')
def lambda_handler(event, context):
    for record in event['Records']:
        preDec = b64decode(record['kinesis']['data'])
        dec = json.loads(str(b64decode(preDec), "ascii"))

        params = {
            'TableName': 'kinesis-ingest',
            'kinesisPartitionKey': record['kinesis']['partitionKey'],
            'datetime': dec['date'],
            'transaction_value': dec['transaction_value'],
            'credit_card_number': dec['credit_card_number'],
            'account_iban': dec['account_iban'],
            'bank_country': dec['bank_country'],
            'country': dec['country'],
            'name': dec['name'],
            'payload_full': dec,
        }

        response = table.put_item(
            Item=params
        )

        logger.info('item inserted \r', response)

    return 'data processed'