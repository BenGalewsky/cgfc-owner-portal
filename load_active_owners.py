import csv
import boto3
"""
This script reads a csv file of active owners and inserts them into the 
Dynamo db. The primary key of this table is the owner ID
"""
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cgfc_owners')
with open('ActiveOwners04.19.21.csv', mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for owner in csv_reader:
        print(owner['OwnerNum'], owner['LastName'], owner['FirstName'])
        item = {
            'owner_id': owner['OwnerNum'],
            'first_name': owner['FirstName'],
            'last_name': owner['LastName'],
            'email': owner['Email']
        }
        table.put_item(Item=item)

