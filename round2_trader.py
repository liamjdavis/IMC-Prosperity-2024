from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
from collections import deque
import pandas as pd

class Trader:
    def __init__(self):
        # orchid stuff
        self.orchid_buy = -5
        self.orchid_sell = 5
        self.OPI = []
        self.first_derivative_OPI = deque(maxlen=100)
        
        # amethyst stuff
        self.amethyst_buyprice = 9998
        self.amethyst_sellprice = 10002
        
        # starfruit stuff
        self.starfruit_prices = deque(maxlen=100)
        self.roc_buy = -5
        self.roc_sell = 5
    
    def calculate_roc(self, product: str, state: TradingState) -> float:
        trades = state.market_trades.get(product, [])
        prices = [trade.price for trade in trades]
        self.starfruit_prices.extend(prices)

        if len(self.starfruit_prices) < 2:
            print("Not enough data points")
            return 0.0
        
        roc = (self.starfruit_prices[-1] - self.starfruit_prices[0]) / self.starfruit_prices[0] * 100
        return roc
    
    def calculate_OPI(self, sunlight, humidity):
        scaled_sunlight = ((sunlight - 1397) / (4513 - 1397)) * 10
        scaled_humidity = (humidity / 100) * 10

        if scaled_sunlight < 5.83:
            sunlight_factor = -0.04 * (5.83 - scaled_sunlight)
        else:
            sunlight_factor = 0.04 * (scaled_sunlight - 5.83)

        if humidity < 60:
            humidity_factor = -0.02 * ((60 - humidity) / 5)
        elif humidity > 80:
            humidity_factor = -0.02 * ((humidity - 80) / 5)
        else:
            humidity_factor = 0

        OPI = (scaled_sunlight * sunlight_factor) + (scaled_humidity * humidity_factor)
        self.OPI.append(OPI)

    def calculate_first_derivative(self):
        if len(self.OPI) >= 2:
            self.first_derivative_OPI.clear()
            for i in range(1, len(self.OPI)):
                diff = self.OPI[i] - self.OPI[i - 1]
                self.first_derivative_OPI.append(diff)
    
    def calculate_second_derivative(self):
        if len(self.first_derivative_OPI) >= 2:
            return self.first_derivative_OPI[-1] - self.first_derivative_OPI[0]
        else:
            return 0.0
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            
            if product == "AMETHYSTS":
                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if best_ask <= self.amethyst_buyprice:
                        orders.append(Order(product, best_ask, -best_ask_amount))

                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if best_bid >= self.amethyst_sellprice:
                        orders.append(Order(product, best_bid, -best_bid_amount))
            
            elif product == "STARFRUIT":
                roc = self.calculate_roc(product, state)

                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if roc >= self.roc_sell:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                
                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if roc <= self.roc_buy:
                        orders.append(Order(product, best_bid, -best_bid_amount))

            elif product == "ORCHIDS":
                sunlight = state.observations.conversionObservations['ORCHIDS'].sunlight
                humidity = state.observations.conversionObservations['ORCHIDS'].humidity
                
                self.calculate_OPI(sunlight, humidity)
                self.calculate_first_derivative()
                
                second_derivative = self.calculate_second_derivative()
                
                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if second_derivative <= self.orchid_buy:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                
                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if second_derivative >= self.orchid_sell:
                        orders.append(Order(product, best_bid, best_bid_amount))

            result[product] = orders
    
        trader_data = "SAMPLE"
        conversions = 1
        return result, conversions, trader_data