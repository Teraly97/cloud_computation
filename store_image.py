import json
import boto3
import os
import sys
import inputfolder
import object_detection
import base64
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    # get s3 bucket info
    for r in event['Records']:
        bucket = r['s3']['bucket']['name']
        key = unquote_plus(r['s3']['object']['key'])
        # get image file in s3 bucket
        imageObj = s3_client.get_object(Bucket=bucket, Key=key)
        # image base63 encode
        image = base64.b64encode(imageObj["Body"].read()).decode('utf8')
        # get file's tags
        tags = object_detection.recog_image(image)
        tags = list(set(tags))
        image_tags = ','.join(tags)
        # get file's s3_url
        s3_url = "s3://" + bucket + "/" + key
        # get image show link
        image_link = "https://" + bucket + ".s3.amazonaws.com/" + key
        # connect to database
        dynamodb = boto3.resource('dynamodb')
        image_table = dynamodb.Table('images_record')
        # insert into database
        response = image_table.put_item(
            Item = {
                'image_name': key,
                'image_tags': image_tags,
                'image_s3_url': s3_url,
                'image_link': image_link
            }
        )
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            msg = "upload successfully"
        else:
            msg = "insert into database failed"
        
    return {
        "statusCode": 200,
        "body": json.dumps({"res": msg}),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }
