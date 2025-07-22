import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('receipt_status')
s3 = boto3.client('s3')

RESULT_BUCKET = 'lerui-receipt-results'

def lambda_handler(event, context):
    user_id = event['queryStringParameters']['user_id']
    receipt_id = event['queryStringParameters']['receipt_id']

    # 1. Look up the receipt in DynamoDB
    response = table.get_item(
        Key={'user_id': user_id, 'receipt_id': receipt_id}
    )

    item = response.get('Item')
    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Receipt not found"})
        }

    if item['status'] != 'done':
        return {
            "statusCode": 202,
            "body": json.dumps({"status": "pending"})
        }

    # 2. Get the result from S3
    output_key = item['output_key']  
    try:
        result_obj = s3.get_object(Bucket=RESULT_BUCKET, Key=output_key.split("/", 1)[1])
        result_data = result_obj['Body'].read().decode('utf-8')
        return {
            "statusCode": 200,
            "body": result_data,
            "headers": {"Content-Type": "application/json"}
        }
    except s3.exceptions.NoSuchKey:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Result file not found in S3"})
        }
