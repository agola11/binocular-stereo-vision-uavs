'''
iir_filter.property
Author:
    Ankush Gola, David Fridovich-Keil
'''

import numpy as np

class IIRFilter:
    """
    Single tap, recursive infinite impulse response filter.
    Acts like low pass filter
    """
    def __init__(self, X_o, tap=0.5):
        """
        X: state vector as np array
        tap: weighting of prior filter value
        """
        self.X = X_o
        self.tap = tap

    
    def update(self, X_n):
        """
        Update the filter with the next state
        X_n: next state
        """
        self.X = self.tap * self.X + (1 - self.tap) * X_n

    def state(self):
        """
        Return the current position as a numpy array
        """
        return self.X