
import json
import boto3
import logging
import urllib.parse
import uuid
from dateutil import parser
import re

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
comprehend_client = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('receipt_status')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']  # e.g. "user1234/uuid.jpg"
        user_id = key.split("/")[0]
        receipt_id = key.split("/")[-1]


        # 1. Analyze document using Textract's analyze_expense
        response = textract_client.analyze_expense(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )

        # 2. Extract structured fields
        summary_data = extract_summary_data(response)
        items = extract_items_from_expense(response)
        extracted_data = {
           'ReceiptId': str(uuid.uuid4()),
           'Vendor': summary_data.get('VENDOR_NAME', 'N/A'),
           'Date': summary_data.get('INVOICE_RECEIPT_DATE', 'N/A'),
           'Total': summary_data.get('TOTAL', 'N/A'),
           'Items': items
       }


        # 3. Save result to receipt-scanned
        output_key = f"{user_id}/{receipt_id.replace('.jpg', '.json').replace('.png', '.json')}"
        s3_client.put_object(
            Bucket="lerui-receipt-results",
            Key=output_key,
            Body=json.dumps(extracted_data, indent = 2),
            ContentType='application/json'
           
        )

        # 4. Update DynamoDB
        table.update_item(
            Key={"user_id": user_id, "receipt_id": receipt_id},
            UpdateExpression="SET #s = :s, output_key = :o",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":s": "done",
                ":o": f"receipt-scanned/{output_key}"
            }
        )

        return {
            "message": "Upload successful",
            "user_id": user_id,
            "receipt_id": receipt_id
            }





# Extracting items
def extract_items_from_expense(response):
    items = []
    for doc in response.get('ExpenseDocuments', []):
        for group in doc.get('LineItemGroups', []):
            for item in group.get('LineItems', []):
                entry = {}
                for field in item.get('LineItemExpenseFields', []):
                    field_type = field.get("Type", {}).get("Text", "")
                    field_value = field.get("ValueDetection", {}).get("Text", "")
                    if field_type and field_value:
                        entry[field_type] = field_value
                if entry:
                    items.append(entry)
    return items



def extract_text_blocks(response):
    text_blocks = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_blocks.append(block['Text'])
    return text_blocks

def extract_data(text_blocks, comprehend_response):
    data = {'ReceiptId': str(uuid.uuid4())}
    entities = comprehend_response['Entities']
    vendor_name = None
    total_amount = None
    date = None

    for entity in entities:
        if entity['Type'] == 'ORGANIZATION' and vendor_name is None:
            vendor_name = entity['Text']
        elif entity['Type'] == 'DATE' and date is None:
            date = entity['Text']

    # Extract total amount more accurately
    for line in text_blocks:
        if 'total' in line.lower():
            parts = line.split()
            for part in parts:
                if part.replace('.', '', 1).isdigit():
                    total_amount = part
                    break

    data['Vendor'] = vendor_name if vendor_name else 'N/A'
    data['Total'] = total_amount if total_amount else 'N/A'
    data['Date'] = extract_date(text_blocks)

    return data

def extract_date(text_blocks):
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # Matches dates like MM/DD/YY or MM/DD/YYYY
    ]
    date_regex = re.compile('|'.join(date_patterns))
    
    for line in text_blocks:
        match = date_regex.search(line)
        if match:
            date_str = match.group(0)
            try:
                date = parser.parse(date_str, fuzzy=False)
                logger.info(f"Parsed date: {date.strftime('%Y-%m-%d')} from line: {line}")
                if date.year > 1900 and date.year < 2100:
                    return date.strftime('%Y-%m-%d')
            except ValueError:
                logger.info(f"Failed to parse date from line: {line}")
                continue
    return 'N/A'

def extract_summary_data(response):
    fields = {}
    for doc in response.get('ExpenseDocuments', []):
        for field in doc.get('SummaryFields', []):
            type_text = field.get("Type", {}).get("Text", "")
            value_text = field.get("ValueDetection", {}).get("Text", "")
            if type_text and value_text:
                fields[type_text] = value_text
    return fields



def save_to_s3(data, original_key):
    result_bucket = 'lerui-receipt-results'  
    result_key = 'results/' + original_key.split('/')[-1].replace('.jpg', '.json').replace('.png', '.json')

    s3_client.put_object(
        Bucket=result_bucket,
        Key=result_key,
        Body=json.dumps(data, indent=2),
        ContentType='application/json'
    )
