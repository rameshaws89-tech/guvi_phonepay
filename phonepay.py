import os
class multiplefileextraction:
    def __init__(self, aggregated_file_path, insurance_file_path, user_file_path):
        self.aggregated_file_path = aggregated_file_path
        self.insurance_file_path = insurance_file_path
        self.user_file_path = user_file_path

    def extract_data(self):
        # Code to extract data from the file
        pass

    def process_data(self):
        # Code to process the extracted data
        pass

    def save_data(self):
        # Code to save the processed data
        pass
if __name__ == "__main__":
    aggregated_file_path = "data/aggregated/transaction/country/india/state/"
    insurance_file_path = "data/insurance/transaction/country/india/state/"
    user_file_path = "data/user/transaction/country/india/state/"
    extractor = multiplefileextraction(aggregated_file_path=aggregated_file_path, insurance_file_path=insurance_file_path, user_file_path=user_file_path)
    extractor.extract_data()
    extractor.process_data()
    extractor.save_data()