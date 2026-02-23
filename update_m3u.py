import requests
from bs4 import BeautifulSoup
import re

# Giả lập trình duyệt để không bị chặn
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://90phutit.cc/'
}

SOURCE_URL = 'https://90phutit.cc/'
OUTPUT_FILE = 'playlist.m3u'

def get_streams():
    streams = []
    try:
        response = requests.get(SOURCE_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Tìm các trận đấu đang diễn ra (thường nằm trong thẻ có class liên quan đến 'match' hoặc 'item')
        # Lưu ý: Cấu trúc class có thể thay đổi theo thời gian
        items = soup.find_all(['div', 'a'], class_=re.compile(r'match|item|live', re.I))

        for item in items:
            title = ""
            link = ""
            
            # Lấy tên trận đấu
            name_tag = item.find(['h3', 'span', 'p'], class_=re.compile(r'name|title', re.I))
            if name_tag:
                title = name_tag.get_text(strip=True)
            
            # Lấy link chi tiết trận đấu
            if item.name == 'a' and item.has_attr('href'):
                link = item['href']
            else:
                a_tag = item.find('a', href=True)
                if a_tag:
                    link = a_tag['href']

            if title and link:
                # Đảm bảo link là tuyệt đối
                if link.startswith('/'):
                    link = SOURCE_URL.rstrip('/') + link
                
                # Vì link trực tiếp .m3u8 thường bị ẩn sâu trong iframe, 
                # ở mức độ đơn giản, ta sẽ lưu link trang xem trực tiếp.
                # Nếu muốn lấy .m3u8, cần một bước xử lý Selenium/Headless Browser phức tạp hơn.
                streams.append((title, link))

        # Loại bỏ các link trùng lặp
        return list(set(streams))

    except Exception as e:
        print(f"Lỗi: {e}")
        return []

def save_to_m3u(streams):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for title, link in streams:
            f.write(f"#EXTINF:-1, {title}\n")
            f.write(f"{link}\n")

if __name__ == "__main__":
    print("Đang quét dữ liệu từ 90phut...")
    data = get_streams()
    if data:
        save_to_m3u(data)
        print(f"Thành công! Đã tìm thấy {len(data)} trận đấu.")
    else:
        print("Không tìm thấy dữ liệu hoặc bị chặn.")
