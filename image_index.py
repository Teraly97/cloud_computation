import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    # this function is to search all images uploaded
    # connect to database
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb')
    image_table = dynamodb.Table('images_record')
    
    # get items
    response = image_table.scan()
    
    if response['Count'] == 0:
        return {
            'statusCode': 200,
            "body": json.dumps([]),
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response["Items"]),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }