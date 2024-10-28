from PIL import Image
import os
import re


def update_code_references(input_dir, old_filename, new_filename):
    for foldername, subfolders, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith(('.html', '.css', '.js', '.jsx', '.ts', '.tsx')):
                file_path = os.path.join(foldername, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                updated_content = re.sub(re.escape(old_filename), new_filename, content)
                
                if updated_content != content:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)

def convert_images_to_webp_inplace(src_dir, quality, whitelist):
    for foldername, subfolders, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename in whitelist:  # 如果文件名在白名单中，跳过转换逻辑
                continue
            if filename.endswith(('.png', '.jpg', '.jpeg')) and not filename.endswith('.9.png'):
                file_path = os.path.join(foldername, filename)
                img = Image.open(file_path)
                if getattr(img, 'is_animated', False):
                    continue  # 如果图片是动态的，跳过转换逻辑
                
                webp_filename = filename.rsplit('.', 1)[0] + '.webp'
                webp_file_path = os.path.join(foldername, webp_filename)
                
                # 初次转换
                img.save(webp_file_path, 'webp', quality=quality)
                
                # 检查文件大小
                if os.path.getsize(webp_file_path) >= os.path.getsize(file_path):
                    # 使用质量值 80 再次转换
                    img.save(webp_file_path, 'webp', quality=80)
                    
                    # 再次检查文件大小
                    if os.path.getsize(webp_file_path) >= os.path.getsize(file_path):
                        os.remove(webp_file_path)  # 删除转换后的文件
                        continue  # 保留原始文件格式
                
                os.remove(file_path)  # 删除原始图片
                # 更新代码中使用该图片资源的方式
                update_code_references(src_dir, filename, webp_filename)

whitelist = ['image1.png', 'image2.jpg']  # 你的白名单



if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_directory}")
    whitelist_dirs = [r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\helpcenter', 
                  r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\mycenter']  # 你的目录白名单
    for dir_path in whitelist_dirs:
        convert_images_to_webp_inplace(dir_path, 80, whitelist) 



## ## 