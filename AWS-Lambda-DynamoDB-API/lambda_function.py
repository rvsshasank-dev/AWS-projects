import json
import boto3
import urllib.parse
import os

def lambda_handler(event, context):
    try:
        response = page_router(event['httpMethod'], event.get('queryStringParameters'), event.get('body'))
        return response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def page_router(httpmethod, querystring, formbody):
    if httpmethod == 'GET':
        return render_html('contactus.html')

    elif httpmethod == 'POST':
        try:
            insert_record(formbody)
            return render_html('success.html')
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'DynamoDB Error: {str(e)}'})
            }

    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'})
        }

def render_html(filename):
    try:
        with open(filename, 'r') as htmlFile:
            htmlContent = htmlFile.read()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': htmlContent
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'File Read Error: {str(e)}'})
        }

def insert_record(formbody):
    # Parse form-encoded body
    parsed_data = urllib.parse.parse_qs(formbody)
    # Convert to DynamoDB item format
    item = {k: {'S': v[0]} for k, v in parsed_data.items()}
    
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='kawintable',
        Item=item
    )
    return response
