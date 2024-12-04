import os

def find_and_delete_unused_images(directory):
    # 遍历目录及其子目录
    for root, _, files in os.walk(directory):
        for file in files:
            # 过滤出文件名包含 "_ts" 和 "_siri" 的图片文件
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')) and ('_ts' in file or '_siri' in file):
                image_path = os.path.join(root, file)
                image_used = False
                
                # 遍历目录下的所有 .js 文件，检查是否引用了该图片文件
                for js_root, _, js_files in os.walk(directory):
                    for js_file in js_files:
                        if js_file.endswith('.js'):
                            js_file_path = os.path.join(js_root, js_file)
                            try:
                                with open(js_file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    if file in content:
                                        image_used = True
                                        break
                            except UnicodeDecodeError:
                                print(f"无法读取文件 {js_file_path}，跳过。")
                                continue
                    if image_used:
                        break
                
                # 如果图片文件没有被引用，则删除该文件，并打印日志
                if not image_used:
                    os.remove(image_path)
                    print(f"Deleted: {image_path}")

# 示例调用
directory = r'D:\Users\louxb1\media\ai\project\msmarthomeapp\app'
find_and_delete_unused_images(directory)