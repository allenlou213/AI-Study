import os

def delete_files_in_whitelisted_dirs(whitelist_dirs):
    for dir_path in whitelist_dirs:
        print(f"Deleting files in {dir_path}")
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                print(f"Deleting {file_path}")
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        print(f"unlink {file_path}")
                        os.unlink(file_path)  # 取消注释以实际删除文件
                    elif os.path.isdir(file_path):
                        print(f"Deleting {file_path}")
                        os.rmdir(file_path)  # 取消注释以实际删除目录
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

# 示例调用
if __name__ == "__main__":
    whitelist_dirs = ["path/to/dir1", "path/to/dir2"]
    delete_files_in_whitelisted_dirs(whitelist_dirs)