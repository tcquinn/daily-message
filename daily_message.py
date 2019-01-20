
def update_website(
    message_database,
    message_store,
    html_template):
    selected_message = message_database.next_message()
    print('Selected message: {}'.format(selected_message))
    message_store.put_message(selected_message)
    html_template.create_html([
        {'tag': '@message','value': selected_message['body']},
        {'tag': '@contributor', 'value': selected_message['contributor']}])
