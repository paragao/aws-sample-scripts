# Objective

This repository has the objective of compiling a series of small projects that I have worked on for customers and friends. Most of them will be interacting with the AWS services. 

List of projects is ever increasing and includes:
 - Delete Amazon S3 buckets which are not empty
 - Implement tracing on python applications using AWS XRay
 - Deploy a frontend that allows to upload/download files from Amazon S3

# Projects

## List of contents
### [Delete Amazon S3 buckets which are not empty](https://github.com/paragao/aws-sample-scripts/tree/main/delete-buckets)
Buckets can only be deleted if they are empty. This script will iterate through all objects and delete them. 

### [Tracing Python applications using AWS XRay](https://github.com/paragao/aws-sample-scripts/tree/main/tracing-python-xray)
Observability is important to identify possible performance bottleneck, improve customer experience, and identify problems/errors in your applications. 

### Simple S3 WebClient
A simple web client that allows to upload/download files from Amazon S3. Integrates with Amazon Cognito to allow for private storage. Based on NodeJS and React, uses AWS Amplify to simplify the integration with the AWS services.