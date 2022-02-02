import json
import boto3
import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # get js post data body
    data = json.loads(event['body'])
    image = data['file']
    image_name = data['image_name']
    # get image
    image = image[image.find(",") + 1:]
    # image base64 decode
    imageObj = base64.b64decode(image)
    # put image into s3 bucket
    s3.put_object(Bucket='fit5225-ass2-upload',Key=image_name,Body=imageObj,ACL='public-read',ContentType='mimetype',ContentDisposition='inline')
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps({"res": 'upload into s3 bucket successfully'}),
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }
