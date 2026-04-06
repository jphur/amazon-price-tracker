# Amazon price tracker

Price checker using Playwright that loads an Amazon product page, extracts the price, and sends a notification via Telegram.

Designed for execution on residential IP environments (local/home server) to avoid datacenter IP blocking commonly used by high-security e-commerce sites.

## Requirements

- Python 3.13+
- Docker (optional)
- `playwright`, `python-dotenv`, `httpx`

## Environment variables

Create a `.env` file in the project root with the required values. `TARGET_PRICE` is the threshold used to decide whether to send a Telegram notification.

```ini
URL=https://www.amazon.com/dp/XXXXXXXXXX
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=-1001234567890
TARGET_PRICE=70.00
```

## Local usage

1. Clone the repository:

    ```bash
    git clone <repo-url>
    cd shadow-check
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    python -m pip install playwright python-dotenv httpx
    python -m playwright install chromium
    ```

4. Run the script:

    ```bash
    uv run main.py
    # or if you don't have uv:
    python main.py
    ```

## Current flow

1. `main.py` reads `URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and `TARGET_PRICE` from `.env`.
2. It launches Chromium with a human-like user agent, `es-ES` locale and `Europe/Madrid` timezone.
3. It opens the Amazon homepage first to establish session and cookies.
4. It navigates to the product page and waits for the price section to appear.
5. It extracts the Amazon price and formats it.
6. It prints the product title and price to the console.
7. If the price is below or equal to `TARGET_PRICE`, it sends a Telegram notification.
8. If the price is above the target, it prints that no notification was sent.
9. On failure it takes a screenshot and sends it to Telegram if the bot config is available.

## Docker usage

1. Build the Docker image:

    ```bash
    docker build -t shadow-check .
    ```

2. Run the container with the `.env` file:

    ```bash
    docker run --rm --env-file .env --name shadow-check shadow-check
    ```

3. To debug without automatically removing the container:

    ```bash
    docker run --name shadow-check --env-file .env shadow-check
    docker logs -f shadow-check
    docker rm shadow-check
    ```

## Notes

- The project uses `pyproject.toml` to declare dependencies.
- If the Amazon price selector changes, update the selectors in `main.py`.
