import cloudscraper
from bs4 import BeautifulSoup
import re

def get_streams():
    # Sử dụng cloudscraper để vượt qua Cloudflare của các trang bóng đá
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    source_url = 'https://90phutit.cc/'
    streams = []
    
    try:
        response = scraper.get(source_url, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các link trận đấu
        for a in soup.find_all('a', href=True):
            link = a['href']
            # Lọc các link có khả năng là trận đấu (tùy biến theo cấu trúc trang)
            if '/truc-tiep/' in link or 'match' in link:
                title = a.get_text(strip=True) or "Trận đấu đang diễn ra"
                if not link.startswith('http'):
                    link = source_url.rstrip('/') + link
                streams.append((title, link))
        
        return list(set(streams)) # Xóa trùng lặp
    except Exception as e:
        print(f"Lỗi rồi: {e}")
        return []

def save_to_m3u(data):
    with open('playlist.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for title, link in data:
            f.write(f"#EXTINF:-1, {title}\n{link}\n")

if __name__ == "__main__":
    data = get_streams()
    save_to_m3u(data)
    print(f"Đã tìm thấy {len(data)} link!")
