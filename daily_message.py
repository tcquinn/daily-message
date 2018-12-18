import pandas as pd
import s3fs
import re
import random
import os
import argparse

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

    # Randomly select a message, return the body, and increment the number of times used
    def next_message(self):
        print('Values for number of times used: {}'.format(self.message_list_df['num_times_used'].unique()))
        min_num_times_used = self.message_list_df['num_times_used'].min()
        print('Minimum number of times used: {}'.format(min_num_times_used))
        selectable_indices = self.message_list_df.index[self.message_list_df['num_times_used'] == min_num_times_used].tolist()
        print('Selectable indices: {}'.format(selectable_indices))
        selected_index = random.choice(selectable_indices)
        print('Selected index: {}'.format(selected_index))
        selected_message = self.message_list_df.loc[selected_index, 'body']
        print('Selected message: {}'.format(selected_message))
        self.message_list_df.loc[selected_index, 'num_times_used'] += 1
        return(selected_message)

def parse_html_template_file(
    html_template_path,
    target_html_path,
    message_string):
    message_re = re.compile('@message')
    html_template = open(
        html_template_path,
        'r')
    target_html = open(
        target_html_path,
        'w')
    for input_line in html_template:
        output_line = message_re.sub(message_string, input_line)
        target_html.write(output_line)
    html_template.close()
    target_html.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message_list_bucket_name', type=str, help="Message list S3 bucket_name (e.g., 'daily-message')")
    parser.add_argument('message_list_object_name', type=str, help="Message list S3 object name (e.g., 'sample_message_list.csv')")
    parser.add_argument('html_template_path', type=str, help="HTML template path (e.g., 'html/index_template.html')")
    parser.add_argument('target_html_path', type=str, help="Target HTML path (e.g., 'html/index.html')")
    arguments = parser.parse_args()

    message_list_bucket_name = arguments.message_list_bucket_name
    message_list_object_name = arguments.message_list_object_name
    html_template_path = arguments.html_template_path
    target_html_path = arguments.target_html_path
    print('message_list_bucket_name: {}'.format(message_list_bucket_name))
    print('message_list_object_name: {}'.format(message_list_object_name))
    print('html_template_path: {}'.format(html_template_path))
    print('target_html_path: {}'.format(target_html_path))
    message_list  = MessageList.from_csv_s3_object(
        message_list_bucket_name,
        message_list_object_name)
    print('Successfully read message list:\n{}'.format(message_list.message_list_df))
    selected_message = message_list.next_message()
    print('Selected message: {}'.format(selected_message))
    print('New message list:\n{}'.format(message_list.message_list_df))
    message_list.to_csv_s3_object(
        message_list_bucket_name,
        message_list_object_name)
    parse_html_template_file(
        html_template_path,
        target_html_path,
        selected_message)
