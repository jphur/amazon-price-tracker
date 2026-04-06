from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

def getCleanedPrice(page, selector) -> str:
    return page.locator(selector).first.inner_text().replace(".", "").replace("\n", "").strip()

with sync_playwright() as p:
    # 1. Launch with a human-like User-Agent
    browser = p.chromium.launch()
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        locale="es-ES",
        timezone_id="Europe/Madrid"
    )
    page = context.new_page()
    # 2. Navigate to Amazon homepage to establish session and cookies
    page.goto("https://www.amazon.es", wait_until="domcontentloaded")
    

    try:
        url = os.environ["URL"]
        print("Navigating to product page...")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector(".a-price-whole", timeout=10000)
        
        # 3. Extraction
        productTitle = page.locator("span#productTitle").inner_text().strip()
        price_container = "#corePrice_feature_div"
        integer = getCleanedPrice(page, f"{price_container} .a-price-whole").replace(".", "")
        fraction = getCleanedPrice(page, f"{price_container} .a-price-fraction")
        price = float(f"{integer}{fraction}".replace(",", "."))
        print("--- RESULT ---")
        print(f"Product: {productTitle}")
        print(f"Price: {price}")
        print("-----------------")

        # 4. Send Telegram notification if price is below target
        target_price = float(os.environ["TARGET_PRICE"])
        if price <= target_price:
            res = httpx.post(
                f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
                json={
                "chat_id": os.environ["TELEGRAM_CHAT_ID"],
                "text": f"The current price of the product '{productTitle}' is: {price}"
            })
            print(f"Telegram res status: {res.status_code}")
        else:
            print(f"Price is above target ({target_price}), no notification sent.")

    except Exception as e:
        print(f"failure: {e}")
        # Take a screenshot for debugging
        page.screenshot(path="error.png")
        
        with open("error.png", "rb") as f:
            httpx.post(
                f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendPhoto",
                data={"chat_id": os.environ["TELEGRAM_CHAT_ID"]},
                files={"photo": f}
            )
    finally:
        browser.close()