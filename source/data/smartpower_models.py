from datetime import datetime

class BusinessPartner:
    def __init__(self, business_type, business_no, name, last_name, tlf, email, birth, customer_start, address):
        self.business_type = business_type
        self.business_no = business_no
        self.name = name
        self.last_name = last_name
        self.tlf = tlf
        self.email = email
        self.birth = birth
        self.customer_start = customer_start
        self.address = address

    def __str__(self):
        return '("{x}",{bn},"{n}","{ln}","{e}","{tlf}","{b}","{r}","{a}")'.format(
            x=self.business_type,
            bn=self.business_no, 
            n=self.name, 
            ln=self.last_name, 
            e=self.tlf, 
            tlf=self.email, 
            b=self.birth.strftime('%Y-%m-%d'),
            r=self.customer_start.strftime('%Y-%m-%d'),  
            a=self.address)

class Switch:
    def __init__(self, business_partner, contract_no, date, reason):
        self.business_partner = business_partner
        self.contract_no = contract_no
        self.date = date
        self.reason = reason 
    
    def __str__(self):
        return '({bn},{cn},"{t}","{s}")'.format(
            bn=self.business_partner, 
            cn=self.contract_no, 
            t=self.date.strftime('%Y-%m-%d'), 
            s=self.reason)

class Install:
    def __init__(self, no, config_code, meter_type, unit, address, date):
        self.no = no
        self.config_code = config_code
        self.meter_type = meter_type
        self.unit = unit
        self.address = address
        self.date = date

class Contract:
    def __init__(self, business_no, contract_no, contract_type, start_date, end_date, ebill_flag):
        self.business_no = business_no
        self.contract_no = contract_no
        self.contract_type = contract_type
        self.start_date = start_date
        self.end_date = end_date
        self.ebill_flag = ebill_flag
    
    def __str__(self):
        return '({bn},{cn},"{t}","{s}","{e}",{eb})'.format(
            bn=self.business_no, 
            cn=self.contract_no, 
            t=self.contract_type, 
            s=self.start_date.strftime('%Y-%m-%d'), 
            e=self.end_date.strftime('%Y-%m-%d'), 
            eb=self.ebill_flag)

class Bill:
    def __init__(self, business_no, contract_no, billing_no, billing_date, billing_type, billing_consumption, amount):
        self.business_no = business_no
        self.contract_no = contract_no
        self.billing_no = billing_no
        self.billing_date = billing_date
        self.billing_type = billing_type
        self.billing_consumption = billing_consumption
        self.amount = amount
    
    def get_consumption(self):
        return '({bn},{cn},"{t}",{s})'.format(
            bn=self.business_no, 
            cn=self.contract_no, 
            t=self.billing_date.strftime('%Y-%m-%d'), 
            s=self.billing_consumption)
    
    def __str__(self):
        return '({bn},{cn},{t},"{s}","{e}",{c},{eb})'.format(
            bn=self.business_no, 
            cn=self.contract_no, 
            t=self.billing_no, 
            s=self.billing_date.strftime('%Y-%m-%d'), 
            e=self.billing_type, 
            c=self.billing_consumption,
            eb=self.amount)
    
    def __lt__(self, other):
         return self.billing_date < other.billing_date

class Payment:
    def __init__(self, business_no, contract_no, billing_no, payment_no, payment_date, payment_amount, payment_type):
        self.business_no = business_no
        self.contract_no = contract_no
        self.billing_no = billing_no
        self.payment_no = payment_no
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.payment_type = payment_type
    
    def __str__(self):
        return '({bn},{cn},{t},{s},"{e}",{eb},"{x}")'.format(
            bn=self.business_no, 
            cn=self.contract_no, 
            t=self.billing_no, 
            s=self.payment_no, 
            e=self.payment_date.strftime('%Y-%m-%d'), 
            eb=self.payment_amount,
            x=self.payment_type)
    
    def __lt__(self, other):
         return self.payment_date < other.payment_date
