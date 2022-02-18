from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import argparse
import requests

xray_recorder.configure(service='call_api', daemon_address='127.0.0.1:2000')
plugins = ('EC2Plugin', 'ECSPlugin')
xray_recorder.configure(plugins=plugins)
patch_all()

# get URL from command line
# XRay is not monitoring this function, there is no decorator or subsegment declared
def args():
    parser = argparse.ArgumentParser(description="get URL from command line")
    parser.add_argument("-u", "--url", help="URL of the API you want to call")

    arguments = parser.parse_args()

    return arguments.url

@xray_recorder.capture('## call api')
def callApi(url):
    response = requests.get(url)
    return response

@xray_recorder.capture('## main')
def main():
    url = args()
    
    if not url:
        print('requires a URL to be passed on the command line')
        exit()

    response = callApi(url)
    print('return from API: {}'.format(response))

if __name__ == "__main__":
    # required to declare at least one segment
    segment = xray_recorder.begin_segment('call api from main')
    main()
    xray_recorder.end_segment()