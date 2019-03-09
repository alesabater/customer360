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
    "s3_output" : "customer360-{u}-refined-eaberlin/smart_power/customer_activities".format(u=username),
    "columns" : ["business_partner_no", "business_partner_name", "business_partner_lastname", "business_partner_telephone",
                 "business_partner_email", "relation_start_date", "business_partner_birthdate",
                "contract_amount","first_contract_date","contracts","contracts_act","amount_act",
                "first_contract_act_date", "switch_amount", "switch_dates", "avg_billing", "avg_kwh",
                "avg_billing_year", "avg_kwh_year","avg_billing_month", "avg_kwh_month"]
}

dfbilling = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_billing", transformation_ctx = "billing").toDF()
dfcontract = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_contract", transformation_ctx = "contract").toDF()
dfpayment = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_payment", transformation_ctx = "payment").toDF()
dfpartner = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_business_partner", transformation_ctx = "partner").toDF()
dfswitch = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_switch", transformation_ctx = "switch").toDF()
dfconsumption = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_consumption_monthly", transformation_ctx = "consumption").toDF()

# get partner activities
# - Start relation activity
partner_rel = (dfpartner.select("relation_start_date", "business_partner_no") 
                            .withColumnRenamed("business_partner_no", "activity_id") 
                            .withColumnRenamed("relation_start_date", "activity_date") 
                            .withColumn("activity_type", lit("Partner")) 
                            .withColumn("activity_subtype", lit("Relation Start")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache()) 

# Get contract Activities
# Contract start
contract_start = (dfcontract.select("c_contract_start_date", "c_contract_no") 
                            .withColumnRenamed("c_contract_no", "activity_id") 
                            .withColumnRenamed("c_contract_start_date", "activity_date") 
                            .withColumn("activity_type", lit("Contract")) 
                            .withColumn("activity_subtype", lit("Contract Start")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache()) 

contract_end = (dfcontract.select("c_contract_end_date", "c_contract_no") 
                            .withColumnRenamed("c_contract_no", "activity_id") 
                            .withColumnRenamed("c_contract_end_date", "activity_date") 
                            .withColumn("activity_type", lit("Contract")) 
                            .withColumn("activity_subtype", lit("Contract End")) 
                            .filter(year("activity_date") != 9999)
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache()) 

# Get billing Activities
# Bill created
                 
bill_created = (dfbilling.select("b_billing_date", "b_billing_no") 
                            .withColumnRenamed("b_billing_no", "activity_id") 
                            .withColumnRenamed("b_billing_date", "activity_date") 
                            .withColumn("activity_type", lit("Billing")) 
                            .withColumn("activity_subtype", lit("Bill Issued")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache())

payment_created = (dfpayment.select("p_payment_date", "p_payment_no") 
                            .withColumnRenamed("p_payment_no", "activity_id") 
                            .withColumnRenamed("p_payment_date", "activity_date") 
                            .withColumn("activity_type", lit("Billing")) 
                            .withColumn("activity_subtype", lit("Bill Payed")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache())

switch_created = (dfswitch.select("s_switch_date", "s_switch_reason", "s_contract_no") 
                            .withColumnRenamed("s_contract_no", "activity_id") 
                            .withColumnRenamed("s_switch_date", "activity_date") 
                            .withColumn("activity_type", lit("Switch")) 
                            .withColumn("activity_subtype", col("s_switch_reason")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache())

kwh_read = (dfconsumption.select("co_consumption_date", "co_kwh_month", "co_contract_no") 
                            .withColumnRenamed("co_contract_no", "activity_id") 
                            .withColumnRenamed("co_consumption_date", "activity_date") 
                            .withColumn("activity_type", lit("Consumption")) 
                            .withColumn("activity_subtype", lit("Meter Read")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .cache())

dfactivities = (
    partner_rel
    .unionAll(contract_start)
    .unionAll(contract_end_
    .unionAll(bill_created)
    .unionAll(payment_created)
    .unionAll(switch_created)
    .unionAll(kwh_read)
    )

dfattributes.write.partitionBy("year", "month", "day").parquet(parameters['s3_output'])