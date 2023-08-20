# import os
# import yfinance as yf
# import json
# import datetime
#
#
# class DataDownloading:
#     def __init__(self):
#         self.instruments = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD', 'DOGE-USD', 'DOT1-USD', 'LINK-USD',
#                             'BCH-USD', 'LTC-USD', 'XLM-USD', 'UNI3-USD', 'AAVE-USD', 'VET-USD', 'EOS-USD',
#                             'THETA-USD', 'XMR-USD', 'WBTC-USD', 'TRX-USD']
#
#     def download_data(self, symbol, start, end):
#         df = yf.download(symbol, start=start, end=end)
#         df_selected = df[['Close']].copy()
#         df_selected['Date'] = df_selected.index.strftime('%Y-%m-%d')
#         data = df_selected.to_dict(orient='records')
#
#         folder_path = "financial_data_json"
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
#
#         filename = os.path.join(folder_path, f'{symbol.lower()}.json')
#         with open(filename, 'w') as f:
#             json.dump(data, f)
#
#     def check_start_date(self, symbol):
#         ticker = yf.Ticker(symbol)
#         history = ticker.history(period="max")
#         start_date = history.index[0].strftime('%Y-%m-%d')
#         return str(start_date)
#
#     def run_downloading(self):
#         for instrument in self.instruments:
#             try:
#                 start_date = self.check_start_date(instrument)
#                 end_date = datetime.date.today().strftime('%Y-%m-%d')
#                 self.download_data(instrument, start=start_date, end=end_date)
#                 print(f"Pobrano i zapisano dane dla {instrument}")
#             except Exception as e:
#                 print(f"Wystąpił błąd przy pobieraniu danych dla {instrument}: {e}")

import os
import yfinance as yf
import json
import datetime


class DataDownloading:
    """Class responsible for downloading financial data from Yahoo Finance."""

    def __init__(self):
        """Initialize the DataDownloading class."""
        self.instruments = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD', 'DOGE-USD', 'DOT1-USD', 'LINK-USD',
                            'BCH-USD', 'LTC-USD', 'XLM-USD', 'UNI3-USD', 'AAVE-USD', 'VET-USD', 'EOS-USD',
                            'THETA-USD', 'XMR-USD', 'WBTC-USD', 'TRX-USD']

    def download_data(self, symbol, start, end):
        """Download financial data for a specific symbol within a specified time range."""
        df = yf.download(symbol, start=start, end=end)
        df_selected = df[['Close']].copy()
        df_selected['Date'] = df_selected.index.strftime('%Y-%m-%d')
        data = df_selected.to_dict(orient='records')

        folder_path = "financial_data_json"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = os.path.join(folder_path, f'{symbol.lower()}.json')
        with open(filename, 'w') as f:
            json.dump(data, f)

    def check_start_date(self, symbol):
        """Check the start date of available historical data for a symbol."""
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="max")
        start_date = history.index[0].strftime('%Y-%m-%d')
        return str(start_date)

    def run_downloading(self):
        """Run the data downloading process for all instruments."""
        for instrument in self.instruments:
            try:
                start_date = self.check_start_date(instrument)
                end_date = datetime.date.today().strftime('%Y-%m-%d')
                self.download_data(instrument, start=start_date, end=end_date)
                print(f"Downloaded and saved data for {instrument}")
            except Exception as e:
                print(f"An error occurred while downloading data for {instrument}: {e}")
