import os
import requests
from bs4 import BeautifulSoup

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"图片 {url} 下载成功！")
    else:
        print(f"图片 {url} 下载失败！")

def download_all_images(url, save_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    for i, img in enumerate(images):
        img_url = img.get('src')
        if img_url.startswith('http'):
            save_path = os.path.join(save_dir, f'image_{i}.jpg')
            download_image(img_url, save_path)

def main():
    url = input("请输入要爬取的网页URL：")
    save_dir = input("请输入保存图片的文件夹路径：")

    # 创建保存路径的文件夹（如果不存在）
    os.makedirs(save_dir, exist_ok=True)

    download_all_images(url, save_dir)

if __name__ == "__main__":
    main()