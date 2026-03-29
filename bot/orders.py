import os
from decimal import Decimal, ROUND_DOWN
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET, testnet=True)


# ─── Precision Helpers ────────────────────────────────────────────────────────

def get_symbol_filters(symbol: str) -> dict:
    """Fetch and return LOT_SIZE and PRICE_FILTER for a futures symbol."""
    info = client.futures_exchange_info()
    for s in info["symbols"]:
        if s["symbol"] == symbol:
            filters = {f["filterType"]: f for f in s["filters"]}
            return {
                "stepSize": filters["LOT_SIZE"]["stepSize"],
                "tickSize": filters["PRICE_FILTER"]["tickSize"],
                "minQty": filters["LOT_SIZE"]["minQty"],
                "maxQty": filters["LOT_SIZE"]["maxQty"],
                "minPrice": filters["PRICE_FILTER"]["minPrice"],
            }
    raise ValueError(f"Symbol '{symbol}' not found on Binance Futures.")


def adjust_precision(value: float, step: str) -> str:
    """
    Round `value` down to the precision defined by `step` (e.g. '0.001').
    Returns a string suitable for the Binance API.
    """
    d_value = Decimal(str(value))
    d_step = Decimal(step)
    adjusted = (d_value // d_step) * d_step
    # Match decimal places of step
    decimal_places = d_step.normalize().as_tuple().exponent
    if decimal_places < 0:
        fmt = Decimal(10) ** decimal_places
        return str(adjusted.quantize(fmt, rounding=ROUND_DOWN))
    return str(int(adjusted))


# ─── Order Functions ──────────────────────────────────────────────────────────

def place_market_order(symbol: str, side: str, quantity: float) -> dict:
    """
    Place a MARKET order on Binance Futures.

    Args:
        symbol:   e.g. 'BTCUSDT'
        side:     'BUY' or 'SELL'
        quantity: raw quantity (will be precision-adjusted automatically)

    Returns:
        Raw JSON response dict from Binance.

    Raises:
        BinanceAPIException: on API-level errors.
        ValueError: if symbol is invalid.
    """
    filters = get_symbol_filters(symbol)
    qty_str = adjust_precision(quantity, filters["stepSize"])

    response = client.futures_create_order(
        symbol=symbol,
        side=side.upper(),
        type="MARKET",
        quantity=qty_str,
    )
    return response


def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    """
    Place a LIMIT GTC order on Binance Futures.

    Args:
        symbol:   e.g. 'BTCUSDT'
        side:     'BUY' or 'SELL'
        quantity: raw quantity (will be precision-adjusted automatically)
        price:    limit price (will be precision-adjusted automatically)

    Returns:
        Raw JSON response dict from Binance.

    Raises:
        BinanceAPIException: on API-level errors.
        ValueError: if symbol is invalid.
    """
    filters = get_symbol_filters(symbol)
    qty_str = adjust_precision(quantity, filters["stepSize"])
    price_str = adjust_precision(price, filters["tickSize"])

    response = client.futures_create_order(
        symbol=symbol,
        side=side.upper(),
        type="LIMIT",
        timeInForce="GTC",
        quantity=qty_str,
        price=price_str,
    )
    return response