import logging
import argparse
import json
import logging
from numpy.random import choice
from faker import Faker
from datetime import datetime
from logging.config import fileConfig
from data_generator_logic import generate_bills, generate_contracts, generate_business_partner, generate_payments
from faker.providers import internet, date_time, person, phone_number, address, lorem

fileConfig('logging_config.ini')
logger = logging.getLogger()

def read_arguments():
    parser = argparse.ArgumentParser(description='Creates Customers for SamrtPower and data with their interactions')
    parser.add_argument('-f', '--file', help='path for JSON file containing customers metadata')
    args = parser.parse_args()
    json_arg = vars(args)['file']
    return {'json_path': json_arg}

def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data

def create_file(file, table):
    path_prefix = "./smartpower_insert_stmt/"
    file_o = open(path_prefix + file, "w")
    file_o.write('INSERT INTO {t} VALUES '.format(t=table))
    return {file: file_o}

def open_get_files(file_list):
    files = [create_file(f['file'], f['table']) for f in file_list]
    return files

def write_data(files, data): 

    for f, datum in data.items():
        datum_fmt = [str(item) for item in datum]
        [item[f].write(",\n".join(datum_fmt)) for item in files if f in item.keys()]

        
        
        #print(type(",\n".join(datum_fmt)))
          #  for file in files:
           #     if f 
        #print([item for item in files if f in item.values()])
        #files[f].write(",\n".join(datum_fmt))

def close_files(files):
    for f in files:
        [ff.close() for ff in f.values()]

def init_faker_providers():
    fake = Faker('en_GB')
    fake.add_provider(date_time)
    fake.add_provider(person)
    fake.add_provider(phone_number)
    fake.add_provider(internet)
    fake.add_provider(address)
    fake.add_provider(lorem)
    return fake

def generate_customer_data(fake, meta_profiles):
    # Select Profile type to create
    meta = choice(meta_profiles['BusinessPartnerFlow'], 1, meta_profiles['BusinessPartnerDistribution'])[0]
    # Start data generation for customer
    partner = generate_business_partner(fake, meta)
    contracts = generate_contracts(fake, meta, partner[0]) 
    bills = generate_bills(fake, meta, contracts)
    payments = generate_payments(fake, meta, bills)
    # Return results using same file names
    return {
        'business_partner': partner, 
        'contract': contracts, 
        'billing': bills, 
        'payment': payments
    }

def main():
    args = read_arguments()
    files = [
        {'file': 'business_partner', 'table':'table_business_partner'},
        {'file': 'contract', 'table':'table_billing'},
        {'file': 'billing', 'table':'table_contract'},
        {'file': 'payment', 'table':'table_payment'},
        {'file': 'switch', 'table':'table_switch'}
    ]
    logger.info('Insert Files to be created: \n ' + str(files))

    # Read JSON
    logger.info('Reading JSON file: %s', args['json_path'])
    meta = read_json(args['json_path'])

    # Get faker instance
    logger.info('Initialize and add Faker Providers')
    fake = init_faker_providers()

    # Open Insert files
    files = open_get_files(files)

    # Create Business Partner and its related data
    partners_no = meta['BusinessPartners']
    logger.info('Initiating the creation of {bp} Business Partners'.format(bp=partners_no))
    for p in range(partners_no):
        data = generate_customer_data(fake, meta)
        write_data(files, data)
    close_files(files)

if __name__ == '__main__':
    main()