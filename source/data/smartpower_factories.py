from faker import Faker
import random
from smartpower_models import *
from random import *
from datetime import datetime, timedelta, date
from numpy.random import choice
from dateutil.relativedelta import relativedelta


def business_partner_faker(fake, meta):
    bp_type = meta['PartnerType']
    tenure = meta['Tenure']
    bp_name = fake.first_name()
    bp_last_name = fake.last_name()
    bp_tlf = fake.phone_number()
    bp_email = fake.email()
    bp_birth = fake.date_time_between(start_date="-65y", end_date="-30y", tzinfo=None)
    bp_customer_start = fake.date_time_between(start_date=tenure, end_date="now", tzinfo=None)
    bp_address = fake.address().replace('\n',' ')
    bp_no = fake.random_number(digits=8, fix_len=True)
    return BusinessPartner(bp_type, bp_no, bp_name, bp_last_name, bp_tlf, bp_email, bp_birth, bp_customer_start, bp_address)

def contract_faker(fake, meta, partner):
    co_types = meta['ContractTypes']
    co_types_prob = meta['ContractTypesProb']
    co_type = choice(co_types, p=co_types_prob)
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
    

def bill_faker(fake, meta, contract, date):
    bill_bp_no = contract.business_no
    bill_co_no = contract.contract_no
    bill_no = fake.random_number(digits=8, fix_len=True)
    bill_date = date
    kwh_dist = [i[1] for i in meta['KwhRangeMonthlyDist']]
    kwh_range_set = ["{a},{b}".format(a=i[0][1]-i[0][0], b=i[0][0]) for i in meta['KwhRangeMonthlyDist']]
    kwh_range = str(choice(kwh_range_set, p=kwh_dist)).split(",")
    bill_consumption = int(kwh_range[1]) + random() * int(kwh_range[0])
    bill_amount = bill_consumption * meta['KwhRate']
    if contract.ebill_flag == 'TRUE':
        bill_type = 'email'
    else: 
        bill_type = 'paper'
    return Bill(bill_bp_no, bill_co_no, bill_no, bill_date, bill_type, bill_consumption, bill_amount)

def payment_faker(fake, meta, bill):
    payment_types = meta['PaymentType'] 
    payment_types_probs = meta['PaymentTypeProb']
    payment_delay = meta['PaymentDelay'] 
    meta = choice(payment_types, p=payment_types_probs)
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

def switch_faker(fake, meta, contract):
    switch_bp_no = contract.business_no
    switch_co_no = contract.contract_no
    switch_co_date = contract.start_date
    switch_after = meta["SwitchAfter"]
    difference_years = relativedelta(datetime.now(), switch_co_date).years
    after_years = int(difference_years * switch_after)
    try:
        switch_date = switch_co_date.replace(year = switch_co_date.year + after_years)
    except ValueError:
        switch_date = switch_co_date + (date(switch_co_date.year + after_years, 1, 1) - date(switch_co_date.year, 1, 1))
    switch_reason_l = meta["SwitchReasonList"]
    switch_reason_dist = meta["SwitchReasonProb"]
    switch_reason = choice(switch_reason_l, p=switch_reason_dist)
    return Switch(switch_bp_no, switch_co_no, switch_date, switch_reason)