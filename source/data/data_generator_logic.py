import logging
import argparse
import json
import logging
from numpy.random import choice
from datetime import datetime
from logging.config import fileConfig
from smartpower_factories import BusinessPartnerFaker, ContractFaker, BillFaker, PaymentFaker

fileConfig('logging_config.ini')
logger = logging.getLogger()

def generate_business_partner(fake, meta):
    partners = list()
    partner = BusinessPartnerFaker(fake, meta)
    partners.append(partner)
    logger.info("Generated Business Partner with number: {n}".format(n=partner.business_no))
    return partners

def generate_contracts(fake, meta, partner):
    contracts = list()
    for c in range(meta['ContractsAmount']):
        contract = ContractFaker(fake, meta, partner)
        logger.debug("Generated Contract with number: {n}".format(n=contract.contract_no))
        contracts.append(contract) 
    return contracts

def get_monthly_dates(start, end):
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

def generate_bills(fake, meta, contracts):
    bills = []
    for contract in contracts:
        bill_dates = get_monthly_dates(contract.start_date, contract.end_date)
        for date in bill_dates:
            bill = BillFaker(fake, meta, contract, date)
            logger.debug("Generated Bill with number: {n}".format(n=bill.billing_no))
            bills.append(bill)
    return sorted(bills)

def generate_payments(fake, meta, bills):
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
            payment = PaymentFaker(fake, meta, b)
            logger.debug("Generated Payment with number: {n}".format(n=payment.payment_no))
            payments.append(payment)
    return sorted(payments)