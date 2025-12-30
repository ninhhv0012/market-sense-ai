import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def extract_content_from_url(url: str) -> str:
    """
    Hàm đơn giản để lấy text từ URL.
    Trong thực tế production, nên dùng thư viện như 'trafilatura' hoặc 'newspaper3k'.
    """
    try:
        # Giả lập User-Agent để tránh bị chặn bởi một số website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise lỗi nếu status code là 4xx hoặc 5xx

        soup = BeautifulSoup(response.content, 'html.parser')

        # Loại bỏ các thẻ không cần thiết (script, style, nav, footer)
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Lấy text và làm sạch khoảng trắng thừa
        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())

        if len(clean_text) < 100:
            raise ValueError("Nội dung bài viết quá ngắn hoặc không cào được.")

        return clean_text

    except Exception as e:
        logger.error(f"Scraping error for {url}: {str(e)}")
        raise e