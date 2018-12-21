import daily_message
import message_database
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message_list_bucket_name', type=str, help="Message list S3 bucket_name (e.g., 'daily-message')")
    parser.add_argument('message_list_object_name', type=str, help="Message list S3 object name (e.g., 'sample_message_list.csv')")
    parser.add_argument('html_template_bucket_name', type=str, help="HTML template S3 bucket name (e.g., 'daily-message')")
    parser.add_argument('html_template_object_name', type=str, help="HTML template S3 object name (e.g., 'index_template.html')")
    parser.add_argument('target_html_bucket_name', type=str, help="Target HTML S3 bucket name (e.g., 'example.com')")
    parser.add_argument('target_html_object_name', type=str, help="Target HTML S3 target name (e.g., 'index.html')")
    arguments = parser.parse_args()

    message_list_bucket_name = arguments.message_list_bucket_name
    message_list_object_name = arguments.message_list_object_name
    html_template_bucket_name = arguments.html_template_bucket_name
    html_template_object_name = arguments.html_template_object_name
    target_html_bucket_name = arguments.target_html_bucket_name
    target_html_object_name = arguments.target_html_object_name
    print('message_list_bucket_name: {}'.format(message_list_bucket_name))
    print('message_list_object_name: {}'.format(message_list_object_name))
    print('html_template_bucket_name: {}'.format(html_template_bucket_name))
    print('html_template_object_name: {}'.format(html_template_object_name))
    print('target_html_bucket_name: {}'.format(target_html_bucket_name))
    print('target_html_object_name: {}'.format(target_html_object_name))
    message_list  = message_database.MessageList.from_csv_s3_object(
        message_list_bucket_name,
        message_list_object_name)
    print('Successfully read message list:\n{}'.format(message_list.message_list_df))
    selected_message = message_list.next_message()
    print('Selected message: {}'.format(selected_message))
    print('New message list:\n{}'.format(message_list.message_list_df))
    message_list.to_csv_s3_object(
        message_list_bucket_name,
        message_list_object_name)
    daily_message.parse_html_template_s3_object(
        html_template_bucket_name,
        html_template_object_name,
        target_html_bucket_name,
        target_html_object_name,
        selected_message)
