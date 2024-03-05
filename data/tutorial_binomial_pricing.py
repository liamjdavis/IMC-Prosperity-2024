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