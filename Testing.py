from Crawl_Data_Huffman_Tree_Coding import *
from binary_tree import *
from collections import defaultdict
import time
import sys

byte_array = lambda bit_string: int(bit_string, 2).to_bytes((len(bit_string) + 7) // 8, byteorder='big')
bit_string = lambda byte_array, fill: bin(int.from_bytes(byte_array, byteorder='big'))[2:].zfill(fill)

def Read(f):
    frequencies = defaultdict(lambda: 0)
    with open(f,'r') as f:
        while (read_bytes:= f.read(1)) != '':
            frequencies[read_bytes] += 1

    # print("Finished reading the file.")
    frequencies = (sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return dict(frequencies)

def Save(huffman_tree, path):
    with open(path, "r") as read_r, open("save.txt", 'wb') as write_f:
        bit_tree = "1"+generate_huffman_text(huffman_tree)
        bit_tree += '0'*(8 - bit_tree.__len__()%8)
        table = Char_bit(huffman_tree)
        string = ""
        count = 0
        write_f.write( byte_array(bit_tree) )
        while (read_bytes:= read_r.read(1)) != '':
            string += table[read_bytes]
            if count > 10**6:
                count = 0
                print(time.time())
            if string.__len__() >= 8:
                write_f.write(byte_array(string[:8]))
                string = string[8:]
        write_f.write(byte_array(string))

def Read_decodef(path):
    with open(path, 'rb') as f, open('Orinal_text.txt', 'w') as write_f:
        bit_tree = bit_string(f.read(256*3), 256*3)[1:]
        huffman_tree, excessb = build_tree_from_ascii8(bit_tree)
        excessb = excessb[excessb.__len__()%8:]

        string, excessb = find_char(excessb, huffman_tree)
        write_f.write(string)
        n = 5
        f_read = f.read(n)
        fill = n*8
        while f_read != b"":
            test = f.read(n)
            if test == b'':
                fill = 0
            excessb += bit_string(f_read,fill)
            string, excessb = find_char(excessb, huffman_tree)
            write_f.write(string)
            f_read = test

#Run program
def Zip_text(path):
    begin = time.time()

    #Lấy dữ liệu và đếm
    frequencies = Read(path)
    print('Done counting')

    #Tạo cây, nén cây, bảng mã
    huffmanTr = build_huffman_tree(frequencies)
    print('Done building tree')

    #Lưu
    Save(huffmanTr, path)
    print('Done save')

    #Đọc
    Read_decodef('save.txt')
    print('Done decode')

    end = time.time()
    # Convert seconds to a time structure
    time_struct = time.gmtime(end - begin)

    # Format the time structure to minutes and seconds
    formatted_time = time.strftime("%M:%S", time_struct)
    print(formatted_time)

def create_file(name, huffmanTree):
    with open(name, 'w') as f:
        f.write(generate_huffman_text(huffmanTree))

def sum_dicts(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result:
            result[key] += value
        else:
            result[key] = value
    return result

def crawl_data(link, tag):
    total = {}
    for url, tag in zip(link, tag):
        total = sum_dicts(total, get_fren_web(url, tag))
    print(total)
    huffman = build_huffman_tree(total)
    print(generate_huffman_text(huffman))

def exit():
    sys.exit()

# Tính năng
def Zip():
    path = input("Type path to file: ")
    Zip_text(path)

def Crawl():
    path = input('Type path to file contain url and tag:  ')
    url, tag = [], []
    with open(path, 'r') as f:
        while (data:=f.readline()) != "":
            url.append(data.split()[0])
            tag.append(data.split()[1])
    crawl_data(url, tag)

Func = {
    'Exit': exit,
    'Zip Text': Zip,
    'Make Tree with url and tag': Crawl
}

while True:
    for index, text in enumerate(Func):
        print(str(index)+'.', text)
    choice = int(input('Your choice:  '))
    list(Func.items())[choice][1]()
    print("="*50)