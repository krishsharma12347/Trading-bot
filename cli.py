import argparse
import logging
from bot.orders import place_market_order, place_limit_order

# ─── Logging Setup ──────────────────────────────────────────────
logging.basicConfig(
    filename="logs/orders.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ─── CLI Parser ─────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Trading Bot CLI")
parser.add_argument("--symbol", type=str, required=True, help="Trading pair e.g. BTCUSDT")
parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="BUY or SELL")
parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
parser.add_argument("--price", type=float, help="Price for LIMIT orders")

args = parser.parse_args()

# ─── Order Logic ────────────────────────────────────────────────
try:
    logging.info(f"Order request: {args}")

    if args.type.upper() == "MARKET":
        response = place_market_order(args.symbol, args.side.upper(), args.quantity)
    elif args.type.upper() == "LIMIT":
        if args.price is None:
            raise ValueError("Price required for LIMIT order")
        response = place_limit_order(args.symbol, args.side.upper(), args.quantity, args.price)
    else:
        raise ValueError("Invalid order type")

    logging.info(f"Order response: {response}")

    # ─── Output Formatting ──────────────────────────────────────
    print("\n✅ Order placed successfully!")
    print(f"Order ID: {response.get('orderId')}")
    print(f"Status: {response.get('status')}")
    print(f"Executed Qty: {response.get('executedQty')}")
    print(f"Avg Price: {response.get('avgPrice') or response.get('price')}")

except Exception as e:
    logging.error(f"Error: {e}")
    print(f"❌ Failed to place order: {e}")