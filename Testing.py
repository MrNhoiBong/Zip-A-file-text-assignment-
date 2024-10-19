import struct

def bytes_to_bits_binary(byte_data):
    bits_data = bin(int.from_bytes(byte_data, byteorder='big'))[2:]
    return bits_data

datas = []
with open('hello.docx', 'rb') as f:
    data = f.read()
    while data:
        datas.append(data)
        data = f.read()

# print(f"Bytes data: {datas}")
# for i in datas:
#     print(f"Bits data: { bytes_to_bits_binary(i) }")

Bytes = datas[0]
print(Bytes)
