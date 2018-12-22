import pandas as pd
import boto3
import s3fs
import re
import os

def parse_html_template_file(
    message_string,
    html_template_path = None,
    target_html_path = None):
    if html_template_path is None:
        html_template_path = os.environ['HTML_TEMPLATE_LOCAL_PATH']
    if target_html_path is None:
        target_html_path = os.environ['TARGET_HTML_LOCAL_PATH']
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
    message_string,
    html_template_bucket_name = None,
    html_template_object_name = None,
    target_html_bucket_name = None,
    target_html_object_name = None):
    if html_template_bucket_name is None:
        html_template_bucket_name = os.environ['HTML_TEMPLATE_BUCKET_NAME']
    if html_template_object_name is None:
        html_template_object_name = os.environ['HTML_TEMPLATE_OBJECT_NAME']
    if target_html_bucket_name is None:
        target_html_bucket_name = os.environ['TARGET_HTML_BUCKET_NAME']
    if target_html_object_name is None:
        target_html_object_name = os.environ['TARGET_HTML_OBJECT_NAME']
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
