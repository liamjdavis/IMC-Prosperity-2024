from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
import math

class Trader:
    def __init__(self):
        self.rsi_periods = 14

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
        pass