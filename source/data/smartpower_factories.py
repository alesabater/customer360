from faker import Faker
import random
from smartpower_models import *
from random import *
from datetime import datetime, timedelta
from numpy.random import choice

def BusinessPartnerFaker(fake, meta):
    tenure = meta['Tenure']
    bp_name = fake.first_name()
    bp_last_name = fake.last_name()
    bp_tlf = fake.phone_number()
    bp_email = fake.email()
    bp_birth = fake.date_time_between(start_date="-65y", end_date="-30y", tzinfo=None)
    bp_customer_start = fake.date_time_between(start_date=tenure, end_date="now", tzinfo=None)
    bp_address = fake.address().replace('\n',' ')
    bp_no = fake.random_number(digits=8, fix_len=True)
    return BusinessPartner(bp_no, bp_name, bp_last_name, bp_tlf, bp_email, bp_birth, bp_customer_start, bp_address)

def ContractFaker(fake, meta, partner):
    co_types = meta['ContractTypes']
    co_types_prob = meta['ContractTypesProb']
    co_type = choice(co_types, 1, co_types_prob)
    co_bp_no = partner.business_no
    co_no = fake.random_number(digits=6, fix_len=True)
    co_start_date = fake.date_time_between(start_date=partner.customer_start, end_date=(partner.customer_start + timedelta(days=30)), tzinfo=None)
    if random() > meta['ContractRunningProb']:
        # Running Contracts
        co_end_date = datetime.strptime('9999-01-01', '%Y-%M-%d')
    else:
        # Ended Contracts
        co_end_date = fake.date_time_between(start_date=co_start_date, end_date="now", tzinfo=None)
    co_ebill = fake.word(ext_word_list=['TRUE','FALSE'])
    return Contract(co_bp_no, co_no, co_type, co_start_date, co_end_date, co_ebill)
    

def BillFaker(fake, meta, contract, date):
    bill_bp_no = contract.business_no
    bill_co_no = contract.contract_no
    bill_no = fake.random_number(digits=8, fix_len=True)
    bill_date = date
    bill_amount = 60.00 * (random() * 3)
    if contract.ebill_flag == 'TRUE':
        bill_type = 'email'
    else:
        bill_type = 'paper'
    return Bill(bill_bp_no, bill_co_no, bill_no, bill_date, bill_type, bill_amount)

def PaymentFaker(fake, meta, bill):
    payment_types = meta['PaymentType'] 
    payment_types_probs = meta['PaymentTypeProb']
    payment_delay = meta['PaymentDelay'] 
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