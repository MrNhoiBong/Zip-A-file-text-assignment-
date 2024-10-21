import urllib.request
from bs4 import BeautifulSoup
import re
from collections import Counter

# Hàm lấy dữ liệu từ URL (sử dụng urllib):
def crawl_data_from_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')                                  # Đọc và giải mã dữ liệu thành chuỗi
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu từ URL: {e}")
        return ""

# Hàm loại bỏ code HTML, chỉ giữ lại văn bản trong thẻ chứa nội dung chính:
def clean_html(raw_html, tag):
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Tìm thẻ người dùng chọn (article, content, div,...):
    content = soup.find(class_=tag)                                                 # Thay tag bằng thẻ cụ thể của trang web

    if content:
        text = content.get_text(separator=' ', strip=True)                          # Lấy toàn bộ văn bản và loại bỏ thẻ HTML
    else:
        print(f"Không tìm thấy thẻ {tag}, dùng toàn bộ văn bản trang.")
        text = soup.get_text(separator=' ', strip=True)                             # Lấy toàn bộ văn bản nếu không tìm thấy thẻ

    # Làm mịn văn bản
    text = re.sub(r'\s+', ' ', text)                                        # Thay thế nhiều khoảng trắng thành một khoảng trắng
    return text

# Hàm đếm tần suất xuất hiện của các ký tự ASCII:
def count_ascii_characters(text):
    # Bỏ các ký tự không cần đếm |, <, >:
    text = re.sub(r'[|<>]', '', text)

    # Chỉ giữ các ký tự ASCII (từ 0 đến 255):
    ascii_text = ''.join([char for char in text if ord(char) < 256])

    # Đếm tần suất của các ký tự ASCII:
    frequencies = Counter(ascii_text)

    # Tạo một bảng tần suất cho tất cả các ký tự ASCII (256 ký tự):
    ascii_frequencies = {chr(i): frequencies.get(chr(i), 0) for i in range(256)}

    return ascii_frequencies

# Hàm chia nhóm các ký tự có tần suất gần nhau:
def group_frequencies(frequencies):
    max = list(frequencies.items())[0][0]
    check = list(frequencies.items())[0][0]
    for i in frequencies:
        if frequencies[i] < frequencies[max]*0.7 and frequencies[i] < frequencies[check]*0.8:
            max = i
        else:
            frequencies[i] = frequencies[max]
        check = i
    return frequencies


# Hàm lấy văn bản từ URL và thẻ HTML do người dùng nhập:
def get_text(url, tag):
    raw_html = crawl_data_from_url(url)
    if raw_html:
        print(f"Đã lấy dữ liệu thành công từ {url}")
        return clean_html(raw_html, tag)
    else:
        print(f"Không thể lấy dữ liệu từ URL: {url}")
        return ""


def clean_and_sort_dict(d):
    # Remove keys with value 0
    cleaned_dict = {k: v for k, v in d.items() if v != 0}

    # Sort the dictionary by values
    sorted_dict = dict(sorted(cleaned_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict

def GetData(url, tag):
    # Lấy văn bản từ URL và thẻ người dùng chỉ định:
    cleaned_text = get_text(url, tag)

    if cleaned_text:
        # Đếm tần suất xuất hiện của các ký tự ASCII:
        frequencies = count_ascii_characters(cleaned_text)
        frequencies = clean_and_sort_dict(frequencies)
        return frequencies
    else:
        return False

def get_fren_web(url, tag):
    # Lấy văn bản từ URL và thẻ người dùng chỉ định:
    cleaned_text = get_text(url, tag)

    if cleaned_text:
        # Đếm tần suất xuất hiện của các ký tự ASCII:
        frequencies = count_ascii_characters(cleaned_text)
        frequencies = clean_and_sort_dict(frequencies)

        # Chia các nhóm tần suất gần nhau:
        frequencies = group_frequencies(frequencies)
    return frequencies

# Hàm chính để chạy chương trình:
if __name__ == "__main__":
    # Nhập URL và thẻ HTML từ bàn phím
    url = 'https://edition.cnn.com/2024/10/20/americas/cuba-blackout-third-day-failed-restore-intl/index.html'
    tag = 'article__content'

    # Lấy văn bản từ URL và thẻ người dùng chỉ định:
    cleaned_text = get_text(url, tag)

    if cleaned_text:
        # Đếm tần suất xuất hiện của các ký tự ASCII:
        frequencies = count_ascii_characters(cleaned_text)
        frequencies = clean_and_sort_dict(frequencies)

        # Chia các nhóm tần suất gần nhau:
        frequencies = group_frequencies(frequencies)

        # Trả kết quả dưới dạng dictionary:
        # result_dict = {group: dict(chars) for group, chars in grouped_frequencies.items()}
        print("Kết quả nhóm các ký tự với tần suất gần bằng nhau:", frequencies)
    else:
        print("Không thể lấy văn bản từ URL cung cấp.")