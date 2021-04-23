import base64
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    """
    Expects a basic auth token in the headers. The decoded token should be a tuple
    with owner last name and ownerID
    :param event:
    :param context:
    :return:
    """
    request = event['Records'][0]['cf']['request']

    if 'authorization' in request['headers']:
        try:
            token = request['headers']['authorization'][0]['value'].replace('Basic ', '')
            message_bytes = base64.b64decode(token)
            message = message_bytes.decode('ascii')
            (username, password) = message.split(':')

            # Look up owner ID in the database
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('cgfc_owners')
            db_results = table.query(KeyConditionExpression=Key('owner_id').eq(password))
            items = db_results['Items']

            # Make sure provided last name matches the database
            if len(items) == 1 and items[0]['last_name'] == username:
                print("GRANTED!")
                return request

            print(username, password)
            msg = "Pass" + username + password
        except Exception as eek:
            msg = str(eek)

        response = {
            "status": '401',
            "statusDescription": 'Mystery',
            "body": "Mysterious," + str(request['headers']) + "---" + msg
        }

        return response

    body = 'Unauthorized';
    response = {
        "status": '401',
        "statusDescription": 'Unauthorized',
        "body": body,
        "headers": {
            'www-authenticate': [{"key": 'WWW-Authenticate', "value": 'Basic'}]
        }
    }
    return response
