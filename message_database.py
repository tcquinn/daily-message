import pandas as pd
import boto3
import s3fs
import json
import random
import os

class MessageDatabaseCSV:
    def next_message(self):
        message_list_df = self.get_dataframe()
        print('Successfully retrieved message database')
        print('Values for number of times used: {}'.format(message_list_df['num_times_used'].unique()))
        min_num_times_used = message_list_df['num_times_used'].min()
        print('Minimum number of times used: {}'.format(min_num_times_used))
        selectable_indices = message_list_df.index[message_list_df['num_times_used'] == min_num_times_used].tolist()
        print('Selectable indices: {}'.format(selectable_indices))
        selected_index = random.choice(selectable_indices)
        print('Selected index: {}'.format(selected_index))
        selected_message = {
            'body': message_list_df.loc[selected_index, 'body'],
            'contributor': message_list_df.loc[selected_index, 'contributor']}
        print('Selected message: {}'.format(selected_message))
        message_list_df.loc[selected_index, 'num_times_used'] += 1
        message_list_df.loc[selected_index, 'last_used'] = pd.Timestamp.now()
        print('Created new message database')
        self.put_dataframe(message_list_df)
        return(selected_message)

class MessageDatabaseCSVS3(MessageDatabaseCSV):
    def __init__(
        self,
        message_database_bucket_name=None,
        message_database_object_name=None):
        if message_database_bucket_name is None:
            message_database_bucket_name = os.environ['MESSAGE_DATABASE_S3_BUCKET_NAME']
        if message_database_object_name is None:
            message_database_object_name = os.environ['MESSAGE_DATABASE_S3_OBJECT_NAME']
        self.message_database_bucket_name = message_database_bucket_name
        self.message_database_object_name = message_database_object_name

    def get_dataframe(self):
        s3_location = 's3://' + self.message_database_bucket_name +'/' + self.message_database_object_name
        print('S3 location: {}'.format(s3_location))
        message_list_df = pd.read_csv(
            s3_location,
            index_col=0,
            parse_dates = ['last_used'])
        return message_list_df

    def put_dataframe(
        self,
        message_list_df):
        s3 = s3fs.S3FileSystem(anon=False)
        s3_location = self.message_database_bucket_name + '/' + self.message_database_object_name
        bytes_to_write = message_list_df.to_csv(None).encode()
        with s3.open(s3_location, 'wb') as f:
            f.write(bytes_to_write)

class MessageDatabaseCSVLocal(MessageDatabaseCSV):
    def __init__(
        self,
        message_database_local_path=None):
        if message_database_local_path is None:
            message_database_local_path = os.environ['MESSAGE_DATABASE_LOCAL_PATH']
        self.message_database_local_path = message_database_local_path

    def get_dataframe(self):
        message_list_df = pd.read_csv(
            self.message_database_local_path,
            index_col=0,
            parse_dates = ['last_used'])
        return message_list_df

    def put_dataframe(
        self,
        message_list_df):
        message_list_df.to_csv(
            self.message_database_local_path)

class MessageStoreS3:
    def __init__(
        self,
        message_store_bucket_name=None,
        message_store_object_name=None):
        if message_store_bucket_name is None:
            message_store_bucket_name = os.environ['MESSAGE_STORE_S3_BUCKET_NAME']
        if message_store_object_name is None:
            message_store_object_name = os.environ['MESSAGE_STORE_S3_OBJECT_NAME']
        self.message_store_bucket_name = message_store_bucket_name
        self.message_store_object_name = message_store_object_name

    def get_message(self):
        s3 = boto3.resource('s3')
        message_store_object = s3.Object(
            self.message_store_bucket_name,
            self.message_store_object_name)
        message_string = message_store_object.get()['Body'].read().decode('utf-8')
        message = json.loads(message_string)
        return message

    def put_message(
        self,
        message):
        message_string = json.dumps(message)
        s3 = boto3.resource('s3')
        message_store_object = s3.Object(
            self.message_store_bucket_name,
            self.message_store_object_name)
        message_store_object.put(
            Body=message_string.encode('utf-8'),
            ContentType='string')

class MessageStoreLocal:
    def __init__(
        self,
        message_store_local_path=None):
        if message_store_local_path is None:
            message_store_local_path = os.environ['MESSAGE_STORE_LOCAL_PATH']
        self.message_store_local_path = message_store_local_path

    def get_message(self):
        message_store = open(
            self.message_store_local_path,
            'r')
        message_string = message_store.read()
        message_store.close()
        message = json.loads(message_string)
        return message

    def put_message(
        self,
        message):
        message_string = json.dumps(message)
        message_store = open(
            self.message_store_local_path,
            'w')
        message_store.write(message_string)
        message_store.close()
