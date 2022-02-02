import json
import boto3
from boto3.dynamodb.conditions import Attr
import inputfolder
import object_detection

def lambda_handler(event, context):
    # connect to database
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb')
    image_table = dynamodb.Table('images_record')
    
    # get js post data body
    data = json.loads(event['body'])
    image = data['file']
    image_name = data['image_name']
    # get image
    image = image[image.find(",") + 1:]
    # detect input image's tags
    tags = object_detection.recog_image(image)
    
    response = []
    res = []
    link_value = []
    for i in range(0, len(tags)):
        response = image_table.scan(
            FilterExpression=Attr('image_tags').contains(tags[i])
        )
        
        if response["Count"] != 0:
            for j in response["Items"]:
                # used to check repeat image link
                if j['image_link'] not in link_value:
                    res.append(j)
                    link_value.append(j['image_link'])

    return {
        "statusCode": 200,
        "body": json.dumps(res),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }
