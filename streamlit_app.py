from enum import Enum
from datetime import datetime, timedelta

import streamlit as st

from core.option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel
from core.option_pricing.base import OPTION_TYPE
from core.util.ticker import Ticker


@st.cache_data
def get_historical_data(ticker):
    """Get historical data for specified ticker and caching it with the app"""
    return Ticker.get_historical_data(ticker)


class OPTION_PRICING_MODEL(Enum):
    BLACK_SCHOLES = 'Black-Scholes'
    MONTE_CARLO = 'Monte Carlo'
    BINOMIAL = 'Binomial-Tree'


st.title('Option Pricing')

# User-selected model from sidebar
pricing_method = st.sidebar.radio(
    'Please select option pricing method',
    options=[model.value for model in OPTION_PRICING_MODEL]
)

st.subheader(f'Pricing Method: {pricing_method}')


def get_common_inputs():
    """Function to get common inputs for all models."""
    ticker = st.text_input('Ticker Symbol', 'AAPL')
    strike_price = st.number_input('Strike Price', value=300.0)
    risk_free_rate = st.slider('Risk-Free Rate (%)', 0.0, 100.0, 10.0)
    sigma = st.slider('Volatility (Sigma) (%)', 0.0, 100.0, 20.0)
    exercise_date = st.date_input(
        'Exercise Date',
        min_value=datetime.today() + timedelta(days=1),
        value=datetime.today() + timedelta(days=365)
    )
    return ticker, strike_price, risk_free_rate, sigma, exercise_date


def display_option_prices(call_price, put_price, currency='$'):
    """Function to display calculated option prices with currency."""
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Call Option Price", value=f"{currency}{call_price:,.2f}")

    with col2:
        st.metric(label="Put Option Price", value=f"{currency}{put_price:,.2f}")



def format_parameters(ticker, exercise_date, risk_free_rate, sigma):
    """Function to format common parameters."""
    data = get_historical_data(ticker)
    st.write(data.tail())
    fig = Ticker.plot_data(data, ticker, 'Adj Close')
    st.pyplot(fig)

    spot_price = Ticker.get_last_price(data, 'Adj Close')
    risk_free_rate /= 100  # Convert percentage to decimal
    sigma /= 100  # Convert percentage to decimal
    days_to_maturity = (exercise_date - datetime.now().date()).days

    return spot_price, days_to_maturity, risk_free_rate, sigma


def calculate_option_prices(model, spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, *args):
    """Function to calculate option prices based on the selected model."""
    if model == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
        model_instance = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
    elif model == OPTION_PRICING_MODEL.MONTE_CARLO.value:
        number_of_simulations = args[0]  # args[0] is number_of_simulations
        model_instance = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma,
                                           number_of_simulations)
        model_instance.simulate_price_paths(num_time_steps=days_to_maturity)
        fig = model_instance.plot_simulation_results(args[1])  # args[1] = num_of_movements
        st.pyplot(fig)
    elif model == OPTION_PRICING_MODEL.BINOMIAL.value:
        number_of_time_steps = args[0]  # args[0] is number_of_time_steps
        model_instance = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma,
                                           number_of_time_steps)

    call_option_price = model_instance.calculate_option_price(OPTION_TYPE.CALL_OPTION)
    put_option_price = model_instance.calculate_option_price(OPTION_TYPE.PUT_OPTION)

    return call_option_price, put_option_price


def main():
    ticker, strike_price, risk_free_rate, sigma, exercise_date = get_common_inputs()

    if pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
        if st.button(f'Calculate Option Price for {ticker}'):
            try:
                spot_price, days_to_maturity, risk_free_rate, sigma = format_parameters(
                    ticker, exercise_date, risk_free_rate, sigma
                )
                call_price, put_price = calculate_option_prices(
                    OPTION_PRICING_MODEL.BLACK_SCHOLES.value,
                    spot_price,
                    strike_price,
                    days_to_maturity,
                    risk_free_rate,
                    sigma
                )
                display_option_prices(call_price, put_price)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
        number_of_simulations = st.slider('Number of Simulations', min_value=100, max_value=100000, value=10000,
                                          step=100)
        num_of_movements = st.slider('Number of Price Movements to Visualize', min_value=0,
                                     max_value=int(number_of_simulations / 10), value=100)

        if st.button(f'Calculate Option Price for {ticker}'):
            try:
                spot_price, days_to_maturity, risk_free_rate, sigma = format_parameters(
                    ticker, exercise_date, risk_free_rate, sigma
                )
                call_price, put_price = calculate_option_prices(
                    OPTION_PRICING_MODEL.MONTE_CARLO.value,
                    spot_price,
                    strike_price,
                    days_to_maturity,
                    risk_free_rate,
                    sigma,
                    number_of_simulations,
                    num_of_movements
                )
                display_option_prices(call_price, put_price)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
        number_of_time_steps = st.slider('Number of Time Steps', min_value=5000, max_value=100000, value=15000,
                                         step=1000)

        if st.button(f'Calculate Option Price for {ticker}'):
            try:
                spot_price, days_to_maturity, risk_free_rate, sigma = format_parameters(
                    ticker, exercise_date, risk_free_rate, sigma
                )
                call_price, put_price = calculate_option_prices(
                    OPTION_PRICING_MODEL.BINOMIAL.value,
                    spot_price,
                    strike_price,
                    days_to_maturity,
                    risk_free_rate,
                    sigma,
                    number_of_time_steps
                )
                display_option_prices(call_price, put_price)
            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
