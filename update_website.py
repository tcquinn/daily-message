import daily_message
import message_database

if __name__ == '__main__':
    message_database  = message_database.MessageDatabaseCSVS3()
    selected_message = message_database.next_message()
    print('Selected message: {}'.format(selected_message))
    daily_message.parse_html_template_s3_object(selected_message)
