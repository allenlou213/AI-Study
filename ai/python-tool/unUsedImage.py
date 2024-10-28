import os
import re
import shutil

# Step 1: 从用户那里获取 Android 工程的根目录
project_dir = input("Enter the path to your Android project directory: ")

# Step 2: 遍历工程中的所有目录，找出所有的图片文件
image_files = []
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')) and 'asset' not in root and file.endswith('.9.png') == False:
            full_file_path = os.path.join(root, file)
            print("Checking image: ", full_file_path)
            image_files.append(full_file_path)
            # image_files.append(os.path.splitext(file)[0])

# Step 3: 遍历项目中的所有 .java, .xml 和 .js 文件
project_dir = input("Enter the path to your project directory: ")
java_xml_js_files = [os.path.join(root, f) for root, dirs, files in os.walk(project_dir) 
                     for f in files if f.endswith(('.java', '.kt','.xml' , '.js')) and '.idea' not in root 
                     and '.git' not in root
                     and '.gradle' not in root
                     and 'build' not in root]

# 创建一个集合，用于存储被引用的图片资源
referenced_images = set()

for java_xml_js_file in java_xml_js_files:
    with open(java_xml_js_file, 'r', encoding= 'utf-8') as file:
        content = file.read()
        for image_file in image_files:
            # 假设 image_file 和 content 已经定义
            image_file_name = os.path.splitext(os.path.basename(image_file))[0]
            # 转义文件名以便在正则表达式中使用
            escaped_image_file_name = re.escape(image_file_name)
            # 检查 content 中是否存在文件名
            if re.search(r'@drawable/' + escaped_image_file_name, content) or re.search(escaped_image_file_name, content):
                referenced_images.add(image_file)

# Step 3: 找出未被引用的图片资源
unused_images = set(image_files) - referenced_images

# 输出未使用的图片资源到指定的日志文件
log_dir = r"E:\资源"
log_file_path = os.path.join(log_dir, 'unused_images.txt')
with open(log_file_path, 'w') as log_file:
    for image in unused_images:
        full_image_path = os.path.join(project_dir, image)
        log_file.write(full_image_path + '\n')

# 复制并删除未使用的图片资源到指定的目录
for unused_image in unused_images:
    source_path = os.path.join(project_dir, unused_image)
    os.remove(source_path)  # 删除未使用的图片资源
