# Standard library imports
import datetime
import requests_cache
import yfinance as yf
import matplotlib.pyplot as plt


class Ticker:
    """Class for fetcing data from Yahoo Finance."""
    def get_historical_data(ticker, start_date="2023-01-01", end_date="2023-08-01", cache_data=True, cache_days=1):
        """
        Fetches historical stock data from Yahoo Finance, with optional caching.

        Parameters:
        ticker (str): The ticker symbol of the stock.
        start_date (str or datetime, optional): The start date for fetching historical data.
        end_date (str or datetime, optional): The end date for fetching historical data.
        cache_data (bool, optional): If True, caches the fetched data in an SQLite database. Default is True.
        cache_days (int, optional): Number of days the data will remain in cache. Default is 1 day.

        Returns:
        pandas.DataFrame: DataFrame containing the historical stock data, or None if an error occurs.
        """
        try:
            if cache_data:
                expire_after = datetime.timedelta(days=cache_days)
                session = requests_cache.CachedSession(
                    cache_name='cache',
                    backend='sqlite',
                    expire_after=expire_after
                )
            else:
                session = None

            data = yf.download(ticker, start=start_date, end=end_date, session=session)
            return data if not data.empty else None
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    @staticmethod
    def get_columns(data):
        """
        Retrieves the column names from the provided stock data DataFrame.

        Parameters:
        data (pd.DataFrame): A DataFrame representing the fetched stock data.

        Returns:
        list: A list of column names from the DataFrame, or None if the input data is None.
        """
        if data is None:
            return None
        return [column for column in data.columns]

    @staticmethod
    def get_last_price(data, column_name):
        """
        Returns the last available price from the specified column in the fetched stock data.

        Parameters:
        data (pd.DataFrame): A DataFrame representing the fetched stock data.
        column_name (str): The name of the column in the DataFrame from which to retrieve the last price.

        Returns:
        float or None: The last available price from the specified column, or None if the data or column_name is invalid.
        """
        if data is None or column_name is None:
            return None
        if column_name not in Ticker.get_columns(data):
            return None
        return data[column_name].iloc[len(data) - 1]

    @staticmethod
    def plot_data(data, ticker, column_name):
        """
        Plots the specified column values from the provided DataFrame.

        Parameters:
        data (pd.DataFrame): A DataFrame representing the fetched stock data.
        ticker (str): The ticker symbol of the stock being plotted.
        column_name (str): The name of the column in the DataFrame to plot.

        Returns:
        matplotlib.figure.Figure: The figure object containing the plot, or None if data is invalid or an error occurs.
        """
        try:
            if data is None:
                return

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data.index, data[column_name], label=f'{ticker} {column_name}')

            ax.set_ylabel(f'{column_name}')
            ax.set_xlabel('Date')
            ax.set_title(f'Historical data for {ticker} - {column_name}')
            ax.legend(loc='best')

            return fig

        except Exception as e:
            print(e)
            return
