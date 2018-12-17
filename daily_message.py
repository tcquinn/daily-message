import pandas as pd
import random
import os
import argparse

class MessageList:
    def __init__(
        self,
        message_list_df):
        self.message_list_df = message_list_df

    # Load message list from CSV file
    @classmethod
    def from_csv_file(
        cls,
        path,
        filename):
        message_list_df = pd.read_csv(
            os.path.join(
                path,
                filename),
            index_col=0)
        return cls(message_list_df)

    def to_csv_file(
        self,
        path,
        filename):
        self.message_list_df.to_csv(
            os.path.join(
                path,
                filename))

    # Randomly select a message, return the body, and increment the number of times used
    def next_message(self):
        print('Values for nmber of times used: {}'.format(self.message_list_df['num_times_used'].unique()))
        min_num_times_used = self.message_list_df['num_times_used'].min()
        print('Minimum number of times used: {}'.format(min_num_times_used))
        selectable_indices = self.message_list_df.index[self.message_list_df['num_times_used'] == min_num_times_used].tolist()
        print('Selectable indices: {}'.format(selectable_indices))
        selected_index = random.sample(selectable_indices, 1)[0]
        print('Selected index: {}'.format(selected_index))
        selected_message = self.message_list_df.loc[selected_index, 'body']
        print('Selected message: {}'.format(selected_message))
        self.message_list_df.loc[selected_index, 'num_times_used'] += 1
        return(selected_message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message_list_filename', type=str, help="Message list filename (e.g., 'sample_message_list.csv')")
    parser.add_argument("-p", "--message-list-path", dest="message_list_path", help="Message list path (e.g., '.')", default=".")
    arguments = parser.parse_args()

    message_list_path = arguments.message_list_path
    print('message_list_path: {}'.format(message_list_path))
    message_list_filename = arguments.message_list_filename
    print('message_list_filename: {}'.format(message_list_filename))
    message_list  = MessageList.from_csv_file(
        message_list_path,
        message_list_filename)
    print('Successfully read message list:\n{}'.format(message_list.message_list_df))
    selected_message = message_list.next_message()
    print('Selected message: {}'.format(selected_message))
    print('New message list:\n{}'.format(message_list.message_list_df))
    message_list.to_csv_file(
        message_list_path,
        message_list_filename)