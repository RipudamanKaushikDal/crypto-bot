from supertrends import check_for_signals

subscribers = dict()


def subscribe(function_name: str, function):
    if function_name not in subscribers:
        subscribers[function_name] = function


def setup_subscription():
    subscribe("supertrend", check_for_signals)


def post_events(function_name: str, exchange_name: str, symbol: str):
    if function_name in subscribers:
        subscribers[function_name](exchange_name, symbol)
    else:
        print("Event not registered yet")
