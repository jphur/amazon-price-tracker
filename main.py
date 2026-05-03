import os
import re
from dotenv import load_dotenv
import httpx

load_dotenv()

def get_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }
    
    with httpx.Client(headers=headers, follow_redirects=True) as client:
        response = client.get(url)
        return response.text

def parse_product_data(html):
    title_match = re.search(r'<span id="productTitle"[^>]*>\s*(.*?)\s*</span>', html, re.DOTALL)
    product_title = title_match.group(1).strip()

    price_whole_match = re.search(r'<span class="a-price-whole">(.*?)</span>', html)
    price_fraction_match = re.search(r'<span class="a-price-fraction">(.*?)</span>', html)

    integer = re.sub(r'[^\d]', '', price_whole_match.group(1))
    fraction = re.sub(r'[^\d]', '', price_fraction_match.group(1)) if price_fraction_match else "00"
    price = float(f"{integer}.{fraction}")

    return product_title, price

def main():
    try:
        url = os.environ.get("URL")
        target_price_env = os.environ.get("TARGET_PRICE")
        print("Fetching product...")
        html = get_product_data(url)
        
        print("Parsing data...")
        product_title, price = parse_product_data(html)
        
        print(f"--- RESULT ---\nProduct: {product_title}\nPrice: {price}€\n--------------")
        if target_price_env and price <= float(target_price_env):
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            
            if bot_token and chat_id:
                print("Sending Telegram notification...")
                httpx.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"✅ Price Alert!\nProduct: {product_title}\nCurrent Price: {price}€"
                    }
                )
                print("Telegram notification sent.")

    except Exception as e:
        print(f"Failure: {e}")
        with open("error_page.html", "w", encoding="utf-8") as f:
            f.write(html if 'html' in locals() else "No HTML fetched.")

if __name__ == "__main__":
    main()