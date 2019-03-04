from faker import Faker
import random
from smartpower_models import *
from random import *
from datetime import datetime
from datetime import timedelta
from numpy.random import choice

def BusinessPartnerFaker(fake):
    name = fake.first_name()
    last_name = fake.last_name()
    tlf = fake.phone_number()
    email = fake.email()
    birth = fake.date_time_between(start_date="-65y", end_date="-30y", tzinfo=None)
    customer_start = fake.date_time_between(start_date="-4y", end_date="now", tzinfo=None)
    address = fake.address().replace('\n',' ')
    no = fake.random_number(digits=8, fix_len=True)
    b = BusinessPartner(no, name, last_name, tlf, email, birth, customer_start, address)
    return b


def ContractFaker(fake, bn):
    contract_types = ['Household', 'Enterprise'] 
    no = fake.random_number(digits=6, fix_len=True)
    contract_type = fake.word(ext_word_list=contract_types)
    start_date = fake.date_time_between(start_date=bn.customer_start, end_date=(bn.customer_start + timedelta(days=30)), tzinfo=None)
    if random() > 0.4:
        end_date = datetime.strptime('9999-01-01', '%Y-%M-%d')
    else:
        end_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
    ebill = fake.word(ext_word_list=['TRUE','FALSE'])
    c = Contract(bn.business_no, no, contract_type, start_date, end_date, ebill)
    return c

def BillFaker(fake, co, date):
    bill_bp_no = co.business_no
    bill_co_no = co.contract_no
    bill_no = fake.random_number(digits=8, fix_len=True)
    bill_date = date
    bill_amount = 60.00 * (random() * 3)
    if co.ebill_flag == 'TRUE':
        bill_type = 'email'
    else:
        bill_type = 'paper'
    b = Bill(bill_bp_no, bill_co_no, bill_no, bill_date, bill_type, bill_amount)
    return b

 
def PaymentFaker(fake, bill, meta):
    if 'PaymentType' in meta:
        payment_types = meta['PaymentType'] 
    else:
        payment_types = ['Direct Debit', 'Pre-paid', 'Bank Deposit', 'Mail'] 
    if 'PaymentProb' in meta:
        payment_types_probs = meta['PaymentProb'] 
    else:
        payment_types_probs = [0.6, 0.20, 0.17, 0.3] 
    if 'PaymentDelay' in meta:
        payment_delay = meta['PaymentDelay'] 
    else:
        payment_delay = 10
    meta = choice(payment_types, 1, payment_types_probs)
    payment_type = meta[0]
    payment_bp_no = bill.business_no
    payment_co_no = bill.contract_no
    payment_bill_no = bill.billing_no
    payment_no = fake.random_number(digits=8, fix_len=True)
    payment_turnaround = int(payment_delay * (random() * 3))
    payment_date = bill.billing_date + timedelta(days=payment_turnaround)
    payment_amount = bill.amount
    p = Payment(payment_bp_no, payment_co_no, payment_bill_no, payment_no, payment_date, payment_amount, payment_type)
    return p