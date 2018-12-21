import pandas as pd
import boto3
import s3fs
import os

class MessageList:
    def __init__(
        self,
        message_list_df):
        self.message_list_df = message_list_df

    # Load message list from local CSV file
    @classmethod
    def from_csv_file(
        cls,
        path):
        message_list_df = pd.read_csv(
            path,
            index_col=0)
        return cls(message_list_df)

    # Load message list from local CSV file
    @classmethod
    def from_csv_s3_object(
        cls,
        bucket_name,
        object_name):
        s3_location = 's3://' + bucket_name +'/' + object_name
        print('S3 location: {}'.format(s3_location))
        message_list_df = pd.read_csv(
            s3_location,
            index_col=0)
        return cls(message_list_df)

    def to_csv_file(
        self,
        path):
        self.message_list_df.to_csv(
            path)

    def to_csv_s3_object(
        self,
        bucket_name,
        object_name):
        s3 = s3fs.S3FileSystem(anon=False)
        s3_location = bucket_name +'/' + object_name
        with s3.open(s3_location,'w') as f:
            self.message_list_df.to_csv(f)
