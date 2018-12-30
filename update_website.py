from message_database import MessageDatabaseCSVS3 as MessageDatabase
# from message_database import MessageDatabaseCSVLocal as MessageDatabase
from message_database import MessageStoreS3 as MessageStore
# from message_database import MessageStoreLocal as MessageStore
from html_template_parser import HTMLTemplateS3 as HTMLTemplate
# from html_template_parser import HTMLTemplateLocal as HTMLTemplate

if __name__ == '__main__':
    message_database  = MessageDatabase()
    selected_message = message_database.next_message()
    print('Selected message: {}'.format(selected_message))
    message_store = MessageStore()
    message_store.put_message(selected_message)
    html_template = HTMLTemplate()
    html_template.create_html([
        {'tag': '@message','value': selected_message['body']},
        {'tag': '@contributor', 'value': selected_message['contributor']}])
