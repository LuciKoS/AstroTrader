import random
import time
import datetime
from ib_insync import IB, Stock, MarketOrder
from fetchastro import astrobuy, astrosell

def get_available_stocks_from_file(filename="/Users/lucbaumeler/documents/eth/vscode/projects/astrotrader/top_1000_companies.txt"):
    stocks = []
    try:
        with open(filename, "r") as f:
            for line in f:
                ticker = line.strip()
                if ticker:
                    stocks.append(Stock(ticker, 'SMART', 'USD'))
    except Exception as e:
        print("Error reading file:", e)
    return stocks

def get_available_cash(ib):
    summary = ib.accountSummary()
    for item in summary:
        if item.tag == 'AvailableFunds':
            try:
                return float(item.value)
            except Exception:
                pass
    return 0.0

def trading_bot():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    MIN_CASH_THRESHOLD = 10000.0

    # Decide how many shares to buy each time. For example, 10 shares.
    # Adjust as needed based on your risk and account size.
    FIXED_QUANTITY = 1000

    while True:
        available_cash = get_available_cash(ib)
        print(f"Available cash: {available_cash:.2f}")

        # Try to buy if we have more than a threshold of available cash
        if available_cash > MIN_CASH_THRESHOLD:
            stocks = get_available_stocks_from_file()
            if not stocks:
                print("No stocks available in file, sleeping...")
                time.sleep(60)
                continue

            # Shuffle the stocks and pick one using astrobuy
            random.shuffle(stocks)
            num_stocks = len(stocks)
            buy_ratio = astrobuy(num_stocks)  # returns float between 0 and 1
            buy_index = int(buy_ratio * num_stocks)
            if buy_index >= num_stocks:
                buy_index = num_stocks - 1

            chosen_stock = stocks[buy_index]
            print(f"Chosen stock to BUY: {chosen_stock.symbol}")

            # Instead of checking the market price, we place a MarketOrder for a fixed quantity
            order = MarketOrder('BUY', FIXED_QUANTITY)
            trade = ib.placeOrder(chosen_stock, order)
            print(f"Placed BUY order for {FIXED_QUANTITY} shares of {chosen_stock.symbol}")
            time.sleep(2)

        else:
            # If we have little liquidity, we do the sell/buy cycle
            positions = ib.positions()
            if positions:
                num_positions = len(positions)
                sell_ratio = astrosell(num_positions)
                sell_index = int(sell_ratio * num_positions)
                if sell_index >= num_positions:
                    sell_index = num_positions - 1

                pos = positions[sell_index]
                contract = pos.contract
                pos_qty = pos.position

                # If pos_qty is positive, SELL. If negative, BUY to cover
                if pos_qty > 0:
                    action = 'SELL'
                    qty = pos_qty
                else:
                    action = 'BUY'
                    qty = abs(pos_qty)

                print(f"Chosen stock to SELL: {contract.symbol}, qty={qty}")
                order = MarketOrder(action, qty)
                ib.placeOrder(contract, order)
                time.sleep(2)

                # After selling, try to buy another random stock with all available cash
                new_cash = get_available_cash(ib)
                if new_cash > MIN_CASH_THRESHOLD:
                    stocks = get_available_stocks_from_file()
                    if stocks:
                        random.shuffle(stocks)
                        num_stocks = len(stocks)
                        buy_ratio = astrobuy(num_stocks)
                        buy_index = int(buy_ratio * num_stocks)
                        if buy_index >= num_stocks:
                            buy_index = num_stocks - 1

                        chosen_stock = stocks[buy_index]
                        print(f"Chosen stock to BUY after selling: {chosen_stock.symbol}")

                        # Place a fixed-quantity BUY again
                        order = MarketOrder('BUY', FIXED_QUANTITY)
                        ib.placeOrder(chosen_stock, order)
                        print(f"Placed BUY order for {FIXED_QUANTITY} shares of {chosen_stock.symbol}")
            # Sleep an hour before the next cycle
            time.sleep(3600)

        time.sleep(1)

if __name__ == "__main__":
    trading_bot()