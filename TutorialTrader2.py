from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
import math

class Trader:
    def __init__(self):
        self.rsi_periods = 14
        self.upper_threshold = 80
        self.lower_threshold = 20

    def calculate_rsi(self, prices):
        if len(prices) < self.rsi_periods + 1:
            return None

        deltas = [prices[i + 1] - prices[i] for i in range(self.rsi_periods)]
        avg_gain = sum(delta for delta in deltas if delta > 0) / self.rsi_periods
        avg_loss = -sum(delta for delta in deltas if delta < 0) / self.rsi_periods

        if avg_loss == 0:
            return 100
        if avg_gain == 0:
            return 0

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def run(self, state: TradingState):
        result = {}

        for product, order_depth in state.order_depths.items():
            prices = [trade.price for trade in state.market_trades[product]]
            rsi = self.calculate_rsi(prices)

            if rsi is None:
                continue

            if rsi > self.upper_threshold:
                # Overbought condition, place a sell order
                result[product] = [Order(product=product, price=order_depth.bids[0].price, volume=-state.position[product])]
            elif rsi < self.lower_threshold:
                # Oversold condition, place a buy order
                result[product] = [Order(product=product, price=order_depth.asks[0].price, volume=1)]

        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData
