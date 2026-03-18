"""
Module: scalar_resonance_validation.py
Project: Cosmo-Scalar-Link / ALife Pilot
Author: Maurice Dubosson
Concept: Empirical validation of Chiral Symmetry Breaking via DESI 2025 wa parameters.
Theory: Timeless Scalar Field 2 / Scalar-Link Resonance.
"""

import numpy as np
import matplotlib.pyplot as plt

class DESIValidationEngine:
    """
    Engine to simulate biogenesis probability based on 
    Dark Energy dynamic evolution (w0, wa).
    """
    def __init__(self, w0=-0.90, wa=-0.35, noise_level=0.03):
        self.w0 = w0
        self.wa = wa
        self.noise = noise_level
        self.a_biogenesis = 0.7  # Scale factor at Earth's biogenesis (~4Gyr ago)

    def calculate_cosmological_bias(self):
        """ Computes the initial torque induced by the scalar field slope (wa) """
        return abs(self.wa * (1 - self.a_biogenesis)) * 0.05

    def run_emergence_trial(self, resonance_force=2.8, threshold=0.05):
        """ Single simulation of chiral emergence vs thermal noise """
        bias = self.calculate_cosmological_bias()
        pop_L = 0.5 + bias
        
        for _ in range(150):
            delta = pop_L - 0.5
            # Non-linear Scalar-Link Resonance (The Pilot Mechanism)
            gain = (delta ** 2.0) * resonance_force if delta > threshold else 0
            
            # Stochastic thermal noise (Entropy)
            entropy = np.random.normal(0, self.noise)
            
            pop_L = np.clip(pop_L + gain + entropy, 0, 1)
            
            if pop_L >= 0.999: return True  # Life Emergence (100% L)
            if pop_L <= 0.40: return False # Thermal Death (Racemic)
        return False

    def map_probability_cliff(self, wa_range=None, trials=100):
        """ Maps the 'Dubosson Cliff': Probability of Life vs wa strength """
        if wa_range is None:
            wa_range = np.linspace(0, -0.8, 50)
            
        probs = []
        for wa_val in wa_range:
            self.wa = wa_val
            success = sum(1 for _ in range(trials) if self.run_emergence_trial())
            probs.append(success / trials)
        
        return wa_range, probs

def plot_validation(wa_range, probs):
    """ Generates the final validation chart for GitHub/Documentation """
    plt.figure(figsize=(12, 6))
    plt.plot(wa_range, probs, color='black', lw=2.5, label='Emergence Probability')
    plt.fill_between(wa_range, probs, color='gray', alpha=0.1)
    
    # DESI 2025 Marker
    plt.axvline(x=-0.35, color='#ff7f0e', ls='--', lw=2, label='DESI 2025 window (wa)')
    plt.axvspan(-0.15, 0, color='red', alpha=0.05, label='Zone of Silence (Entropy wins)')
    
    plt.title("THE DUBOSSON CLIFF: Life as a Cosmological Necessity", fontsize=14)
    plt.xlabel("Scalar Field Dynamic Strength (wa)", fontsize=12)
    plt.ylabel("Probability of Chiral Homochirality (L-form)", fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(alpha=0.2)
    plt.show()

# Execution
if __name__ == "__main__":
    engine = DESIValidationEngine()
    wa_axis, probabilities = engine.map_probability_cliff()
    plot_validation(wa_axis, probabilities)
