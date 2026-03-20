import os
import json
import pandas as pd
from sqlalchemy import create_engine

class DataExtraction:
    def __init__(self,file_path):
        self.file_path = file_path
        self.state_list = os.listdir(self.file_path)
    def aggregated_data_extraction_trans_insurance(self):
        # Code to extract the aggregated data from the file
        aggregated_data_dict={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    for trans_data in json_data['data']['transactionData']:
                        name=trans_data['name']
                        count=trans_data['paymentInstruments'][0]['count']
                        amount=trans_data['paymentInstruments'][0]['amount']
                        aggregated_data_dict['Transaction_type'].append(name)
                        aggregated_data_dict['Transaction_count'].append(count)
                        aggregated_data_dict['Transaction_amount'].append(amount)
                        aggregated_data_dict['State'].append(state_name)
                        aggregated_data_dict['Year'].append(year)
                        aggregated_data_dict['Quarter'].append(int(quarter.strip('.json')))
        return aggregated_data_dict
    
    def aggregated_data_extraction_user(self):
        # Code to extract the aggregated user data from the file
        aggregated_user_data_dict={'State':[], 'Year':[],'Quarter':[],'registeredUsers':[], 'appOpens':[], 'brand':[],'count':[],'percentage':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    if json_data['data']['usersByDevice'] is not None:
                        for trans_data in json_data['data']['usersByDevice']:
                            brand=trans_data['brand']
                            count=trans_data['count']
                            percentage=trans_data['percentage']
                            aggregated_user_data_dict['registeredUsers'].append(json_data['data']['aggregated']['registeredUsers'])
                            aggregated_user_data_dict['appOpens'].append(json_data['data']['aggregated']['appOpens'])
                            aggregated_user_data_dict['brand'].append(brand)
                            aggregated_user_data_dict['count'].append(count)
                            aggregated_user_data_dict['percentage'].append(percentage)
                            aggregated_user_data_dict['State'].append(state_name)
                            aggregated_user_data_dict['Year'].append(year)
                            aggregated_user_data_dict['Quarter'].append(int(quarter.strip('.json')))
        return aggregated_user_data_dict

    def extract_map_transcation_data(self):
        # Code to extract the map transaction data from the file
        map_transaction_data_dict={'State':[], 'Year':[],'Quarter':[],'name':[], 'count':[],'amount':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    
                    for trans_data in json_data['data']['hoverDataList']:
                        name=trans_data['name']
                        count=trans_data['metric'][0]['count']
                        amount=trans_data['metric'][0]['amount']
                        
                        map_transaction_data_dict['State'].append(state_name)
                        map_transaction_data_dict['Year'].append(year)
                        map_transaction_data_dict['Quarter'].append(int(quarter.strip('.json')))
                        map_transaction_data_dict['name'].append(name)
                        map_transaction_data_dict['count'].append(count)
                        map_transaction_data_dict['amount'].append(amount)
        return map_transaction_data_dict
    def extract_map_user_data(self):
        # Code to extract the map user data from the file
        map_user_data_dict={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'registeredUsers':[],'appOpens':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    
                    for district_name in json_data['data']['hoverData'].keys():
                        registeredUsers=json_data['data']['hoverData'][district_name]['registeredUsers']
                        appOpens=json_data['data']['hoverData'][district_name]['appOpens']
                        map_user_data_dict['State'].append(state_name)
                        map_user_data_dict['Year'].append(year)
                        map_user_data_dict['Quarter'].append(int(quarter.strip('.json')))
                        map_user_data_dict['district_name'].append(district_name)
                        map_user_data_dict['registeredUsers'].append(registeredUsers)
                        map_user_data_dict['appOpens'].append(appOpens)
        return map_user_data_dict
    def extract_map_insurance_data(self):
        # Code to extract the map insurance data from the file
        map_insurance_data_dict={'State':[], 'Year':[],'Quarter':[],'name':[], 'count':[],'amount':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    
                    for trans_data in json_data['data']['hoverDataList']:
                        name=trans_data['name']
                        count=trans_data['metric'][0]['count']
                        amount=trans_data['metric'][0]['amount']
                        map_insurance_data_dict['State'].append(state_name)
                        map_insurance_data_dict['Year'].append(year)    
                        map_insurance_data_dict['Quarter'].append(int(quarter.strip('.json')))
                        map_insurance_data_dict['name'].append(name)
                        map_insurance_data_dict['count'].append(count)
                        map_insurance_data_dict['amount'].append(amount)

        return map_insurance_data_dict
    def extract_top_trans_insurance_data(self):
        # Code to extract the top transaction data from the file
        top_transaction_data={'State':[], 'Year':[],'Quarter':[],'entityName':[], 'count':[],'amount':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    
                    for district_data in json_data['data']['districts']:
                        
                        entity_name=district_data['entityName']
                        count=district_data['metric']['count']
                        amount=district_data['metric']['amount']
                        top_transaction_data['State'].append(state_name)
                        top_transaction_data['Year'].append(year)
                        top_transaction_data['Quarter'].append(int(quarter.strip('.json')))
                        top_transaction_data['entityName'].append(entity_name)
                        top_transaction_data['count'].append(count)
                        top_transaction_data['amount'].append(amount)
                        
        return top_transaction_data
    def extract_top_user_data(self):
        # Code to extract the top user data from the file
        top_user_data={'State':[], 'Year':[],'Quarter':[],'type':[],'name':[], 'pincode':[], 'registeredUsers':[]}
        for state_name in self.state_list:
            state_dir_path=self.file_path+state_name+"/"
            year_dir_list=os.listdir(state_dir_path)
            for year in year_dir_list:
                year_dir_path=state_dir_path+year+"/"
                quarter_dir_list=os.listdir(year_dir_path)
                for quarter in quarter_dir_list:
                    json_file=year_dir_path+quarter
                    F=open(json_file,'r')
                    json_data=json.load(F)
                    
                    for district_data in json_data['data']['districts']:
                        name=district_data['name']
                        registeredUsers=district_data['registeredUsers']
                        
                        top_user_data['State'].append(state_name)
                        top_user_data['Year'].append(year)
                        top_user_data['Quarter'].append(int(quarter.strip('.json')))
                        top_user_data['name'].append(name)
                        top_user_data['registeredUsers'].append(registeredUsers)
                        top_user_data['pincode'].append(None)
                        top_user_data['type'].append('District')
                    for district_data in json_data['data']['pincodes']:
                        name=district_data['name']
                        registeredUsers=district_data['registeredUsers']
                        
                        top_user_data['State'].append(state_name)
                        top_user_data['Year'].append(year)
                        top_user_data['Quarter'].append(int(quarter.strip('.json')))
                        top_user_data['pincode'].append(name)
                        top_user_data['name'].append(None)
                        top_user_data['registeredUsers'].append(registeredUsers)
                        top_user_data['type'].append('Pincode')
                       
                        
        return top_user_data

class DatabaseInsertion:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')


    def insert_data(self, dataframes):
        # Code to insert the data into the database
        for table_name, df in dataframes.items():
            df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
            print(f"Table {table_name} created and data inserted.")


if __name__ == "__main__":
    aggregated_transaction_data_file_path = "data/aggregated/transaction/country/india/state/"
    aggregated_insurance_data_file_path = "data/aggregated/insurance/country/india/state/"
    aggregated_user_data_file_path   = "data/aggregated/user/country/india/state/"
    aggregated_transaction_data_Obj = DataExtraction(file_path=aggregated_transaction_data_file_path)
    aggregate_transaction_data = aggregated_transaction_data_Obj.aggregated_data_extraction_trans_insurance()
    aggregated_insurance_data_Obj = DataExtraction(file_path=aggregated_insurance_data_file_path)
    aggregate_insurance_data = aggregated_insurance_data_Obj.aggregated_data_extraction_trans_insurance()
    aggregated_user_data_Obj = DataExtraction(file_path=aggregated_user_data_file_path)
    aggregate_user_data = aggregated_user_data_Obj.aggregated_data_extraction_user()
    aggregate_transaction_data_df=pd.DataFrame(aggregate_transaction_data)
    aggregate_insurance_data_df=pd.DataFrame(aggregate_insurance_data)
    aggregate_user_data_df=pd.DataFrame(aggregate_user_data)

    
    # aggregate_transaction_data_df.to_csv("aggregated_transaction_data.csv", index=False)
    # aggregate_insurance_data_df.to_csv("aggregated_insurance_data.csv", index=False)        
    # aggregate_user_data_df.to_csv("aggregated_user_data.csv", index=False)

    map_transaction_data_file_path = "data/map/transaction/hover/country/india/state/"
    map_insurance_data_file_path = "data/map/insurance/hover/country/india/state/"
    map_user_data_file_path   = "data/map/user/hover/country/india/state/"
    map_transaction_data_Obj = DataExtraction(file_path=map_transaction_data_file_path)
    map_transaction_data = map_transaction_data_Obj.extract_map_transcation_data()  
    map_insurance_data_Obj = DataExtraction(file_path=map_insurance_data_file_path)
    map_insurance_data = map_insurance_data_Obj.extract_map_insurance_data()    
    map_user_data_Obj = DataExtraction(file_path=map_user_data_file_path)
    map_user_data = map_user_data_Obj.extract_map_user_data()   
    map_transaction_data_df=pd.DataFrame(map_transaction_data)
    map_insurance_data_df=pd.DataFrame(map_insurance_data)
    map_user_data_df=pd.DataFrame(map_user_data)

    map_transaction_data_df.to_csv("map_transaction_data.csv", index=False)
    map_insurance_data_df.to_csv("map_insurance_data.csv", index=False)
    map_user_data_df.to_csv("map_user_data.csv", index=False)

    top_transaction_data_file_path = "data/top/transaction/country/india/state/"
    top_insurance_data_file_path = "data/top/insurance/country/india/state/"
    top_user_data_file_path   = "data/top/user/country/india/state/"

    top_transaction_data_Obj = DataExtraction(file_path=top_transaction_data_file_path)
    top_insurance_data_Obj = DataExtraction(file_path=top_insurance_data_file_path)
    top_user_data_Obj = DataExtraction(file_path=top_user_data_file_path)
    top_transaction_data = top_transaction_data_Obj.extract_top_trans_insurance_data()
    top_insurance_data = top_insurance_data_Obj.extract_top_trans_insurance_data()
    top_user_data = top_user_data_Obj.extract_top_user_data()
    top_transaction_data_df=pd.DataFrame(top_transaction_data)
    top_insurance_data_df=pd.DataFrame(top_insurance_data)
    top_user_data_df=pd.DataFrame(top_user_data)

    top_transaction_data_df.to_csv("top_transaction_data.csv", index=False)
    top_insurance_data_df.to_csv("top_insurance_data.csv", index=False)
    top_user_data_df.to_csv("top_user_data.csv", index=False)

    dataframes = {
    'aggregated_transaction_data': aggregate_transaction_data_df,
    'aggregated_insurance_data': aggregate_insurance_data_df,
    'aggregated_user_data': aggregate_user_data_df,
    'map_transaction_data': map_transaction_data_df,
    'map_insurance_data': map_insurance_data_df,
    'map_user_data': map_user_data_df,
    'top_transaction_data': top_transaction_data_df,
    'top_insurance_data': top_insurance_data_df,
    'top_user_data': top_user_data_df
}
    # DatabaseInsertion_Obj = DatabaseInsertion(user='root', password=12345, host='localhost', database='phonepay')
    # DatabaseInsertion_Obj.insert_data(dataframes)