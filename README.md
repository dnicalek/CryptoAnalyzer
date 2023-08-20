# CryptoAnalyzer

## Description

The CryptoAnalyzer is a versatile utility designed to facilitate comprehensive financial analysis for various financial instruments,
such as cryptocurrencies, stocks, and more. 
This tool empowers users with the ability to perform a range of analyses, aiding in informed financial decision-making.

## Features

- **Investment Return Calculation**: Calculate the investment return for two instruments over a specified period, enabling users to assess the profitability of their investments.

- **Correlation Analysis**: Measure the correlation between two instruments to understand how their performance trends relate to each other, assisting users in identifying potential patterns.

- **Basic Statistics Calculation**: Compute basic statistics, such as mean, median, standard deviation, minimum, and maximum prices, to gain insights into the instruments' historical performance.

- **Risk Indicator Assessment**: Calculate risk indicators, including the Sharpe ratio and Sortino ratio, to evaluate the risk-return tradeoff associated with each instrument.

- **Price Chart Generation**: Generate normalized price charts that depict the relative performance of two instruments, aiding visual comparison.

## Requirements

- Python (version 3.11.0)
- Refer to the `requirements.txt` file for the list of additional required libraries.

## Installation

1. Clone the repository to your local machine:
   git clone https://github.com/YourUsername/FinancialAnalysis.git
2. Navigate to the project directory:
   cd FinancialAnalysis
3. Install the required libraries:
   pip install -r requirements.txt

## USAGE
Run the main.py script:
  python main.py


## Project Structure

- **main.py**: The primary script of the application.
- **Analysis.py**: Module containing the class for conducting financial analysis
- **DataDownloading.py**: Module downloading data from YahooFinance API
- **ConvertingData.py**: Module converting files from format .json to .xml or .xlsx
- **financial_data_json/**: Folder where data is stored.
- **results/**: Folder where analysis results will be saved.

## Author
Dominik Nicałek
Email: dominiknicalek@gmail.com




