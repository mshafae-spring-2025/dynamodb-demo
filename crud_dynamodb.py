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

import logging
from hashlib import md5
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)

# hashlib.md5(s.encode()).hexdigest()


class Links:
    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource
        self.table = None

    def exists(self, table_name):
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists

    def create_table(self, table_name):
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        "AttributeName": "md5hash",
                        "KeyType": "HASH",
                    },  # Partition key
                    {"AttributeName": "url", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "md5hash", "AttributeType": "S"},
                    {"AttributeName": "url", "AttributeType": "S"},
                ],
                BillingMode='PAY_PER_REQUEST',
            )
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.table

    def delete_table(self):
        try:
            self.table.delete()
            self.table = None
        except ClientError as err:
            logger.error(
                "Couldn't delete table. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def list_tables(self):
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            logger.error(
                "Couldn't list tables. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return tables

    def add_url(self, url):
        url_hash = md5(url.encode()).hexdigest()
        try:
            self.table.put_item(
                Item={
                    "md5hash": url_hash,
                    "url": url,
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't add url %s to table %s. Here's why: %s: %s",
                url,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return url_hash

    def query_url_hash(self, url_hash):
        try:
            response = self.table.query(
                KeyConditionExpression=Key("md5hash").eq(url_hash)
            )
        except ClientError as err:
            logger.error(
                "Couldn't query for url with hash %s. Here's why: %s: %s",
                url_hash,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Items"]


def main(table_name, dyn_resource):
    links = Links(dyn_resource)
    links_exists = links.exists(table_name)
    if not links_exists:
        print(f"\nCreating table {table_name}...")
        links.create_table(table_name)
        print(f"\nCreated table {links.table.name}.")
    url = input("Enter a URL: ")
    print('Adding URL')
    url_key = links.add_url(url)
    print(url_key)
    print('querying')
    response = links.query_url_hash(url_key)
    print(response)
    # print("Deleting table")
    # links.delete_table()


if __name__ == "__main__":
    try:
        table_name = 'squaturl-example-table'
        main(table_name, boto3.resource("dynamodb"))
    except Exception as e:
        print(f"Something went wrong with the demo! Here's what: {e}")
