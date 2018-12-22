import daily_message
import message_database

if __name__ == '__main__':
    message_database  = message_database.MessageDatabaseCSVLocal()
    selected_message = message_database.next_message()
    print('Selected message: {}'.format(selected_message))
    html_template = daily_message.HTMLTemplateLocal()
    html_template.create_html([{
        'tag': '@message',
        'value': selected_message}])
