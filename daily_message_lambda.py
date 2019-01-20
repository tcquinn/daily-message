import daily_message
from message_database import MessageDatabaseCSVS3 as MessageDatabase
# from message_database import MessageDatabaseCSVLocal as MessageDatabase
from message_database import MessageStoreS3 as MessageStore
# from message_database import MessageStoreLocal as MessageStore
from html_template_parser import HTMLTemplateS3 as HTMLTemplate
# from html_template_parser import HTMLTemplateLocal as HTMLTemplate

def update_website_lambda_handler(event, context):
    message_database  = MessageDatabase()
    message_store = MessageStore()
    html_template = HTMLTemplate()
    daily_message.update_website(
        message_database,
        message_store,
        html_template)
