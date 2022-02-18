# Objective

This repository has the objective of compiling a series of small projects that I have worked on for customers and friends. Most of them will be interacting with the AWS services. 

List of projects is ever increasing and includes:
 - Delete Amazon S3 buckets which are not empty
 - Frontend that allows to upload/download files from Amazon S3
 - Implement tracing on python/nodejs applications using AWS XRay
 - Managing costs and resources using tags

# Projects

## List of contents
### [Delete Amazon S3 buckets which are not empty](https://github.com/paragao/aws-sample-scripts/tree/main/delete-buckets)
Buckets can only be deleted if they are empty. This script will iterate through all objects and delete them. 

### [Tracing Python microservices with AWS XRay and Amazon ECS](https://github.com/paragao/aws-sample-scripts/tree/main/tracing-python-xray)
Observability is important to identify possible performance bottleneck, improve customer experience, and identify problems/errors in your applications. 

### [Simple S3 WebClient](https://github.com/paragao/aws-sample-scripts/tree/main/simple-s3-webclient)
**[[ WIP ]]**

A simple web client that allows to upload/download files from Amazon S3. Integrates with Amazon Cognito to allow for private storage. Based on NodeJS and React, uses AWS Amplify to simplify the integration with the AWS services.

### [Tracing NodeJS functions with AWS XRay and Amazon API Gateway](https://github.com/paragao/aws-sample-scripts/tree/main/trace-lambda-xray)
**[[ WIP ]]**

Implement observability on REST API using Amazon API Gateway and AWS Lambda functions as the backend. This project is based on NodeJS and will demonstrate how to create an API Gateway that uses AWS Lambda to run the microservices code. AWS XRay is used to decorate the functions and allow visibility on latency and errors.

### [Replace 2-phase commit with SAGA based orchestration]()
**[[ WIP ]]**

Use an orchestration based modernization of applications by leveraging the method of SAGA. This project helps companies that relies on 2-phase commit (or global transactions) implement a SAGA-based state machine that decouples the services and also enable the usage of microservices. It will help companies modernize their applications and reduce the total cost of ownership (TCO).