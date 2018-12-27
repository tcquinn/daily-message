from message_database import MessageDatabaseCSVS3 as MessageDatabase
# from message_database import MessageDatabaseCSVLocal as MessageDatabase
from html_template_parser import HTMLTemplateS3 as HTMLTemplate
# from html_template_parser import HTMLTemplateLocal as HTMLTemplate

def update_website_lambda_handler(event, context):
    message_database  = MessageDatabase()
    selected_message = message_database.next_message()
    print('Selected message: {}'.format(selected_message))
    html_template = HTMLTemplate()
    html_template.create_html([
        {'tag': '@message','value': selected_message['body']},
        {'tag': '@contributor', 'value': selected_message['contributor']}])
