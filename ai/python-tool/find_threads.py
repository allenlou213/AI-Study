import os
import re

def find_threads(project_dir, output_dir):
    # 正则表达式匹配 "new Thread(" 或 "Thread("
    pattern = re.compile(r'\bnew\s+Thread\(|\bThread\(')

    results = []

    # 遍历项目目录中的所有文件
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.kt') or file.endswith('.java'):
                with open(os.path.join(root, file), 'r', encoding = 'utf-8') as f:
                    lines = f.readlines()

                # 在文件内容中查找匹配的线程创建代码
                for i, line in enumerate(lines, start=1):
                    if pattern.search(line):
                        results.append((os.path.join(root, file), i))

    # 将结果保存到输出目录中
    with open(os.path.join(output_dir, 'threads.txt'), 'w') as f:
        for file, line in results:
            f.write(f'{file}: {line}\n')


def mani():
    project_dir = input("请输入项目目录路径：")
    output_dir = input("请输入输出目录路径：")

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    find_threads(project_dir, output_dir)

if __name__ == "__main__":
    mani()
