import logging
import argparse
import json
import logging
from numpy.random import choice
from faker import Faker
from datetime import datetime
from logging.config import fileConfig
from smartpower_factories import BusinessPartnerFaker, ContractFaker, BillFaker, PaymentFaker
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

def get_billing_dates(start, end):
    bill_dates = []
    while start < end and start < datetime.now():
        bill_dates.append(start)
        day = start.day
        month = start.month
        if day > 28 and month == 1:
            next_day = 28
        elif day > 30:
            next_day = 30
        else:
            next_day = day
        next_month = datetime(int(start.year + (start.month / 12)), ((start.month % 12) + 1), next_day)
        start = next_month
    return bill_dates

def generate_bills(fake, contracts):
    bills = []
    for c in contracts:
        bill_dates = get_billing_dates(c.start_date, c.end_date)
        for date in bill_dates:
            bills.append(BillFaker(fake,c,date))
    return sorted(bills)

def generate_payments(fake, bills, meta):
    payments = []
    if 'InDebtMonths' in meta:
        debt_days = meta['InDebtDays']
    else:
        debt_days = 90
    for b in bills:
        date_diff = datetime.now() - b.billing_date
        if 'InDebt' in meta and date_diff.days < debt_days:
            break
        else:
            payments.append(PaymentFaker(fake,b, meta))
    return sorted(payments)

def generate_customer_data(fake, specs):
    bp = BusinessPartnerFaker(fake)
    meta = choice(specs['BusinessPartnerFlow'], 1, specs['BusinessPartnerDistribution'])
    contracts = generate_contracts(fake, meta[0]['Contracts'], bp)
    bills = generate_bills(fake, contracts)
    payments = generate_payments(fake, bills, meta[0])
    return {
        'Customer': bp, 
        'Contracts': contracts, 
        'Bills': bills, 
        'Payments': payments
    }

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
    bp_file = open("smartpower_insert_stmt/business_partner.sql","w") 
    co_file = open("smartpower_insert_stmt/contract.sql","w")
    bill_file = open("smartpower_insert_stmt/billing.sql","w")
    pay_file = open("smartpower_insert_stmt/payments.sql","w")
    bp_file.write("INSERT INTO table_business_partner VALUES ")
    co_file.write("INSERT INTO table_contract VALUES ")
    bill_file.write("INSERT INTO table_billing VALUES ")
    pay_file.write("INSERT INTO table_payments VALUES ")
    for e in range(meta['BusinessPartners']):
        data = generate_customer_data(fake, meta)
        business_partner = str(data['Customer'])
        contracts = [str(contract) for contract in data['Contracts']]
        bills = [str(bill) for bill in data['Bills']]
        payments = [str(payment) for payment in data['Payments']]
        bp_file.write(business_partner + ",\n")
        co_file.write(",\n".join(contracts) + ",\n")
        bill_file.write(",\n".join(bills) + ",\n")
        pay_file.write(",\n".join(payments) + ",\n")
    bp_file.close()
    co_file.close()
    bill_file.close()
    pay_file.close()
    


if __name__ == '__main__':
    main()
