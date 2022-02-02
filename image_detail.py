import json
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    # connect to database
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb')
    image_table = dynamodb.Table('images_record')
    
    # get js post data body
    data = json.loads(event['body'])
    image_link = data['image_link']
    
    response = image_table.scan(
        FilterExpression=Attr('image_link').eq(image_link)
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response['Items']),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }
