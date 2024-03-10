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
        
        # clean by replacing nan values with previous values
        for i in range(len(self.amethyst_bids) - 1):
            if math.isnan(self.amethyst_bids[i + 1]):
                self.amethyst_bids[i + 1] = self.amethyst_bids[i]
            
            if math.isnan(self.amethyst_asks[i + 1]):
                self.amethyst_asks[i + 1] = self.amethyst_asks[i]
                
        for i in range(len(self.starfruit_bids) - 1):
            if math.isnan(self.starfruit_bids[i + 1]):
                self.starfruit_bids[i + 1] = self.starfruit_bids[i]
            
            if math.isnan(self.starfruit_asks[i + 1]):
                self.starfruit_asks[i + 1] = self.starfruit_asks[i]
        
        # create midprices
        self.amethyst_midprices = ((x + y) / 2 for x, y in zip(self.amethyst_bids, self.amethyst_asks))
        self.starfruit_midprices = ((x + y) / 2 for x, y in zip(self.starfruit_bids, self.starfruit_asks))

class volatility:
    def __init__(self, amethyst_midprices, starfruit_midprices):
        amethyst_mean = self.calculate_mean(amethyst_midprices)
        starfruit_mean = self.calculate_mean(starfruit_midprices)
        
        self.amethyst_vol = self.calculate_variance(amethyst_midprices, amethyst_mean)
        self.starfruit_vol = self.calculate_variance(starfruit_midprices, starfruit_mean)
        
    def calculate_mean(data):
        return sum(data) / len(data)

    def calculate_variance(data, mean):
        squared_diff = [(x - mean) ** 2 for x in data]
        return sum(squared_diff) / len(data)