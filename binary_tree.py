import heapq
from collections import defaultdict

# Định nghĩa lớp Node cho cây Huffman
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char  # Ký tự ở nút lá
        self.freq = freq  # Tần suất của ký tự
        self.left = None  # Nhánh trái
        self.right = None  # Nhánh phải

    def __lt__(self, other):
        return self.freq < other.freq

    def __getPar__(self):
        return "".join(["0" if self.left.char==None else "1" , "0" if self.right.char==None else "1"])


# Hàm xây dựng cây Huffman từ tần suất ký tự
def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


# Hàm mã hóa cây Huffman thành chuỗi ASCII8
def generate_huffman_text(node):
    Queue = [node]
    Bit_tree = ""
    while len(Queue) > 0:
        if Queue[0].char != None:
            Bit_tree += str(bin(ord(Queue[0].char))[2:].zfill(8))
            Queue.pop(0)
        else:
            Bit_tree += Queue[0].__getPar__()
            Queue.insert(1, Queue[0].right)
            Queue.insert(1, Queue[0].left)
            Queue.pop(0)
    return Bit_tree

# Hàm xây dựng lại cây từ chuỗi ASCII8
def build_tree_from_ascii8(bitstream):
    root = bitstream[:2]
    bitstream = bitstream[2:]
    huffman_tree = Node()
    huffman_tree.left = Node()
    huffman_tree.right = Node()
    waiting=[[huffman_tree.left, root[0]], [huffman_tree.right, root[1]]]
    while bitstream.__len__()>0:
        check = waiting.pop(0)
        if check[1] == "1":
            get_char = bitstream[:8]
            bitstream = bitstream[8:]
            check[0].char = chr(int(get_char, 2))
            if waiting.__len__()==0: break
        else:
            bit_state = bitstream[:2]
            bitstream = bitstream[2:]
            check[0].left = Node()
            check[0].right = Node()
            waiting.insert(0,[check[0].right, bit_state[1]])
            waiting.insert(0,[check[0].left, bit_state[0]])
    return huffman_tree, bitstream

# Hàm giải mã văn bản từ cây Huffman
def decode_huffman_tree(node, encoded_text):
    decoded_output = []
    current_node = node

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:  # Nếu đã đến nút lá
            decoded_output.append(current_node.char)  # Thêm ký tự vào kết quả
            current_node = node  # Quay về gốc cây

    return ''.join(decoded_output)

def Char_bit(huffman_tree):
    char_bit = defaultdict(lambda :"")
    Stack = [['0',huffman_tree.left], ['1', huffman_tree.right]]
    while Stack != []:
        tem = Stack.pop(0)
        if tem[1].char != None:
            char_bit[tem[1].char] = tem[0]
        else:
            Stack.append([tem[0]+"0", tem[1].left])
            Stack.append([tem[0]+"1", tem[1].right])

    return dict(char_bit)

def find_char(bit, huffman_tree):
    current = huffman_tree
    string = ''
    k = 0
    for i, pos in zip(bit, range(len(bit))):
        if i=="1":
            current = current.right
        else:
            current = current.left
        if current.char != None:
            string += current.char
            current = huffman_tree
            k = pos

    return string, bit[k+1:]


# Hàm in cây Huffman theo định dạng dễ đọc
def print_huffman_tree(node, indent=""):
    if node is not None:
        if node.char is not None:  # Nút lá
            print(f"{indent}char: '{node.char}'")
        else:  # Nút nội
            # print(f"{indent}Node")
            print(f"{indent}├── Left:")
            print_huffman_tree(node.left, indent + "│   ")
            print(f"{indent}└── Right:")
            print_huffman_tree(node.right, indent + "    ")

if __name__=="__main__":
    # Ví dụ sử dụng
    frequencies = {'j': 2, 'q': 2, '5': 1, 'L': 1, 'z': 1}

    # Tạo cây Huffman
    huffman_tree = build_huffman_tree(frequencies)
    print_huffman_tree(huffman_tree)
    # print_huffman_tree(huffman_tree)
    print(find_char("11", huffman_tree))

    # Bước 1: Mã hóa cây Huffman thành chuỗi ASCII8
    # huffman_text = generate_huffman_text(huffman_tree)
    # print("Huffman Text Representation (ASCII8):")
    # print(huffman_text)

    # Bước 2: Giải mã lại cây từ chuỗi ASCII8
    # decoded_huffman_tree = build_tree_from_ascii8(huffman_text)
    # print_huffman_tree(decoded_huffman_tree)

    # # Bước 3: In cây Huffman đã được giải mã
    # print("Huffman Tree decoded from ASCII8 representation:")
    # print_huffman_tree(decoded_huffman_tree)
    #
    # # Bước 4: Giải mã văn bản từ cây Huffman
    # encoded_text = "1101010110..."  # Chuỗi mã hóa để giải mã (cần thay thế bằng chuỗi thực tế)
    # decoded_text = decode_huffman_tree(decoded_huffman_tree, encoded_text)
    # print("Decoded Text from Huffman Tree:")
    # print(decoded_text)
