import heapq

# Định nghĩa lớp Node cho cây Huffman
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char  # Ký tự ở nút lá
        self.freq = freq  # Tần suất của ký tự
        self.left = None  # Nhánh trái
        self.right = None  # Nhánh phải

    def __lt__(self, other):
        return self.freq < other.freq


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
def generate_huffman_text(node, text_representation=None):
    if text_representation is None:
        text_representation = []

    if node is not None:
        if node.char is not None:  # Nếu là nút lá (có ký tự)
            text_representation.append(f"1;{format(ord(node.char), '08b')}")  # Mã cho ký tự
        else:  # Nếu không có ký tự, tiếp tục phân chia
            text_representation.append("0")  # Mã cho nhánh trái
            generate_huffman_text(node.left, text_representation)
            text_representation.append("1")  # Mã cho nhánh phải
            generate_huffman_text(node.right, text_representation)

    return text_representation


# Hàm xây dựng lại cây từ chuỗi ASCII8
def build_tree_from_ascii8(bitstream):
    def build_tree(bitstream, index):
        if bitstream[index] == '1':  # Nút lá
            # Đọc tiếp 8 bit để lấy ký tự
            char_bits = bitstream[index + 1: index + 9]
            char = chr(int(char_bits, 2))  # Chuyển đổi mã nhị phân thành ký tự
            node = Node(char=char)  # Tạo nút lá
            return node, index + 9  # Tiến đến vị trí tiếp theo
        elif bitstream[index] == '0':  # Nút nội
            node = Node()  # Tạo nút nội
            node.left, next_index = build_tree(bitstream, index + 1)  # Duyệt nhánh trái
            node.right, next_index = build_tree(bitstream, next_index)  # Duyệt nhánh phải
            return node, next_index  # Trả về nút hiện tại và vị trí tiếp theo

    root, _ = build_tree(bitstream, 0)  # Bắt đầu từ vị trí đầu tiên của bitstream
    return root


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


# Hàm in cây Huffman theo định dạng dễ đọc
def print_huffman_tree(node, indent=""):
    if node is not None:
        if node.char is not None:  # Nút lá
            print(f"{indent}Leaf: '{node.char}'")
        else:  # Nút nội
            print(f"{indent}Node")
            print(f"{indent}├── Left:")
            print_huffman_tree(node.left, indent + "│   ")
            print(f"{indent}└── Right:")
            print_huffman_tree(node.right, indent + "    ")


# Ví dụ sử dụng
frequencies = {
    ' ': 9419, '\n': 2228, 'e': 646, 't': 484, 'i': 465, 'o': 435,
    'a': 412, 's': 404, 'n': 399, 'r': 368, 'l': 231, 'd': 213,
    'h': 201, 'c': 198, 'u': 180, 'g': 120, 'm': 112, 'p': 110,
    'N': 101, 'y': 94, 'C': 90, 'f': 84, 'A': 68, 'S': 68, 'w': 67,
    'T': 59, 'v': 59, 'F': 55, 'b': 55, ',': 51, 'k': 46, 'W': 31,
    '.': 30, '2': 27, 'E': 27, 'I': 27, 'M': 27, 'P': 24, 'D': 23,
    'L': 23, 'V': 21, 'U': 20, '0': 17, 'O': 17, 'H': 16, 'B': 14,
    'Y': 12, '-': 11, 'G': 10, '4': 9, 'R': 9, '1': 8, 'x': 8,
}

# Tạo cây Huffman
huffman_tree = build_huffman_tree(frequencies)

# Bước 1: Mã hóa cây Huffman thành chuỗi ASCII8
huffman_text = generate_huffman_text(huffman_tree)
huffman_text_representation = ''.join([item.replace("1;", "1") for item in huffman_text])
print("Huffman Text Representation (ASCII8):")
print(huffman_text_representation)

# Bước 2: Giải mã lại cây từ chuỗi ASCII8
decoded_huffman_tree = build_tree_from_ascii8(huffman_text_representation)

# Bước 3: In cây Huffman đã được giải mã
print("Huffman Tree decoded from ASCII8 representation:")
print_huffman_tree(decoded_huffman_tree)

# Bước 4: Giải mã văn bản từ cây Huffman
encoded_text = "1101010110..."  # Chuỗi mã hóa để giải mã (cần thay thế bằng chuỗi thực tế)
decoded_text = decode_huffman_tree(decoded_huffman_tree, encoded_text)
print("Decoded Text from Huffman Tree:")
print(decoded_text)
