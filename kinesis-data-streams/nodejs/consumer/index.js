const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, PutCommand } = require('@aws-sdk/lib-dynamodb')

const ddbClient = new DynamoDBClient({ region: process.env.REGION })
const ddbDocClient = DynamoDBDocumentClient.from(ddbClient);

exports.handler = async (event) => {
    
    event.Records.forEach(async (record) => {
        var payload = JSON.parse(Buffer.from(record.kinesis.data, 'base64').toString('ascii'));
        
        const params = { 
            TableName: 'kinesis-ingest',
            Item: { 
                kinesisPartitionKey: record.kinesis.partitionKey,
                datetime: payload.date,
                transaction_value: payload.transaction_value,
                credit_card_number: payload.credit_card_number,
                account_iban: payload.account_iban,
                bank_country: payload.bank_country,
                country: payload.country,
                name: payload.name,
                payload_full: payload,
            },
        };

        try { 
            const data = await ddbDocClient.send(new PutCommand(params));
            console.log('sucess inserting item into DynamoDB')
        } catch (err) { 
            console.log('error inserting data: ', err)
        }
        
    });

    const response = {
        statusCode: 200,
        body: JSON.stringify('record processed'),
    };
    
    return response;
};
