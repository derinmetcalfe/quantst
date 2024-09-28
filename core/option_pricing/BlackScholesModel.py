# Third party imports
import numpy as np
from scipy.stats import norm 

# Local package imports
from .base import OptionPricingModel
from .base import OPTION_TYPE

class BlackScholesModel(OptionPricingModel):
    """
    Class implementing calculation for European option price using the Black-Scholes formula.
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma):
        """
        Initialises variables used in the Black-Scholes option pricing model.

        Parameters:
        underlying_spot_price (float): The current price of the underlying asset.
        strike_price (float): The strike price of the option.
        days_to_maturity (int): The number of days until the option's maturity or expiration.
        risk_free_rate (float): The risk-free interest rate, expressed as a decimal (e.g., 0.05 for 5%).
        sigma (float): The volatility of the underlying asset, represented as the standard deviation of its returns.
        """
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma

        # Precompute d1 and d2
        self._compute_d1_d2()

    def _compute_d1_d2(self):
        """
        Computes the values of d1 and d2 used in the Black-Scholes option pricing formulas.
            Formulas:
            d1 = [ln(S / K) + (r + 0.5 * sigma^2) * T] / (sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)
        """
        sqrt_T = np.sqrt(self.T)
        sigma_sqrt_T = self.sigma * sqrt_T
        log_SK = np.log(self.S / self.K)
        self.d1 = (log_SK + (self.r + 0.5 * self.sigma ** 2) * self.T) / sigma_sqrt_T
        self.d2 = self.d1 - sigma_sqrt_T

    def calculate_option_price(self, option_type):
        """
        Calculates the option price based on the option type using the Black-Scholes formula.

        Parameters:
        option_type (OPTION_TYPE): The type of option, either OPTION_TYPE.CALL_OPTION or OPTION_TYPE.PUT_OPTION.

        Returns:
        float: The calculated price of the option.

        Raises:
        ValueError: If an invalid option type is provided.
        """
        if option_type == OPTION_TYPE.CALL_OPTION:
            price = (self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
        elif option_type == OPTION_TYPE.PUT_OPTION:
            price = (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1))
        else:
            raise ValueError("Invalid option type. Must be OPTION_TYPE.CALL_OPTION or OPTION_TYPE.PUT_OPTION.")
        return price
