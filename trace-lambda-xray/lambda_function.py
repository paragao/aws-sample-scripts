from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import shutil

patch_all()

file95 = "/mnt/efs/file1.pdf"
file400 = "/mnt/efs/file2.mp4"

xray_recorder.begin_subsegment('copying 95MB to /tmp')
shutil.copy(file95, '/tmp/')
xray_recorder.end_subsegment()

xray_recorder.begin_subsegment('copying 402MB to /tmp')
shutil.copy(file400, '/tmp/')
xray_recorder.end_subsegment()

def lambda_handler(event, context):    
    file95tmp = '/tmp/file1.pdf'
    file400tmp = '/tmp/file2.mp4'

    xray_recorder.begin_subsegment('copying - 95MB')
    with open(file95tmp, 'rb') as f:
      f.read()
    xray_recorder.end_subsegment()

    xray_recorder.begin_subsegment('copying - 400MB')
    with open(file400tmp, 'rb') as f:
      f.read()
    xray_recorder.end_subsegment()
