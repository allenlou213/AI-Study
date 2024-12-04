import os
import shutil

def copy_and_delete(whitelist_dirs, common_dir):
    if not os.path.exists(common_dir):
        os.makedirs(common_dir)

    copied_files = set()

    for resource_dir, code_dir in whitelist_dirs.items():
        for root, _, files in os.walk(resource_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file not in copied_files:
                    shutil.copy2(file_path, common_dir)
                    copied_files.add(file)
                os.remove(file_path)
        
        # 遍历对应的代码目录，替换使用资源的文件路径
        for root, _, files in os.walk(code_dir):
            for file in files:
                # 过滤只有特定文件格式
                if not file.endswith(('.html', '.css', '.js', '.jsx', '.ts', '.tsx')):
                    continue
                
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                

                new_content = content.replace('./assets/image/devicesIcon/', '../common/devicesIcon/')
                    
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
# 示例调用
whitelist_dirs = {
    r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\helpcenter\assets\image\devicesIcon': r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\helpcenter',
    r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\mycenter\assets\image\devicesIcon': r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\mycenter',
    r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\mydevices\assets\image\devicesIcon': r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\mydevices',
    r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\service\assets\image\devicesIcon': r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\service',
    r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\setting\assets\image\devicesIcon': r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\setting'
}

common_dir = r'D:\Users\louxb1\media\ai\project\msmarthomebusinesscomponents\app\assets\common\deviceIcon'

copy_and_delete(whitelist_dirs, common_dir)