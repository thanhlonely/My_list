import requests
from bs4 import BeautifulSoup

# Cấu hình
SOURCE_URL = 'https://trang-web-chi-dinh.com' # Thay bằng trang bạn muốn lấy
OUTPUT_FILE = 'playlist.m3u'

def get_streams():
    try:
        response = requests.get(SOURCE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Logic tìm link: Bạn cần tùy chỉnh phần này dựa trên cấu trúc trang web
        # Ví dụ: Tìm tất cả các thẻ <a> có chứa link .m3u8
        streams = []
        for a in soup.find_all('a', href=True):
            if '.m3u8' in a['href']:
                title = a.text.strip() or "Kênh không tên"
                link = a['href']
                streams.append((title, link))
        return streams
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        return []

def save_to_m3u(streams):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for title, link in streams:
            f.write(f"#EXTINF:-1, {title}\n")
            f.write(f"{link}\n")

if __name__ == "__main__":
    data = get_streams()
    if data:
        save_to_m3u(data)
        print("Đã cập nhật file .m3u thành công!")
