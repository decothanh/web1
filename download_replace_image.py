import os
import re
import requests

# Đảm bảo đã có thư mục images
os.makedirs('images', exist_ok=True)

# Đọc nội dung file index2.html
with open('index2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Tìm tất cả các link ảnh từ genspark.site
pattern = r'(https://genspark\.site/[\w/\.\-\_]+(?:jpg|jpeg|png|gif))'
links = re.findall(pattern, html)
print(f"Found {len(links)} images.")

for link in set(links):
    filename = link.split('/')[-1]
    local_path = f'images/{filename}'

    # Tải ảnh nếu chưa có
    if not os.path.exists(local_path):
        print(f"Downloading {link} ...")
        try:
            resp = requests.get(link)
            if resp.status_code == 200:
                with open(local_path, 'wb') as img_f:
                    img_f.write(resp.content)
            else:
                print(f"Failed to download {link}")
        except Exception as e:
            print(f"Error: {e}")

    # Thay link trong HTML
    html = html.replace(link, local_path)

# Ghi đè lại file index2.html
with open('index2.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Đã hoàn thành download và thay thế đường dẫn ảnh.")
