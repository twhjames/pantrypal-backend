import boto3, base64, datetime, json

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('receipt_status')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body['user_id']
    image_data = base64.b64decode(body['image_base64'])

    receipt_id = body['receipt_id']
    s3_key = f"{user_id}/{receipt_id}"

    # Upload image to S3
    s3.put_object(Bucket="recipts-example", Key=s3_key, Body=image_data)

    # Create DynamoDB record
    table.put_item(Item={
        "user_id": user_id,
        "receipt_id": receipt_id,
        "status": "pending",
        "output_key": None,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

    return {
        "statusCode": 200,
        "body": json.dumps({"receipt_id": receipt_id})
    }
