from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
import math

class Trader:
    def __init__(self):
        self.upper_threshold = 80
        self.lower_threshold = 20
        self.rsi_periods = 2

    def calculate_rsi(self, prices):
        if len(prices) < self.rsi_periods + 1:
            return None

        deltas = [prices[i + 1] - prices[i] for i in range(self.rsi_periods)]
        avg_gain = sum(delta for delta in deltas if delta > 0) / self.rsi_periods
        avg_loss = -sum(delta for delta in deltas if delta < 0) / self.rsi_periods
        
        print("avg gain: " + str(avg_gain) + "avg loss: " + str(avg_loss))

        if avg_loss == 0:
            return 100
        if avg_gain == 0:
            return 0

        rs = avg_gain / avg_loss
        print("rs: " + str(rs))
        return 100 - (100 / (1 + rs))

    def run(self, state: TradingState):
        result = {}

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            trades = state.market_trades.get(product, [])
            prices = [trade.price for trade in trades]
            print('\n'.join(map(str, prices)))
                    
            rsi = self.calculate_rsi(prices)
            
            if rsi is None:
                continue

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if rsi > self.upper_threshold:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))

            if len(order_depth.sell_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if rsi < self.lower_threshold:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))

            result[product] = orders
            
        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData
