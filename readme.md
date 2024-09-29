# Option Pricing Application

An intuitive and efficient web application for pricing European call and put options using various financial models. The
application provides insightful visualisations and leverages advanced computational optimisations to deliver fast and
accurate results.

## Introduction

This application is designed to assist investors, traders, and financial analysts in pricing European options using
three fundamental models:

- **Black-Scholes Model**
- **Binomial Tree Model**
- **Monte Carlo Simulation**

By integrating these models into a user-friendly Streamlit app, users can input parameters, visualise data, and obtain
option prices efficiently.

## Features

- **Multiple Pricing Models**: Choose from Black-Scholes, Binomial Tree, or Monte Carlo Simulation to price options.
- **Real-Time Data Retrieval**: Fetches the latest historical stock data for accurate pricing.
- **Interactive Visualisations**:
    - Historical adjusted closing price of the selected stock.
    - Simulated price paths from the Monte Carlo Simulation.
- **User-Friendly Interface**: Intuitive input fields and sliders for setting parameters.
- **Optimised Performance**: Leveraging computational optimisations for fast calculations.

## Models Implemented

### Black-Scholes Model

A mathematical model for pricing European options, accounting for factors like volatility, interest rate, and time to
maturity.

### Binomial Tree Model

A discrete-time model for option pricing that constructs a binomial tree of possible underlying asset prices.

### Monte Carlo Simulation

A statistical method that uses random sampling to simulate possible price paths of the underlying asset to estimate the
option price.

## Optimisations

Significant optimisations have been incorporated to enhance performance and efficiency:

1. **Precomputed Variables in Models**: Critical components such as \( d1 \) and \( d2 \) in the Black-Scholes Model are
   calculated in advance to eliminate redundant computations.

2. **Direct Simulation of Terminal Prices**: In the Monte Carlo Simulation, terminal asset prices are simulated
   directly, reducing computational overhead by avoiding full path simulations for European options.

3. **Memory Optimisation in Binomial Tree Model** : Memory usage is significantly reduced by using minimal arrays to
   store option prices during backward induction, instead of constructing the entire binomial tree.

4. **Vectorised Operations with NumPy**: Utilised NumPy's vectorised operations across all models for efficient
   numerical computations, enhancing execution speed.

5. **Unified Pricing Method**: The base `OptionPricingModel` class now requires only a single abstract
   method `calculate_option_price`, reducing code duplication and allowing for more streamlined subclass
   implementations.

6. **Improved Plotting Practices**: Plotting functions return Matplotlib figure objects, enabling thread-safe rendering
   in Streamlit and future-proofing the application.

7. **Use of Enums for Type Safety**: Implemented `Enum` classes for option types and pricing models to ensure type
   safety and reduce the risk of invalid inputs.

8. **Consolidated Input Handling**: Refactored common input fields and functions to minimize redundancy and improve code
   maintainability.

9. **Error Handling and Validation**: Comprehensive error handling and input validation ensure robustness and prevent
   runtime errors due to invalid inputs.

## Installation

To run the application locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/option-pricing-app.git

2. **Navigate to the Project Directory**
    ```bash
   cd option-pricing-app

3. **Install Dependencies**
   Ensure you have Python 3.8 or later installed. Install the required packages using:
    ```bash
   pip3 install -r requirements.txt

## Usage

To start the Streamlit application, run:

    streamlit run streamlit_app.py

This will launch the app in your default web browser.
<br>

<hr>

**Disclaimer:** This application is for educational and informational purposes only and should not be considered financial advice. Always consult with a qualified financial professional before making investment decisions.