import os
import pandas as pd

from pandas.core.frame import DataFrame
from pyvi import ViTokenizer
from underthesea import word_tokenize
from termcolor import cprint


def print_red(x: str): return cprint(x, 'red')


def ignore_spec_chars(text: str):
    '''Loại bỏ các ký tự không cần thiết'''
    skip_chars = ['-', ':', ',', '.', '+', ';', '<', '>', "'", '*', '!',
                  '(', ')', '"', '/', '‰', '%', '…', '‘', '–', '?', '@', '°']
    return ''.join([c for c in text if c not in skip_chars and not c.isdigit()])


def tokenize(sentence: str, lower: bool = True, tokenizer_id: int = 1):
    '''Tách (các) câu thành các từ/cụm từ dựa trên khoảng trắng (0), pyvi (1) hoặc underthesea (2)'''
    if lower:
        sentence = sentence.lower()

    # Bỏ qua các ký tự không cần thiết
    sentence = ignore_spec_chars(sentence).strip()
    if tokenizer_id == 0:
        tokens = sentence.split()
    elif tokenizer_id == 1:
        tokens = [i.replace('_', ' ')
                  for i in ViTokenizer.tokenize(sentence).split()]
    elif tokenizer_id == 2:
        tokens = word_tokenize(sentence)

    return tokens


def group_by_and_count(df: DataFrame, cols=['Vietnamese'], new_col_name='Occurences'):
    group = df.groupby(cols)
    group = group.size()
    return group.reset_index(name=new_col_name)


def export_file(df: DataFrame, filename: str, sep='\t'):
    df.to_csv(filename, index=False, encoding='utf-8', sep=sep)


def sort(df: DataFrame, cols=['Vietnamese', 'Occurrences'], ascending=[True, False]):
    return df.sort_values(by=cols, ascending=ascending)


data_folder = os.path.join(os.getcwd(), 'data')
text_file = os.path.join(data_folder, 'crawled_text.txt')
tokens_file = os.path.join(data_folder, 'vi_tokens.txt')

result_df = pd.DataFrame(columns=['Vietnamese'])

with open(text_file, 'r', encoding='utf8') as reader:
    len_text = len(reader)
    print_red('Số dòng trong file text là ' + len_text)
    count = 0
    for line in reader:
        count += 1
        line = line.strip()
        if line:
            tokens = tokenize(line, lower=True, tokenizer_id=2)
            len_df = len(result_df)
            result_df.loc[len_df] = tokens
        print_red('Đã xử lý dòng thứ ' + count + '/'+len_text)
    print('Đã đọc xong file text')

result_df = group_by_and_count(result_df)
result_df = sort(result_df)
export_file(result_df, tokens_file)
