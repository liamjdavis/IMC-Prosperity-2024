from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
from collections import deque
import pandas as pd

class Trader:
    def __init__(self):
        self.buy = -0.2
        self.sell = 0.2
        self.indicators = deque(maxlen=500)
    
    def calculate_derivative(self, sunlight, humidity):
        self.indicators.extend([sunlight + humidity])
        
        if len(self.indicators) < 500:
            print(" Not enough data ")
            return 0.0
        
        oldest_value = self.indicators[0]
        newest_value = self.indicators[-1]
        price_diff = oldest_value - newest_value
        
        price_diff *= 10
        
        print(price_diff)
        return price_diff
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            print(product)
            
            # retrieve humidity and sunlight
            sunlight = state.observations.conversionObservations['ORCHIDS'].sunlight
            humidity = state.observations.conversionObservations['ORCHIDS'].humidity
            
            # normalize sunlight and humidity
            sunlight = (sunlight - 1397.3049) / (4513.9863 - 1397.3049)
            humidity = (humidity - 59.99958) / (97.51327 - 59.99958)
            
            print("Sunlight: " + str(sunlight))
            print("Humidity: " + str(humidity))
            
            derivative = self.calculate_derivative(sunlight, humidity)
            
            if len(order_depth.buy_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                
                if derivative <= self.buy:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
            
            if len(order_depth.sell_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                
                if derivative >= self.sell:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, best_bid_amount))
        
            result[product] = orders
    
        trader_data = "SAMPLE"
        conversions = 1
        return result, conversions, trader_data