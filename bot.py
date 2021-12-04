from events import post_events, setup_subscription
import time

setup_subscription()


if __name__ == "__main__":
    while True:
        post_events("supertrend", "coinbasepro", "ETH/USD")
        time.sleep(60)  # 60 seconds = 1 minute
