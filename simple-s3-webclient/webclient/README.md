# Amazon S3 Simple Web client using AWS Amplify

This is a project based on a customer need. They wanted to have an user interface to easily share files between third party companies, allowing them to download and upload files easily. FTP/SFTP and other protocols which required creating an user directory or setting up a client on the third party side was not an option. Also they wanted something simple and low cost. As they already used AWS, it was only natural to use AWS Amplify. 


## Pre-requisites

This project was built on top of React and Javascript. It leverages [AWS Amplify](https://aws.amazon.com/amplify/getting-started/) to create resources without needing to know how to manually deploy them or writing IaC scripts such as AWS CloudFormation. You only need: 

 1. An AWS account with the right set of permissions to use AWS Amplify and create the require resources;
 2. NodeJS 14 or higher;
 3. This repo cloned to your github account or locally.

## The architecture

AWS Amplify is capable of creating AWS resources on your account based on the libraries you install and add to your project. Never deployed a GraphQL API using AWS AppSync? Never create a table on Amazon DynamoDB? No problem! Just create your app and tell AWS Amplify you want those and it will take care of it for you. 

The architecture diagram is very simple. Let's take a look at it:

![Simple S3 Web Client Architecture](https://github.com/paragao/simple-s3-webclient/blob/master/images/simple-s3-web-client.png?raw=true)

 1. [AWS Amplify](https://aws.amazon.com/amplify/getting-started/) stores the React website on [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) and uses [Amazon Cloudfront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html) as a CDN. This is the first layer of protection since only the CDN is able to access the data on Amazon S3.
 2. This project uses [Amazon Cognito](https://aws.amazon.com/cognito/getting-started/) as the identity provider. It will authenticate users and also exchange those JWT tokens to AWS STS tokens which will allow access to the required AWS resources.
 3. Once the user is logged in, the website uses [AWS AppSync](http://console.aws.amazon.com/appsync/home) to interact with the provided API. 
 4. AWS Amplify has a feature called [DataStore](https://docs.aws.amazon.com/whitepapers/latest/amplify-datastore-implementation/amplify-datastore-overview.html), which allows for data to be stored in the user session and sync'ed with the [Amazon DynamoDB](https://aws.amazon.com/dynamodb/getting-started/) table on the AWS cloud. AWS AppSync uses the Amazon DynamoDB to keep track of what's happening in terms of file uploaded/deleted so we can use it as an audit tool later.
 5. AWS AppSync also connects to Amazon S3 to store the actual files. The key (filename) is stored on Amazon DynamoDB as well so we can query the storage area to find a specific file. But the actual data is stored on Amazon S3. It also uses the log in information to create a private area where only the logged in user is capable of uploading/downloading/listing its files.

As you can see, nothing very fancy but simple to achieve our goal. 

## How to deploy

As I am using AWS Amplify in this project the best way is to use it on your account as well. Navigate to the [AWS Amplify console]() and click on `New App` and choose `Host a new app`. This will allow you to connect a Github repo to the AWS Amplify and it will setup a CI/CD pipeline automatically for you. Make sure you choose `Create a new environment` when deploying this project otherwise it will try to connect to my backend environment (which, of course, you will not have access to because it is isolated to my AWS account). 

![Create a new backend environment](https://github.com/paragao/simple-s3-webclient/blob/master/images/backend-env.png?raw=true)

AWS Amplify allows you to share a single backend environment between multiple frontend projects. For this use case, please create your own. 

Also, make sure you go to `Advanced Settings` at the bottom of the page and choose `Add package version override` and add a package `Node.js version` with version `14`. I used react-app@5.0.0 which requires at least NodeJS 14 or higher.

![Update NodeJS to version 14](https://github.com/paragao/simple-s3-webclient/blob/master/images/adv-settings.png?raw=true)

If you do not want to use Github as your repo, AWS Amplify allows you to store your code on GitLab, BitBucket, AWS CodeCommit, or deploy this project without a Git provider (by uploading it through the console or storing the code on an Amazon S3 bucket, for example).

When the deploy is complete, you will be able to access the website using the provided URL for the CDN that was created for you. Create an account, verify your code, and start using this Simple S3 Web Client. 

![Amplify Login](https://github.com/paragao/simple-s3-webclient/blob/master/images/amplify-signin.png?raw=true)