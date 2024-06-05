# import struct
# number = 123456789
# packed_data = struct.pack('i', number)
# print(packed_data)


# import os

# # 获取当前工作目录
# current_directory = os.getcwd()

# # 列出当前目录下的所有文件和目录
# entries = os.listdir(current_directory)

# # 打印所有文件和目录，并区分它们
# for entry in entries:
#     entry_path = os.path.join(current_directory, entry)
#     if os.path.isfile(entry_path):
#         print(f"{entry} 是一个文件")
#     elif os.path.isdir(entry_path):
#         print(f"{entry} 是一个目录")