import pandas as pd
import boto3
import s3fs
import re
import os

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

def parse_html_template_s3_object(
    html_template_bucket_name,
    html_template_object_name,
    target_html_bucket_name,
    target_html_object_name,
    message_string):
    s3 = boto3.resource('s3')
    html_template_object = s3.Object(
        html_template_bucket_name,
        html_template_object_name)
    html_template_string = html_template_object.get()['Body'].read().decode('utf-8')
    print('HTML template string:\n{}'.format(html_template_string))
    message_re = re.compile('@message')
    output_string = message_re.sub(message_string, html_template_string)
    print('HTML output string:\n{}'.format(output_string))
    target_html_object = s3.Object(
        target_html_bucket_name,
        target_html_object_name)
    target_html_object.put(
        Body=output_string.encode('utf-8'),
        ContentType='string')
