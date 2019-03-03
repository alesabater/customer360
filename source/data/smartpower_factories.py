from faker import Faker
from smartpower_models import *
from random import *
from datetime import datetime
from datetime import timedelta

def BusinessPartnerFaker(fake):
    name = fake.first_name()
    last_name = fake.last_name()
    tlf = fake.phone_number()
    email = fake.email()
    birth = fake.date_time_between(start_date="-65y", end_date="-30y", tzinfo=None)
    customer_start = fake.date_time_between(start_date="-10y", end_date="now", tzinfo=None)
    address = fake.address().replace('\n',' ')
    no = fake.random_number(digits=8, fix_len=True)
    b = BusinessPartner(no, name, last_name, tlf, email, birth, customer_start, address)
    return b


def ContractFaker(fake, bn):
    contract_types = ['Household', 'Enterprise'] 
    no = fake.random_number(digits=6, fix_len=True)
    contract_type = fake.word(ext_word_list=contract_types)
    start_date = fake.date_time_between(start_date=bn.customer_start, end_date=(bn.customer_start + timedelta(days=30)), tzinfo=None)
    print(start_date)
    if random() > 0.4:
        end_date = datetime.strptime('9999-01-01', '%Y-%M-%d')
    else:
        end_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
    ebill = fake.word(ext_word_list=['true','false'])
    c = Contract(bn.business_no, no, contract_type, start_date, end_date, ebill)
    return c
