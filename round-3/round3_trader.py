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
        
        # rose stuff
        self.rose_prices = deque(maxlen=100)
        self.rose_buy = 0.05
        self.rose_sell = -0.10
        
        # strawberry stuff
        self.strawberry_prices = deque(maxlen=100)
        self.strawberry_buy = 0.10
        self.strawberry_sell = -0.10
        
        # chocolate stuff
        self.chocolate_prices = deque(maxlen=100)
        self.chocolate_buy = 0.15
        self.chocolate_sell = -0.20
    
    def calculate_roc(self, product: str, state: TradingState, prices_deque: deque) -> float:
        trades = state.market_trades.get(product, [])
        prices = [trade.price for trade in trades]
        prices_deque.extend(prices)

        if len(prices_deque) < 2:
            print("Not enough data points")
            return 0.0
        
        roc = (prices_deque[-1] - prices_deque[0]) / prices_deque[0] * 100
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
                roc = self.calculate_roc(product, state, self.starfruit_prices)

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
            
            elif product == 'GIFT_BASKET':
                strawberry_trades = state.market_trades.get('STRAWBERRIES', [])
                strawberry_prices = [trade.price for trade in strawberry_trades]
                strawberry_price = strawberry_prices[-1]
                
                chocolate_trades = state.market_trades.get('CHOCOLATE', [])
                chocolate_prices = [trade.price for trade in chocolate_trades]
                chocolate_price = chocolate_prices[-1]
                
                rose_trades = state.market_trades.get('ROSES', [])
                rose_prices = [trade.price for trade in rose_trades]
                rose_price = rose_prices[-1]
                
                basket_trades = state.market_trades.get('GIFT_BASKET', [])
                basket_prices = [trade.price for trade in basket_trades]
                basket_price = basket_prices[-1]
                
                spread = basket_price - ((6 * strawberry_price) + (4 * chocolate_price) + rose_price)
                print(" spread " + str(spread))
                
                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if spread <= 300:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                
                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if spread >= 500:
                        orders.append(Order(product, best_bid, best_bid_amount))
            
            elif product == 'STRAWBERRIES':
                roc = self.calculate_roc(product, state, self.strawberry_prices)
                print(" Strawberry ROC " + str(roc))

                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if roc <= self.strawberry_sell:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                
                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if roc >= self.strawberry_buy:
                        orders.append(Order(product, best_bid, -best_bid_amount))
            
            elif product == 'ROSES':
                roc = self.calculate_roc(product, state, self.rose_prices)
                print(" Rose ROC " + str(roc))

                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if roc <= self.rose_sell:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                
                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if roc >= self.rose_buy:
                        orders.append(Order(product, best_bid, -best_bid_amount))
            
            elif product == 'CHOCOLATE':
                roc = self.calculate_roc(product, state, self.chocolate_prices)
                print(" Chocolate ROC " + str(roc))
                
                if len(order_depth.sell_orders) > 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if roc <= self.chocolate_sell:
                        orders.append(Order(product, best_ask, -best_ask_amount))
                        
                if len(order_depth.buy_orders) > 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if roc >= self.chocolate_buy:
                        orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
        trader_data = "SAMPLE"
        conversions = 1
        return result, conversions, trader_data