import os
import pandas as pd
import sys
import xlsxwriter

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


def group_by_and_count(df: DataFrame, cols=['Vietnamese'], new_col_name='Occurrences'):
    group = df.groupby(cols)
    group = group.size()
    return group.reset_index(name=new_col_name)


def load_text_file(filename: str, sep='\t'):
    if not os.path.exists(filename):
        raise FileNotFoundError('File not found')
    df = pd.read_csv(filename, index_col=False, sep=sep)
    return df


def read_excel(filename: str, sheet_name: str):
    if os.path.exists(filename):
        return pd.read_excel(filename, sheet_name, index_col=False)
    return None


def export_file(df: DataFrame, filename: str, sep='\t'):
    df.to_csv(filename, index=False, encoding='utf-8', sep=sep)


def export_df_to_excel(dataframe, output_filepath: str, sheet_name: str, auto_fit_width: bool = True):
    '''Xuất DataFrame thành tập tin Excel, có viền và các độ rộng cột vừa khít nội dung'''
    try:
        writer = pd.ExcelWriter(output_filepath,  engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # Tự động thay đổi kích thước cột theo nội dung
        for column in dataframe:
            if auto_fit_width:
                column_length = max(dataframe[column].astype(
                    str).map(len).max(), len(str(column)))
            else:
                column_length = 80
            col_idx = dataframe.columns.get_loc(column)
            worksheet.set_column(col_idx, col_idx, column_length)
        # thêm border và wrap text vào
        format = workbook.add_format(
            {'bottom': 1, 'top': 1, 'left': 1, 'right': 1, 'text_wrap': True})
        worksheet.conditional_format(xlsxwriter.utility.xl_range(
            0, 0, len(dataframe), len(dataframe.columns) - 1), {'type': 'no_errors', 'format': format})
    except:
        print('Xuất tập tin không thành công do lỗi "{}"'.format(
            sys.exc_info()[1]))
        writer.save()
    else:
        print('Xuất tập tin thành công tại đường dẫn ' + output_filepath)
        writer.save()


def sort(df: DataFrame, cols=['Vietnamese', 'Occurrences'], ascending=[True, False]):
    return df.sort_values(by=cols, ascending=ascending)


def filter_aligned_words(aligned_df: DataFrame, crawled_df: DataFrame):
    df = pd.DataFrame(columns=aligned_df.columns)

    # Lấy các giá trị cột đầu tiên thành mảng
    crawled_arr = crawled_df.iloc[:, [0]].values

    total = len(aligned_df)
    for index, row in aligned_df.iterrows():
        # Nếu từ đó có trong danh sách từ crawled_arr
        word = row[0].strip()
        if word in crawled_arr:
            l = len(df)
            df.loc[l] = row
            print_red(f'Đã xử lý xong dòng thứ {index+1}/{total}')
        else:
            print_red(f'Đã bỏ qua dòng thứ {index+1}/{total}')

    return df


# Khai báo các đường dẫn và các biến
crawl_data_folder = os.path.join(os.getcwd(), 'data')
excel_folder = r'C:\Users\La Quoc Thang\OneDrive - dlu.edu.vn\CÔNG VIỆC\TuDienKHoChuru\Dữ liệu'

text_file = os.path.join(crawl_data_folder, 'crawled_text.txt')
tokens_file = os.path.join(crawl_data_folder, 'vi_tokens.txt')
align_file = os.path.join(excel_folder, 'SongNgu_GiongTu_Cần kiểm tra.xlsx')
align_sheet_name = 'Dot 1+2+3'
filtered_align_file = os.path.join(excel_folder, 'SongNgu_GiongTu_Đã lọc.xlsx')

'''
# Dataframe lưu kết quả
result_df = pd.DataFrame(columns=['Vietnamese'])

# Tách từ từ dữ liệu
with open(text_file, 'r', encoding='utf8') as reader:
    count = 0
    for line in reader:
        count += 1
        line = line.strip()
        if line:
            tokens = tokenize(line, lower=True, tokenizer_id=2)
            for token in tokens:
                len_df = len(result_df)
                result_df.loc[len_df] = token

        print_red(f'Đã xử lý dòng thứ {count}')
    print('Đã đọc xong file text')

# Gom nhóm và thêm số đếm
print(result_df)
result_df = group_by_and_count(result_df)
result_df = sort(result_df)
print(result_df)
print(f'Kích thước dữ liệu {len(result_df)}')
export_file(result_df, tokens_file)
print_red('Đã xuất danh sách các từ đã thu thập được')
'''

result_df = load_text_file(tokens_file)

# Lọc các từ đã gióng dựa trên các từ đã thu thập được
aligned_df = read_excel(align_file, align_sheet_name)
result_df = filter_aligned_words(aligned_df, result_df)
export_df_to_excel(result_df, filtered_align_file, align_sheet_name)
print_red('Đã xuất danh sách các từ đã gióng')
