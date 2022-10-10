const { KinesisClient, PutRecordsCommand } = require('@aws-sdk/client-kinesis'); 
const kinesis = new KinesisClient({ region: process.env.REGION });
const { faker } = require('@faker-js/faker');
const AWSXRay = require('aws-xray-sdk');

exports.handler = async (event) => {
    var records = [];
    for (var i=0; i<100; i++) {
        records.push({
            Data: Buffer.from(JSON.stringify({
                name: faker.name.fullName(),
                address: faker.address.streetAddress(),
                country: faker.address.countryCode(),
                credit_card_number: faker.finance.creditCardNumber(),
                credit_card_expire: faker.date.future(),
                credit_card_provider: faker.finance.creditCardIssuer(),
                phone: faker.phone.number('+## ### ####-####'),
                job: faker.name.jobTitle(),
                company: faker.company.name(),
                account_iban: faker.finance.iban(),
                bank_country: faker.address.countryCode(),
                date: new Date(),
                transaction_value: faker.finance.amount(1, 1000)
            })),
            PartitionKey: 'auto-sharding-' + faker.random.numeric(3) 
        });
    }

    try { 
        const output = await kinesis.send(new PutRecordsCommand({
            Records: records,
            StreamName: process.env.KINESIS_STREAM
        }))
        console.log('data ingested: ', output)
    } catch (err) { 
        console.error('ingest failed: ', err)
    }

    const response = {
        statusCode: 200,
        body: JSON.stringify('record processed'),
    };
    
    return response;
}