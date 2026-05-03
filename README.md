# Amazon price tracker

Simple price checker using `httpx` and `regex` that loads an Amazon product page, extracts the price, and sends a notification via Telegram.

Designed for execution on residential IP environments (local/home server) to avoid datacenter IP blocking commonly used by high-security e-commerce sites.

## Requirements

- Python 3.13+
- `uv` (recommended for dependency management)
- `httpx`, `python-dotenv`

## Environment variables

Create a `.env` file in the project root with the required values:

```ini
URL=https://www.amazon.es/dp/XXXXXXXXXX
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100...
TARGET_PRICE=70.00
```

## Local usage

1. Clone the repository and navigate to it:

    ```bash
    git clone <repo-url>
    cd amazon-price-tracker
    ```

2. Install dependencies (using `uv`):

    ```bash
    uv sync
    ```

3. Run the script:

    ```bash
    uv run main.py
    ```

## How it works

1. `main.py` reads configuration from `.env`.
2. It makes an HTTP request to the Amazon product page using `httpx` with a custom User-Agent.
3. It uses regular expressions (`re`) to extract the product title and price from the HTML.
4. If the price is below or equal to `TARGET_PRICE`, it sends a message via the Telegram Bot API.
5. In case of failure, it saves the HTML to `error_page.html` for debugging.

## Docker usage

1. Build the image:

    ```bash
    docker build -t amazon-tracker .
    ```

2. Run the container:

    ```bash
    docker run --rm --env-file .env amazon-tracker
    ```

## Notes

- This version does not depend on Playwright or any heavy browser automation, making it much faster and lightweight.
- If Amazon changes its page structure, the regular expressions in `main.py` might need adjustment.
