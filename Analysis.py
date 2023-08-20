import os
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from PIL import Image
import io
import base64
import numpy as np

class Analysis:
    """
    A class for performing data analysis on financial instrument data.
    """
    def __init__(self):
        pass

    def check_analysis_feasibility(self, start_date, end_date, filename):
        """
            Check if analysis is feasible based on provided date range and data availability.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename (str): Path to the JSON data file for the instrument.

            Returns:
                bool: True if analysis is feasible, False otherwise.
        """
        try:
            instrument = os.path.splitext(os.path.basename(filename))[0]
            with open(filename, 'r') as file:
                data = json.load(file)
            df = pd.DataFrame(data)
            df['Date'] = pd.to_datetime(df['Date'])
            min_date = df['Date'].min().strftime('%Y-%m-%d')
            max_date = df['Date'].max().strftime('%Y-%m-%d')

            if start_date < min_date or end_date > max_date:
                print("Analiza dla podanych dat jest niemożliwa.")
                print(f"Dostępny zakres danych dla {instrument}: {min_date} - {max_date}")
                return False

            return True

        except Exception as e:
            print(f"Wystąpił błąd podczas sprawdzania możliwości analizy: {e}")
            return False

    def calculate_investment_return(self, start_date, end_date, filename1, filename2):
        """
            Calculate investment return for two instruments over a specified period.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename1 (str): Path to the JSON data file for instrument 1.
                filename2 (str): Path to the JSON data file for instrument 2.

            Returns:
                dict: A dictionary containing investment return values for both instruments.
        """
        try:
            instrument1 = os.path.splitext(os.path.basename(filename1))[0]
            instrument2 = os.path.splitext(os.path.basename(filename2))[0]

            if not self.check_analysis_feasibility(start_date, end_date, filename1) or not \
                    self.check_analysis_feasibility(start_date, end_date, filename2):
                return

            # Funkcja pomocnicza do obliczenia zwrotu dla jednego instrumentu
            def calculate_return(filename):
                with open(filename, 'r') as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                df['Date'] = pd.to_datetime(df['Date'])
                mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
                filtered_df = df.loc[mask]
                start_price = filtered_df.iloc[0]['Close']
                end_price = filtered_df.iloc[-1]['Close']
                return (((end_price - start_price) / start_price) * 100)

            # Obliczenie zwrotu z inwestycji dla dwóch instrumentów
            return1 = calculate_return(filename1)
            return2 = calculate_return(filename2)

            print(f"Zwrot z inwestycji dla {instrument1}: {return1:.2f}%")
            print(f"Zwrot z inwestycji dla {instrument2}: {return2:.2f}%")

            result = {
                "instrument1": instrument1,
                "instrument2": instrument2,
                "start_date": start_date,
                "end_date": end_date,
                "investment_return1": return1,
                "investment_return2": return2
            }

            self.save_results(result, start_date, end_date, instrument1, instrument2)

        except Exception as e:
            print(f"Wystąpił błąd podczas obliczania zwrotu z inwestycji: {e}")

    def calculate_correlation(self, start_date, end_date, filename1, filename2):
        """
            Calculate correlation between two instruments over a specified period.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename1 (str): Path to the JSON data file for instrument 1.
                filename2 (str): Path to the JSON data file for instrument 2.

            Returns:
                float: The calculated correlation value.

        """
        try:
            instrument1 = os.path.splitext(os.path.basename(filename1))[0]
            instrument2 = os.path.splitext(os.path.basename(filename2))[0]

            if not self.check_analysis_feasibility(start_date, end_date, filename1) or not self.check_analysis_feasibility(start_date, end_date, filename2):
                return

            with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
                data1 = json.load(file1)
                data2 = json.load(file2)

            df1 = pd.DataFrame(data1)
            df2 = pd.DataFrame(data2)

            # Filtracja danych na podstawie daty
            df1['Date'] = pd.to_datetime(df1['Date'])
            mask1 = (df1['Date'] >= start_date) & (df1['Date'] <= end_date)
            filtered_df1 = df1.loc[mask1]

            df2['Date'] = pd.to_datetime(df2['Date'])
            mask2 = (df2['Date'] >= start_date) & (df2['Date'] <= end_date)
            filtered_df2 = df2.loc[mask2]

            # Łączenie danych po dacie
            merged_data = pd.merge(filtered_df1, filtered_df2, on='Date', suffixes=('_1', '_2'))

            # Obliczanie korelacji
            correlation = merged_data['Close_1'].corr(merged_data['Close_2'])

            print(f"Korelacja między {instrument1} i {instrument2} (od {start_date} do {end_date}): {correlation:.2f}")

            result = {
                "instrument1": instrument1,
                "instrument2": instrument2,
                "correlation": correlation
            }

            self.save_results(result, start_date, end_date, instrument1, instrument2)

        except Exception as e:
            print(f"Wystąpił błąd podczas obliczania korelacji: {e}")

    def calculate_basic_statistics(self, start_date, end_date, filename1, filename2):
        """
            Calculate basic statistics for two instruments over a specified period.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename1 (str): Path to the JSON data file for instrument 1.
                filename2 (str): Path to the JSON data file for instrument 2.

            Returns:
                dict: A dictionary containing basic statistics values for both instruments.

        """

        try:
            instrument1 = os.path.splitext(os.path.basename(filename1))[0]
            instrument2 = os.path.splitext(os.path.basename(filename2))[0]
            if not self.check_analysis_feasibility(start_date, end_date, filename1) or not \
                    self.check_analysis_feasibility(start_date, end_date, filename2):
                return

            def calculate_statistics(filename):
                instrument = os.path.splitext(os.path.basename(filename))[0]
                with open(filename, 'r') as file:
                    data = json.load(file)

                df = pd.DataFrame(data)
                df['Close'] = pd.to_numeric(df['Close'])

                # Obliczanie podstawowych miar statystycznych
                stats = df['Close'].describe()[['mean', '50%', 'std', 'min', 'max']]
                print(f"{instrument}: ")
                for key, value in stats.items():
                    print(f"{key}: {value:.2f}")
                return stats['mean'], stats['50%'], stats['std'], stats['min'], stats['max']

            # Obliczenie podstawowych statystyk dla obu instrumentów
            mean1, median1, std_dev1, min_price1, max_price1 = calculate_statistics(filename1)
            mean2, median2, std_dev2, min_price2, max_price2 = calculate_statistics(filename2)

            result = {
                "instrument1": instrument1,
                "instrument2": instrument2,
                "start_date": start_date,
                "end_date": end_date,
                "basic_statistics1": {
                    "mean": mean1,
                    "median": median1,
                    "std_dev": std_dev1,
                    "min_price": min_price1,
                    "max_price": max_price1
                },
                "basic_statistics2": {
                    "mean": mean2,
                    "median": median2,
                    "std_dev": std_dev2,
                    "min_price": min_price2,
                    "max_price": max_price2
                }
            }

            self.save_results(result, start_date, end_date, instrument1, instrument2)

        except Exception as e:
            print(f"Wystąpił błąd podczas obliczania miar statystycznych: {e}")



    def calculate_risk_indicators(self, start_date, end_date, filename1, filename2):
        """
            Calculate risk indicators for two instruments over a specified period.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename1 (str): Path to the JSON data file for instrument 1.
                filename2 (str): Path to the JSON data file for instrument 2.

            Returns:
                dict: A dictionary containing risk indicators values for both instruments.

        """

        try:
            instrument1 = os.path.splitext(os.path.basename(filename1))[0]
            instrument2 = os.path.splitext(os.path.basename(filename2))[0]
            if not self.check_analysis_feasibility(start_date, end_date, filename1) or not \
                    self.check_analysis_feasibility(start_date, end_date, filename2):
                return

            def calculate_statistics(filename):
                with open(filename, 'r') as file:
                    data = json.load(file)

                df = pd.DataFrame(data)
                df['Close'] = pd.to_numeric(df['Close'])

                # Obliczanie dziennych zwrotów
                returns = df['Close'].pct_change() * 100

                # Obliczanie wskaźników ryzyka
                risk_free_rate = 0.05  # Przykładowa stopa bezpiecznego zwrotu (5%)
                excess_returns = returns - risk_free_rate
                mean_return = np.mean(excess_returns)
                std_dev = np.std(excess_returns)

                # Obliczanie współczynnika Sharpe'a
                sharpe_ratio = mean_return / std_dev

                # Obliczanie współczynnika Sortino
                downside_returns = excess_returns.copy()
                downside_returns[downside_returns > 0] = 0  # Zerowanie dodatnich zwrotów
                downside_std_dev = np.std(downside_returns)

                sortino_ratio = mean_return / downside_std_dev

                return sharpe_ratio, sortino_ratio

            # Obliczenie wskaźników ryzyka dla instrumentu 1
            sharpe_ratio1, sortino_ratio1 = calculate_statistics(filename1)

            # Obliczenie wskaźników ryzyka dla instrumentu 2
            sharpe_ratio2, sortino_ratio2 = calculate_statistics(filename2)

            print(f"Wskaźniki ryzyka dla {instrument1} (od {start_date} do {end_date}):")
            print(f"Współczynnik Sharpe'a: {sharpe_ratio1:.2f}")
            print(f"Współczynnik Sortino: {sortino_ratio1:.2f}")

            print(f"\nWskaźniki ryzyka dla {instrument2} (od {start_date} do {end_date}):")
            print(f"Współczynnik Sharpe'a: {sharpe_ratio2:.2f}")
            print(f"Współczynnik Sortino: {sortino_ratio2:.2f}")

            result = {
                "instrument1": instrument1,
                "instrument2": instrument2,
                "risk_indicators1": {
                    "sharpe_ratio": sharpe_ratio1,
                    "sortino_ratio": sortino_ratio1
                },
                "risk_indicators2": {
                    "sharpe_ratio": sharpe_ratio2,
                    "sortino_ratio": sortino_ratio2
                }
            }
            self.save_results(result, start_date, end_date, instrument1, instrument2)

        except Exception as e:
            print(f"Wystąpił błąd podczas obliczania wskaźników ryzyka: {e}")

    def calculate_correlation_between_declines_and_increases(self, start_date, end_date, filename1, filename2):
        """
            Calculate correlation between declines and increases for two instruments.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename1 (str): Path to the JSON data file for instrument 1.
                filename2 (str): Path to the JSON data file for instrument 2.

            Returns:
                float: The calculated correlation between declines increases value.

        """
        try:
            instrument1 = os.path.splitext(os.path.basename(filename1))[0]
            instrument2 = os.path.splitext(os.path.basename(filename2))[0]

            if not self.check_analysis_feasibility(start_date, end_date,filename1) or not \
                    self.check_analysis_feasibility(start_date,end_date,filename2):
                return

            with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
                data1 = json.load(file1)
                data2 = json.load(file2)

            df1 = pd.DataFrame(data1)
            df2 = pd.DataFrame(data2)

            # Filtracja danych na podstawie daty
            df1['Date'] = pd.to_datetime(df1['Date'])
            mask1 = (df1['Date'] >= start_date) & (df1['Date'] <= end_date)
            filtered_df1 = df1.loc[mask1].copy()

            df2['Date'] = pd.to_datetime(df2['Date'])
            mask2 = (df2['Date'] >= start_date) & (df2['Date'] <= end_date)
            filtered_df2 = df2.loc[mask2].copy()

            # Obliczanie dziennych zwrotów (procentowych zmian) cen
            filtered_df1.loc[:, 'Return'] = filtered_df1['Close'].pct_change() * 100
            filtered_df2.loc[:, 'Return'] =filtered_df2['Close'].pct_change() * 100

            # Usunięcie pierwszego wiersza (brak zwrotu)
            filtered_df1 = filtered_df1.iloc[1:]
            filtered_df2 = filtered_df2.iloc[1:]

            # Łączenie danych po dacie
            merged_data = pd.merge(filtered_df1, filtered_df2, on='Date', suffixes=('_1', '_2'))

            # Obliczanie korelacji między dziennymi zwrotami
            correlation_between_declines_increases = merged_data['Return_1'].corr(merged_data['Return_2'])

            print(f"Korelacja między wzrostami i spadkami cen {instrument1} i {instrument2} (od {start_date} do {end_date}): {correlation_between_declines_increases:.2f}")
            result = {
                "instrument1": instrument1,
                "instrument2": instrument2,
                "correlation_between_declines_increases": correlation_between_declines_increases
            }

            self.save_results(result, start_date, end_date, instrument1, instrument2)

        except Exception as e:
            print(f"Wystąpił błąd podczas obliczania korelacji między spadkami, a wzrostami: {e}")


    def generate_price_chart(self, start_date, end_date, filename1, filename2):
        """
            Generate a normalized price chart for two instruments.

            Args:
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                filename1 (str): Path to the JSON data file for instrument 1.
                filename2 (str): Path to the JSON data file for instrument 2.

            Returns:
                dict: A dictionary containing plot and .

        """
        instrument1 = filename1.split(".")[0].split("/")[-1]
        instrument2 = filename2.split(".")[0].split("/")[-1]

        if filename1 == filename2:
            print("Nazwy plików muszą być różne.")
            return

        try:
            with open(filename1, "r") as file1, open(filename2, "r") as file2:
                data1 = json.load(file1)
                data2 = json.load(file2)

            df1 = pd.DataFrame(data1)
            df2 = pd.DataFrame(data2)

            # Wybieramy tylko potrzebne kolumny
            df1 = df1[["Date", "Close"]]
            df2 = df2[["Date", "Close"]]

            # Konwertujemy kolumnę z datami na typ datetime
            df1["Date"] = pd.to_datetime(df1["Date"])
            df2["Date"] = pd.to_datetime(df2["Date"])

            # Parsowanie start_date i end_date do typu datetime64[ns]
            start_date = np.datetime64(datetime.strptime(start_date, "%Y-%m-%d").date())
            end_date = np.datetime64(datetime.strptime(end_date, "%Y-%m-%d").date())

            # Filtrujemy dane według zakresu dat
            mask1 = (df1["Date"] >= start_date.astype('datetime64[ns]')) & (
                        df1["Date"] <= end_date.astype('datetime64[ns]'))
            mask2 = (df2["Date"] >= start_date.astype('datetime64[ns]')) & (
                        df2["Date"] <= end_date.astype('datetime64[ns]'))
            df1 = df1.loc[mask1]
            df2 = df2.loc[mask2]

            # Normalizacja danych względem wartości bazowej 100
            base_value1 = df1["Close"].iloc[0]
            base_value2 = df2["Close"].iloc[0]
            df1["Normalized Close"] = df1["Close"].div(base_value1).mul(100)
            df2["Normalized Close"] = df2["Close"].div(base_value2).mul(100)

            # Generowanie wykresu
            fig, ax = plt.subplots()
            ax.plot(df1["Date"], df1["Normalized Close"], label=instrument1)
            ax.plot(df2["Date"], df2["Normalized Close"], label=instrument2)
            ax.set_xlabel("Date")
            ax.set_ylabel("Percent Change (%)")
            ax.set_title("Normalized Price Chart")
            ax.legend()

            # Ustawianie wyświetlania przedziałów na osi x w zależności od różnicy czasowej
            time_difference = end_date - start_date
            if time_difference < pd.Timedelta(days=365 * 2):
                ax.xaxis.set_major_locator(mdates.MonthLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            else:
                ax.xaxis.set_major_locator(mdates.YearLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

            # Ustawianie skalowania osi y
            ax.set_ylim(0, max(df1["Normalized Close"].max(), df2["Normalized Close"].max()))

            plt.xticks(rotation=45)

            # Zapisz wykres jako obraz w postaci binarnej
            image_stream = io.BytesIO()
            plt.savefig(image_stream, format='png')
            image_stream.seek(0)
            image_binary = image_stream.read()

            # Koduj dane binarne do formatu Base64
            image_base64 = base64.b64encode(image_binary).decode('utf-8')
            # print(image_base64)

            # Tworzenie nazwy folderu na podstawie parametrów analizy
            analysis_folder = f"{instrument1}_{instrument2}_{start_date.astype('datetime64[D]').astype(str).replace('-', '')}_{end_date.astype('datetime64[D]').astype(str).replace('-', '')}"

            # Tworzenie ścieżki do folderu
            folder_path = os.path.join("results", analysis_folder)

            # Tworzenie folderu, jeśli nie istnieje
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Zapisywanie wykresu jako pliku PNG
            chart_filename = f"{instrument1}_{instrument2}_chart.png"
            chart_path = os.path.join(folder_path, chart_filename)
            plt.savefig(chart_path, format='png')

            # Zapisywanie ścieżki do wykresu w wynikach
            result = {
                'instrument1': instrument1,
                'instrument2': instrument2,
                'image': image_base64,
                'chart_path': chart_path
            }
            self.save_results(result, start_date, end_date, instrument1, instrument2)
            plt.show()

        except FileNotFoundError:
            print("Nie można znaleźć pliku. Sprawdź ścieżkę i nazwę pliku.")
        except json.JSONDecodeError:
            print("Błąd podczas wczytywania pliku JSON. Upewnij się, że plik ma poprawny format.")
        except Exception as e:
            print("Wystąpił błąd podczas generowania wykresu.")
            print("Błąd:", e)

    def save_results(self, result, start_date, end_date, instrument1, instrument2):
        """
            Save analysis results to a JSON file.

            Args:
                result (dict): Analysis results.
                start_date (str): Start date for analysis in 'YYYY-MM-DD' format.
                end_date (str): End date for analysis in 'YYYY-MM-DD' format.
                instrument1 (str): Name of instrument 1.
                instrument2 (str): Name of instrument 2.

            """
        try:
            results_dir = "results"

            # Konwersja dat na łańcuchy znaków
            start_date_str = str(start_date)
            end_date_str = str(end_date)

            # Tworzenie nazwy katalogu na podstawie parametrów analizy
            analysis_name = f"{instrument1}_{instrument2}_{start_date_str.replace('-', '')}_{end_date_str.replace('-', '')}"
            analysis_dir = os.path.join(results_dir, analysis_name)

            if not os.path.exists(analysis_dir):
                os.makedirs(analysis_dir)

            # Tworzenie nazwy pliku wynikowego
            filename = f"{instrument1}_{instrument2}_results.json"
            filepath = os.path.join(analysis_dir, filename)

            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    data = json.load(file)
                    data.update(result)
            else:
                data = result

            with open(filepath, "w") as file:
                json.dump(data, file)

        except Exception as e:
            print(f"Wystąpił błąd podczas zapisywania wyników: {e}")

