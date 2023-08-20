# import os
# import json
# import pandas as pd
# import xml.etree.ElementTree as ET
# import xml.dom.minidom as minidom
#
# class ConvertingData:
#     def __init__(self):
#         pass
#
#     def convert_json_to_excel(self):
#         folder_path = "financial_data_json"
#         output_folder = "financial_data_excel"
#
#         if not os.path.exists(output_folder):
#             os.makedirs(output_folder)
#
#         for filename in os.listdir(folder_path):
#             if filename.endswith(".json"):
#                 json_file = os.path.join(folder_path, filename)
#                 symbol = os.path.splitext(filename)[0].upper()
#                 output_file = os.path.join(output_folder, f"{symbol}.xlsx")
#
#                 with open(json_file, "r") as f:
#                     data = json.load(f)
#
#                 df = pd.DataFrame(data)
#                 df.to_excel(output_file, index=False)
#                 print(f"Skonwertowano plik {filename} do formatu Excel.")
#
#     def convert_json_to_xml(self):
#         folder_path = "financial_data_json"
#         output_folder = "financial_data_xml"
#
#         if not os.path.exists(output_folder):
#             os.makedirs(output_folder)
#
#         for filename in os.listdir(folder_path):
#             if filename.endswith(".json"):
#                 json_file = os.path.join(folder_path, filename)
#                 symbol = os.path.splitext(filename)[0].upper()
#                 output_file = os.path.join(output_folder, f"{symbol}.xml")
#
#                 with open(json_file, "r") as f:
#                     data = json.load(f)
#
#                 root = ET.Element("data")
#                 for item in data:
#                     entry = ET.SubElement(root, "entry")
#                     for key, value in item.items():
#                         element = ET.SubElement(entry, key)
#                         element.text = str(value)
#
#                 tree = ET.ElementTree(root)
#                 tree.write(output_file)
#
#                 print(f"Skonwertowano plik {filename} do formatu XML.")

import os
import json
import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class ConvertingData:
    """Class responsible for converting data formats."""

    def __init__(self):
        """Initialize the ConvertingData class."""
        pass

    def convert_json_to_excel(self):
        """Convert JSON files to Excel format."""
        folder_path = "financial_data_json"
        output_folder = "financial_data_excel"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                json_file = os.path.join(folder_path, filename)
                symbol = os.path.splitext(filename)[0].upper()
                output_file = os.path.join(output_folder, f"{symbol}.xlsx")

                with open(json_file, "r") as f:
                    data = json.load(f)

                df = pd.DataFrame(data)
                df.to_excel(output_file, index=False)
                print(f"Converted {filename} to Excel format.")

    def convert_json_to_xml(self):
        """Convert JSON files to XML format."""
        folder_path = "financial_data_json"
        output_folder = "financial_data_xml"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                json_file = os.path.join(folder_path, filename)
                symbol = os.path.splitext(filename)[0].upper()
                output_file = os.path.join(output_folder, f"{symbol}.xml")

                with open(json_file, "r") as f:
                    data = json.load(f)

                root = ET.Element("data")
                for item in data:
                    entry = ET.SubElement(root, "entry")
                    for key, value in item.items():
                        element = ET.SubElement(entry, key)
                        element.text = str(value)

                tree = ET.ElementTree(root)
                tree.write(output_file)

                print(f"Converted {filename} to XML format.")
