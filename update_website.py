import message_database
import html_template_parser

if __name__ == '__main__':
    message_database  = message_database.MessageDatabaseCSVLocal()
    selected_message = message_database.next_message()
    print('Selected message: {}'.format(selected_message))
    html_template = html_template_parser.HTMLTemplateLocal()
    html_template.create_html([
        {'tag': '@message','value': selected_message['body']},
        {'tag': '@contributor', 'value': selected_message['contributor']}])
