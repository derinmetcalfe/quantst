import numpy as np
import matplotlib.pyplot as plt
from .base import OptionPricingModel, OPTION_TYPE


class MonteCarloPricing(OptionPricingModel):
    """
    Class implementing calculation for European option price using Monte Carlo Simulation.
    It simulates underlying asset prices at expiry using the geometric Brownian motion model.
    For the simulated prices at maturity, it calculates the payoffs, averages them, and discounts the final value.
    This value represents the option price.
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma,
                 number_of_simulations):
        """
        Initialises variables used in Monte Carlo Simulation for pricing options.

        Parameters:
        underlying_spot_price (float): Current spot price of the underlying asset.
        strike_price (float): Strike price of the option contract.
        days_to_maturity (int): Days until the option contract's maturity/exercise date.
        risk_free_rate (float): Constant risk-free interest rate until expiry, expressed as a decimal (e.g., 0.05 for 5%).
        sigma (float): Volatility of the underlying asset, represented as the standard deviation of log returns.
        number_of_simulations (int): Number of simulated price paths to run for the Monte Carlo Simulation.
        """
        self.S_0 = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma
        self.N = number_of_simulations

        # Seed for reproducibility
        np.random.seed(20)

        # Precompute constants
        self.discount_factor = np.exp(-self.r * self.T)

    def simulate_terminal_prices(self):
        """
        Simulates terminal prices directly for European options using geometric Brownian motion.
        """
        # Generate random standard normal variables
        Z = np.random.standard_normal(self.N)
        # Calculate terminal asset prices
        self.S_T = self.S_0 * np.exp(
            (self.r - 0.5 * self.sigma ** 2) * self.T + self.sigma * np.sqrt(self.T) * Z
        )

    def calculate_option_price(self, option_type):
        """
        Calculates the price of a European call or put option using a Monte Carlo Simulation.

        This method simulates the terminal stock prices if they haven't been simulated yet,
        and then calculates the option price based on the specified option type.

        Parameters:
        option_type (OPTION_TYPE): The type of option to price. Must be OPTION_TYPE.CALL_OPTION
                                   for a call option or OPTION_TYPE.PUT_OPTION for a put option.

        Returns:
        float: The estimated option price based on the simulation.

        Raises:
        ValueError: If the provided option_type is not valid.
        """
        try:
            self.S_T
        except AttributeError:
            self.simulate_terminal_prices()

        # Calculate payoffs
        if option_type == OPTION_TYPE.CALL_OPTION:
            payoffs = np.maximum(self.S_T - self.K, 0)
        elif option_type == OPTION_TYPE.PUT_OPTION:
            payoffs = np.maximum(self.K - self.S_T, 0)
        else:
            raise ValueError("Invalid option type. Must be OPTION_TYPE.CALL_OPTION or OPTION_TYPE.PUT_OPTION.")

        # Calculate the option price
        option_price = self.discount_factor * np.mean(payoffs)
        return option_price

    def simulate_price_paths(self, num_time_steps):
        """
        Simulates price paths for the underlying asset over the option's life.

        This method generates multiple simulated price paths using a geometric Brownian motion model,
        which can be useful for path-dependent options or for visualizing potential asset price trajectories.

        Parameters:
        num_time_steps (int): The number of time steps in the simulation.
        """
        dt = self.T / num_time_steps
        # Initialize price paths matrix: rows are time steps, columns are simulations
        S = np.zeros((num_time_steps + 1, self.N))
        S[0] = self.S_0

        # Generate random standard normal variables for each time step and simulation
        Z = np.random.standard_normal((num_time_steps, self.N))

        # Simulate the price paths
        for t in range(1, num_time_steps + 1):
            S[t] = S[t - 1] * np.exp(
                (self.r - 0.5 * self.sigma ** 2) * dt + self.sigma * np.sqrt(dt) * Z[t - 1]
            )

        self.price_paths = S

    def plot_simulation_results(self, num_of_movements=10):
        """
        Plots a specified number of simulated price movements from the Monte Carlo Simulation.

        This method visualises the simulated asset price paths over time. If the price paths have not been simulated yet,
        it will first generate them using the default of 252 time steps (approximate number of trading days in a year).

        Parameters:
        num_of_movements (int, optional): The number of simulated price paths to plot. Defaults to 10.

        Returns:
        matplotlib.figure.Figure: The matplotlib figure object.
        """
        # Ensure that price paths are simulated
        try:
            self.price_paths
        except AttributeError:
            self.simulate_price_paths(num_time_steps=252)  # Default to 252 steps (approx. trading days in a year)

        fig, ax = plt.subplots(figsize=(12, 8))

        ax.plot(self.price_paths[:, :num_of_movements])
        ax.axhline(self.K, color='k', linestyle='--', label='Strike Price')
        ax.set_xlim([0, self.price_paths.shape[0] - 1])
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Asset Price')
        ax.set_title(f'First {num_of_movements} Simulated Price Paths')
        ax.legend(loc='best')

        # Return the figure object to be used in Streamlit
        return fig

