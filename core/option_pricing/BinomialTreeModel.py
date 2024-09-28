import numpy as np
from .base import OptionPricingModel, OPTION_TYPE


class BinomialTreeModel(OptionPricingModel):
    """
    Class implementing calculation for European option price using the Binomial Option Pricing Model (BOPM).
    It calculates option prices in discrete time (lattice-based), with a specified number of time steps between the valuation date and the exercise date.
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps):
        """
        Parameters:
        underlying_spot_price (float): Current spot price of the underlying asset.
        strike_price (float): Strike price of the option contract.
        days_to_maturity (int): Number of days until the option contract's maturity or exercise date.
        risk_free_rate (float): Constant risk-free interest rate, expressed as a decimal (e.g., 0.05 for 5%).
        sigma (float): Volatility of the underlying asset (standard deviation of log returns).
        number_of_time_steps (int): Number of time periods between the valuation date and the exercise date.
        """
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma
        self.N = number_of_time_steps

        # Precompute constants
        self.dT = self.T / self.N
        self.u = np.exp(self.sigma * np.sqrt(self.dT))
        self.d = 1.0 / self.u
        self.a = np.exp(self.r * self.dT)
        self.p = (self.a - self.d) / (self.u - self.d)
        self.q = 1.0 - self.p
        self.discount = np.exp(-self.r * self.dT)

    def calculate_option_price(self, option_type):
        """
        Calculates the price of a European call or put option using the Binomial Tree model.

        Parameters:
        option_type (OPTION_TYPE): The type of option to price. Must be OPTION_TYPE.CALL_OPTION
                                   for a call option or OPTION_TYPE.PUT_OPTION for a put option.

        Returns:
        float: The calculated option price.

        Raises:
        ValueError: If an invalid option type is provided (i.e., not OPTION_TYPE.CALL_OPTION or OPTION_TYPE.PUT_OPTION).
        """
        if option_type == OPTION_TYPE.CALL_OPTION:
            payoff_function = lambda S: np.maximum(S - self.K, 0.0)
        elif option_type == OPTION_TYPE.PUT_OPTION:
            payoff_function = lambda S: np.maximum(self.K - S, 0.0)
        else:
            raise ValueError("Invalid option type. Must be OPTION_TYPE.CALL_OPTION or OPTION_TYPE.PUT_OPTION.")

        # Initialise asset prices at maturity
        j = np.arange(self.N + 1)
        S_T = self.S * self.u ** (self.N - j) * self.d ** j

        # Calculate option values at maturity
        V = payoff_function(S_T)

        # Perform backward induction
        for _ in range(self.N):
            V = self.discount * (self.p * V[:-1] + self.q * V[1:])

        return V[0]