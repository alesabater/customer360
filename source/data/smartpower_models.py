from datetime import datetime

class BusinessPartner:
    def __init__(self, business_no, name, last_name, tlf, email, birth, customer_start, address):
        self.business_no = business_no
        self.name = name
        self.last_name = last_name
        self.tlf = tlf
        self.email = email
        self.birth = birth
        self.customer_start = customer_start
        self.address = address

    def __str__(self):
        return '({bn},{n},{ln},{e},{tlf},{b},{s},{a})'.format(
            bn=self.business_no, 
            n=self.name, 
            ln=self.last_name, 
            e=self.tlf, 
            tlf=self.email, 
            b=self.birth.strftime('%Y-%m-%d'), 
            s=self.customer_start.strftime('%Y-%m-%d'), 
            a=self.address)

class Switch:
    def __init__(self, business_partner, contract_no, date, reason):
        self.business_partner = business_partner
        self.contract_no = contract_no
        self.date = date
        self.reason = reason 

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
        return '({bn},{cn},{t},{s},{e},{eb})'.format(
            bn=self.business_no, 
            cn=self.contract_no, 
            t=self.contract_type, 
            s=self.start_date, 
            e=self.end_date.strftime('%Y-%m-%d'), 
            eb=self.ebill_flag)
#
#
#
#
#import factory
#
#class User:
#    def __init__(self, name, email):
#        self.name = name
#        self.email = email
#
#class UserFactory(factory.Factory):
#    name = factory.Faker('name')
#    email = factory.Faker('email')
#
#    class Meta:
#        model = User