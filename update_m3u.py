import cloudscraper
from bs4 import BeautifulSoup
import re

def get_streams():
    # Sử dụng trình giả lập trình duyệt cao cấp hơn
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    
    # Danh sách các trang nguồn có thể lấy (90phut thường có nhiều tên miền phụ)
    source_url = 'https://90phutit.cc/' 
    streams = []
    
    try:
        response = scraper.get(source_url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các khối trận đấu (Cấu trúc này thường dùng cho các trang bóng đá)
        # Chúng ta tìm tất cả các thẻ có khả năng chứa thông tin trận đấu
        matches = soup.select('div.match-item, a.match-link, .item-match') 

        if not matches:
            # Nếu không tìm thấy theo class, tìm tất cả link có chữ 'truc-tiep'
            matches = soup.find_all('a', href=re.compile(r'/truc-tiep/|/match/'))

        for match in matches:
            try:
                # 1. Lấy tiêu đề trận đấu
                title = match.get_text(separator=" ", strip=True)
                if not title or len(title) < 5: continue
                
                # 2. Lấy link xem
                link = match.get('href') if match.name == 'a' else match.find('a')['href']
                if not link.startswith('http'):
                    link = source_url.rstrip('/') + link
                
                # 3. Lấy ảnh logo (nếu có) để MonPlayer hiển thị đẹp hơn
                img = match.find('img')
                logo = img['src'] if img and img.has_attr('src') else ""

                # Định dạng lại tiêu đề cho đẹp: [Giờ] Đội A vs Đội B
                clean_title = re.sub(r'\s+', ' ', title).strip()
                
                streams.append({
                    'title': clean_title,
                    'link': link,
                    'logo': logo
                })
            except:
                continue
                
        return streams
    except Exception as e:
        print(f"Lỗi cào dữ liệu: {e}")
        return []

def save_to_m3u(data):
    with open('playlist.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for item in data:
            # Thêm logo và định dạng chuẩn IPTV
            f.write(f'#EXTINF:-1 tvg-logo="{item["logo"]}", {item["title"]}\n')
            f.write(f"{item['link']}\n")

if __name__ == "__main__":
    print("Đang quét dữ liệu bóng đá mới nhất...")
    data = get_streams()
    save_to_m3u(data)
    print(f"Thành công! Đã cập nhật {len(data)} trận đấu vào playlist.")
