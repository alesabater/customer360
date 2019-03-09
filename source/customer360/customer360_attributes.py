import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from awsglue.dynamicframe import DynamicFrame

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

username = "username01"
parameters = {
    "trusted_db" : "{u}_trusted_db".format(u=username),
    "s3_output" : "customer360-{u}-trusted-eaberlin/smart_power".format(u=username)
}

billing = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_billing", transformation_ctx = "billing")
contract = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_contract", transformation_ctx = "contract")
payment = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_payment", transformation_ctx = "payment")
partner = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_business_partner", transformation_ctx = "partner")
switch = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_switch", transformation_ctx = "switch")
consumption = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_consumption_monthly", transformation_ctx = "consumption")

contract.printSchema()

# Get contract amount
contract_amt = contract.toDF().filter(col("c_business_partner_no") == 50919955).groupBy(col("c_business_partner_no")).count().cache()