#!/usr/bin/env python3
# Boto3 home page
# https://github.com/boto/boto3
#
# set up credentials (in e.g. ~/.aws/credentials):
# [default]
# aws_access_key_id = YOUR_KEY
# aws_secret_access_key = YOUR_SECRET
# set up a default region (in e.g. ~/.aws/config):
# [default]
# region=us-west-2

import boto3

# Create a DynamoDB client using the default credentials and region
dynamodb = boto3.client("dynamodb")

# Initialize a paginator for the list_tables operation
paginator = dynamodb.get_paginator("list_tables")

# Create a PageIterator from the paginator
page_iterator = paginator.paginate(Limit=10)

# List the tables in the current AWS account
print("Here are the DynamoDB tables in your account:")

# Use pagination to list all tables
table_names = []

for page in page_iterator:
    for table_name in page.get("TableNames", []):
        print(f"- {table_name}")
        table_names.append(table_name)

if not table_names:
    print("You don't have any DynamoDB tables in your account.")
else:
    print(f"\nFound {len(table_names)} tables.")



