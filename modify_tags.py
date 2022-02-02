import json
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    msg = ""
    data = json.loads(event['body'])
    # input link
    image_link = data['image_link']
    # get image_name as database's key
    image_name = image_link.split('/')[-1]
    input_tags = data['tags'].split(',')
    # connect to database
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb')
    image_table = dynamodb.Table('images_record')
    
    # get item by two keys
    response = image_table.get_item(Key={'image_name': image_name})
    
    tags = response['Item']["image_tags"].split(',')

    # remove tags
    for i in input_tags:
        for j in tags:
            if i == j:
                tags.remove(j)
    
    image_tags = ','.join(tags)
    
    # update database
    update_res = image_table.update_item(
        Key={
            'image_name': image_name
        },
        UpdateExpression="set image_tags = :t",
        ExpressionAttributeValues={
            ':t' : image_tags
        },
        ReturnValues="UPDATED_NEW"
    )

    if update_res['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = "remove tags successfully"
    else:
        msg = "remove tags failed"

    return {
        "statusCode": 200,
        "body": json.dumps({"res": msg}),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }
