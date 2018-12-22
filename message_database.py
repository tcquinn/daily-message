import pandas as pd
import boto3
import s3fs
import random
import os

class MessageDatabaseCSV:
    def next_message(self):
        message_list_df = self.get_dataframe()
        print('Successfully retrieved message database:\n{}'.format(message_list_df))
        print('Values for number of times used: {}'.format(message_list_df['num_times_used'].unique()))
        min_num_times_used = message_list_df['num_times_used'].min()
        print('Minimum number of times used: {}'.format(min_num_times_used))
        selectable_indices = message_list_df.index[message_list_df['num_times_used'] == min_num_times_used].tolist()
        print('Selectable indices: {}'.format(selectable_indices))
        selected_index = random.choice(selectable_indices)
        print('Selected index: {}'.format(selected_index))
        selected_message = message_list_df.loc[selected_index, 'body']
        print('Selected message: {}'.format(selected_message))
        message_list_df.loc[selected_index, 'num_times_used'] += 1
        print('New message database:\n{}'.format(message_list_df))
        self.put_dataframe(message_list_df)
        return(selected_message)

class MessageDatabaseCSVS3(MessageDatabaseCSV):
    def __init__(
        self,
        bucket_name=None,
        object_name=None):
        if bucket_name is None:
            bucket_name = os.environ['MESSAGE_DATABASE_S3_BUCKET_NAME']
        if object_name is None:
            object_name = os.environ['MESSAGE_DATABASE_S3_OBJECT_NAME']
        self.bucket_name = bucket_name
        self.object_name = object_name

    def get_dataframe(self):
        s3_location = 's3://' + self.bucket_name +'/' + self.object_name
        print('S3 location: {}'.format(s3_location))
        message_list_df = pd.read_csv(
            s3_location,
            index_col=0)
        return message_list_df

    def put_dataframe(
        self,
        message_list_df):
        s3 = s3fs.S3FileSystem(anon=False)
        s3_location = self.bucket_name + '/' + self.object_name
        with s3.open(s3_location,'w') as f:
            message_list_df.to_csv(f)

class MessageDatabaseCSVLocal(MessageDatabaseCSV):
    def __init__(
        self,
        path=None):
        if path is None:
            path = os.environ['MESSAGE_DATABASE_LOCAL_PATH']
        self.path = path

    def get_dataframe(self):
        message_list_df = pd.read_csv(
            self.path,
            index_col=0)
        return message_list_df

    def put_dataframe(
        self,
        message_list_df):
        message_list_df.to_csv(
            self.path)
