'''
First test run of the basic binomial pricing model
'''

from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

import collections
from collections import defaultdict

import random
import math
import copy

import pandas as pd
import numpy as np

class Trader:
    def run(self, state:TradingState):
        pass

class csv_parser:   
    def __init__(self):
        self.amethyst_bids = []
        self.starfruit_bids = []
        self.amethyst_asks = []
        self.starfruit_asks = []

        df = pd.read_csv("data/tutorial_round.csv", sep=";")

        for index, row in df.iterrows():
            if row['product'] == 'AMETHYSTS':
                self.amethyst_bids.append(row['bid_price_1'])
                self.amethyst_bids.append(row['bid_price_2'])
                self.amethyst_bids.append(row['bid_price_3'])

                self.amethyst_asks.append(row['ask_price_1'])
                self.amethyst_asks.append(row['ask_price_2'])
                self.amethyst_asks.append(row['ask_price_3'])
            
            if row['product'] == 'STARFRUIT':
                self.starfruit_bids.append(row['bid_price_1'])
                self.starfruit_bids.append(row['bid_price_2'])
                self.starfruit_bids.append(row['bid_price_3'])

                self.starfruit_asks.append(row['ask_price_1'])
                self.starfruit_asks.append(row['ask_price_2'])
                self.starfruit_asks.append(row['ask_price_3'])

parser = csv_parser()
print(len(parser.amethyst_bids))
print(len(parser.amethyst_asks))

# class volatility:
#     def __init__(self, amethyst_bids, starfruit_bids, amethyst_asks, starfruit_asks):
#         amethyst_prices = amethyst_bids + amethyst_asks
#         starfruit_prices = starfruit_bids + starfruit_asks
        
#         # calculate means
#         self.amethyst_mean = 0

#         for price in amethyst_bids:
#             self.amethyst_mean += price
        
#         self.amethyst_mean /= len(amethyst_prices)

#         self.starfruit_mean = 0

#         for price in starfruit_prices:
#             self.starfruit_mean += price
        
#         self.starfruit_mean /= len(starfruit_prices)

#         # calculate returns
#         amethyst_returns = 0




