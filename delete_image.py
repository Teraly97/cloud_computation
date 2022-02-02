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
    # connect to database
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb')
    image_table = dynamodb.Table('images_record')
    
    # get items by two keys
    response = image_table.get_item(Key={'image_name': image_name})
    if "Item" not in response:
        return {
            "statusCode": 200,
            "body": json.dumps({"res": "image not found"}),
            'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }

    # s3_url used to delete image in s3 bucket
    s3_url = response['Item']["image_s3_url"]
    
    # delete the item in database
    delete_res = image_table.delete_item(
        Key={
            'image_name': image_name
        }
    )
    # delete successfully
    if delete_res['ResponseMetadata']['HTTPStatusCode'] == 200:
        # delete the item in s3 bucket
        s3.Object('fit5225-ass2-upload', image_name).delete()
        msg = "delete image successfully"
    else:
        # delete failed
        msg = "delete image failed"

    return {
        "statusCode": 200,
        "body": json.dumps({"res": msg}),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }
