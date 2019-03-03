import logging
import argparse
import json
import logging
from numpy.random import choice
from faker import Faker
from logging.config import fileConfig
from smartpower_factories import BusinessPartnerFaker, ContractFaker
from faker.providers import internet, date_time, person, phone_number, address, lorem

fileConfig('logging_config.ini')
logger = logging.getLogger()

def read_arguments():
    parser = argparse.ArgumentParser(description='Creates Customers for SamrtPower and data with their interactions')
    parser.add_argument('-f', '--file', help='path for JSON file containing customers metadata')
    args = parser.parse_args()
    json_arg = vars(args)['file']
    return {'json_path': json_arg}

def create_customers(n, fake):
    business_partner = list(map(lambda x: BusinessPartnerFaker(fake), range(0,n)))
    return business_partner

def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data

def generate_contracts(fake, n, bp):
    return list(map(lambda x: ContractFaker(fake, bp), range(n)))


def generate_customer_data(fake, specs):
    bp = BusinessPartnerFaker(fake)
    meta = choice(specs['BusinessPartnerFlow'], 1, specs['BusinessPartnerDistribution'])
    co_bp = generate_contracts(fake, meta[0]['Contracts'], bp)
    return {'Customer': bp, 'Contracts': co_bp}

def main():
    fake = Faker('en_GB')
    fake.add_provider(date_time)
    fake.add_provider(person)
    fake.add_provider(phone_number)
    fake.add_provider(internet)
    fake.add_provider(address)
    fake.add_provider(lorem)
    args = read_arguments()

    # Read JSON
    logger.info('Reading JSON file: %s', args['json_path'])
    meta = read_json(args['json_path'])

    # Create Business Partner
    bp_file = open("business_partner.csv","w") 
    co_file = open("contract.csv","w")
    for i in range(meta['BusinessPartners']):
        data = generate_customer_data(fake, meta)
        bp_file.write(str(data['Customer']))
        bp_file.write("\n")
        for c in data['Contracts']: 
            co_file.write(str(c))
            co_file.write("\n")
    bp_file.close()
    co_file.close()


if __name__ == '__main__':
    main()
