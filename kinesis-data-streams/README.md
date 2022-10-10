# WIP 
# Data ingestion and processing using Amazon Kinesis

This sample application was created in two different programming languages. You can find the Python version [here](./python/README.md) and the NodeJS version [here]. 

The purpose of the application is the same: to ingest streaming data into a database and a data lake at the same time, with low latency and high throughput.

## Running the demonstration
To run this demonstration you will have to:
- Have an AWS Account
- Create an Amazon Kinesis Data Streams stream. Please follow the instructions [here](). Write down the name of the stream as it will be used later.
- Create two Lambda functions, one named `producer` and the other named `consumer` . Choose Python as your runtime and arm64 as the platform. Configure the Lambda for a runtime of 30 seconds (at least)
- Configure the Environment Variables for the `producer` lambda. Create one variable named `SERVICE_NAME` and give it any name (avoid spaces and special characters). Create a second variable named `KINESIS_STREAM` and use the same name as the stream you created earlier. 
- Upload the proper code to each of the lambdas. 
- To start the workflow invoke the `producer` lambda. The AWS CLI command is: `aws lambda invoke --function-name <lambda_name> output.txt`