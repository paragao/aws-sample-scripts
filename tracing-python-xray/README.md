# Tracing Python applications using AWS XRay

This project aims to give a brief overview of what you can do to trace applications when coding in Python. 

It is a very basic code, showcasing how to initially setup [AWS XRay](https://docs.aws.amazon.com/xray/index.html) into your Python application. 

![AWS XRay Service Map example](https://github.com/paragao/xray-tracing-python/blob/main/images/ServiceMap.png?raw=true)

## How to deploy

After you clone this repo you need to install the Python3 modules: 

`pip3 install -e requirements.txt`

This will install all the requirements for this application (mainly aws-xray-sdk, argparser, and requests). 

Then, if running this application in a virtual server (not an AWS Lambda, for example), you will need to install the XRay daemon. This daemon handles the API calls to AWS XRay in order to optimize the cost and do not call AWS XRay every single time your application calls it. The XRay daemon is capable of buffering those calls and reducing the amount of time it calls the XRay service, thus reducing the costs.

To install the XRay daemon, please follow the instructions [here](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html). 

For Amazon Linux 2 (or RedHat-like linux systems), specifically, you can run the following commands: 

`wget https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-3.x.rpm`

`sudo yum install -y aws-xray-daemon-3.x.rpm`

`sudo systemctl enable aws-xray-daemon && sudo systemctl start aws-xray-daemon`


## How to run the application

All you need to do is call the application like this: 

`python3 call_api.py -u <url>`

where `<url>` is the URL of the API you want to call. It is recommended that your API also implement AWS XRay so you can create a [Service Map](https://docs.aws.amazon.com/xray/latest/devguide/xray-console.html) and get a complete tracing of all requests in your application.

## More details

More details about the AWS XRay SDK can be found [here](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python.html) and [here](https://pypi.org/project/aws-xray-sdk/)