# from DataDownloading import DataDownloading
# from ConvertingData import ConvertingData
# from Analysis import Analysis
#
# class Main:
#     def __init__(self):
#         self.data_downloader = DataDownloading()
#         self.data_converting = ConvertingData()
#         self.data_analysis = Analysis()
#
#     def run_downloading(self):
#         self.data_downloader.run_downloading()
#
#     def run_converting(self):
#         self.data_converting.convert_json_to_excel()
#         self.data_converting.convert_json_to_xml()
#
#     def run_analysis(self):
#         self.data_analysis.calculate_investment_return(start_date,end_date,filename1,filename2)
#         self.data_analysis.calculate_correlation(start_date,end_date,filename1,filename2)
#         self.data_analysis.calculate_correlation_between_declines_and_increases(start_date,end_date,filename1,filename2)
#         self.data_analysis.calculate_basic_statistics(start_date,end_date,filename1,filename2)
#         self.data_analysis.calculate_risk_indicators(start_date,end_date,filename1,filename2)
#         self.data_analysis.generate_price_chart(start_date,end_date,filename1,filename2)
#
#     def run(self):
#         # self.run_downloading()
#         # self.run_converting()
#         self.run_analysis()
#
# if __name__ == "__main__":
#     main = Main()
#     start_date = '2019-01-01'
#     end_date = '2021-01-01'
#     filename1 = 'financial_data_json/btc-usd.json'
#     filename2 = 'financial_data_json/ltc-usd.json'
#     main.run()
#
#
#
#
#


from DataDownloading import DataDownloading
from ConvertingData import ConvertingData
from Analysis import Analysis


class Main:
    def __init__(self):
        self.data_downloader = DataDownloading()
        self.data_converting = ConvertingData()
        self.data_analysis = Analysis()

    def run_downloading(self):
        """Run the data downloading process."""
        self.data_downloader.run_downloading()

    def run_converting(self):
        """Run the data conversion process."""
        self.data_converting.convert_json_to_excel()
        self.data_converting.convert_json_to_xml()

    def run_analysis(self, start_date, end_date, filename1, filename2):
        """Run the data analysis process.

        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.
            filename1 (str): Path to the first JSON file.
            filename2 (str): Path to the second JSON file.
        """
        self.data_analysis.calculate_investment_return(start_date, end_date, filename1, filename2)
        self.data_analysis.calculate_correlation(start_date, end_date, filename1, filename2)
        self.data_analysis.calculate_correlation_between_declines_and_increases(start_date, end_date, filename1,
                                                                                filename2)
        self.data_analysis.calculate_basic_statistics(start_date, end_date, filename1, filename2)
        self.data_analysis.calculate_risk_indicators(start_date, end_date, filename1, filename2)
        self.data_analysis.generate_price_chart(start_date, end_date, filename1, filename2)

    def run(self):
        """Run the main program."""
        # Uncomment the following lines if needed
        # self.run_downloading()
        # self.run_converting()

        # Set your analysis parameters here
        start_date = '2019-01-01'
        end_date = '2021-01-01'
        filename1 = 'financial_data_json/xlm-usd.json'
        filename2 = 'financial_data_json/xrp-usd.json'

        self.run_analysis(start_date, end_date, filename1, filename2)


if __name__ == "__main__":
    main = Main()
    main.run()
