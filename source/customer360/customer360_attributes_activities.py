import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from awsglue.dynamicframe import DynamicFrame
import datetime


args = getResolvedOptions(sys.argv, ['JOB_NAME', 'username'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

username = args['username']
parameters = {
    "trusted_db" : "{u}_trusted_db".format(u=username),
    "s3_output_attributes" : "s3://customer360-{u}-refined-eaberlin/customer_attributes".format(u=username),
    "s3_output_activities" : "s3://customer360-{u}-refined-eaberlin/customer_activities".format(u=username),
    "attributes_columns" : [
        "business_partner_no", 
        "business_partner_name", 
        "business_partner_lastname", 
        "business_partner_telephone",
        "business_partner_email",  
        "business_partner_birthdate",
        "relation_start_date", 
        "contract_amount",
        "contracts",
        "contracts_act",
        "amount_act",
        "switch_amount", 
        "switch_dates", 
        "avg_billing", 
        "avg_kwh", 
        "bill_qty",
        "payment_qty"],
    "activities_columns" : ["activity_type", "activity_subtype", "activity_id", "activity_date", "year", "month", "day"]
}

dfbilling = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_billing", transformation_ctx = "billing").toDF()
dfcontract = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_contract", transformation_ctx = "contract").toDF()
dfpayment = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_payment", transformation_ctx = "payment").toDF()
dfpartner = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_business_partner", transformation_ctx = "partner").toDF()
dfswitch = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_switch", transformation_ctx = "switch").toDF()
dfconsumption = glueContext.create_dynamic_frame.from_catalog(database = parameters['trusted_db'], table_name = "trusted_table_consumption_monthly", transformation_ctx = "consumption").toDF()


#################################################################################################################################################################################
##                                                          Create Customer Attributes                                                                                         ##
#################################################################################################################################################################################

# Get contract information 
contract_amt = (dfcontract
                .groupBy(col("c_business_partner_no"))
                .agg(
                    collect_set("c_contract_no").alias("contracts"),
                    count("*").alias("contract_amount"),
                    min("c_contract_start_date").alias("first_contract_date"))
                .cache())

contract_act_amt = (dfcontract.filter(year("c_contract_end_date")==9999)
                    .groupBy("c_business_partner_no")
                    .agg(
                        collect_set("c_contract_no").alias("contracts_act"),
                        count("*").alias("amount_act"),
                        min("c_contract_start_date").alias("first_contract_act_date"))
                    .withColumnRenamed("c_business_partner_no","c_act_business_partner_no")
                    .cache())

# Get switch amount
switch_amt = (dfswitch
             .groupBy("s_business_partner_no").agg(
                 count("*").alias("switch_amount"), 
                 collect_list("s_switch_date").alias("switch_dates"))
             .cache())

# Get Billing information
billing_avg_partner = (dfbilling
                      .groupBy("b_business_partner_no")
                      .agg(
                          avg("b_billing_amount").alias("avg_billing"),
                          avg("b_billing_kwh").alias("avg_kwh"),
                          count("b_billing_date").alias("bill_qty")
                          )
                       .cache())

payment_qty = (dfpayment
                      .groupBy("p_business_partner_no")
                      .agg(
                          count("p_payment_date").alias("payment_qty")      
                          )
                      .cache())

# Create Attributes DataFrame
dfattributes = (dfpartner
              .join(contract_amt, col("business_partner_no")==col("c_business_partner_no"), "left_outer")
              .join(contract_act_amt, col("business_partner_no")==col("c_act_business_partner_no"), "left_outer")
              .join(switch_amt, col("business_partner_no")==col("s_business_partner_no"), "left_outer")
              .join(billing_avg_partner, col("business_partner_no")==col("b_business_partner_no"), "left_outer")
              .join(payment_qty, col("business_partner_no")==col("p_business_partner_no"), "left_outer")
              .select(parameters['attributes_columns'])
             )


# Write Attributes to S3
dfattributes.repartition(5).write.mode("overwrite").parquet(parameters['s3_output_attributes'])

#################################################################################################################################################################################
##                                                          Create Customer Activities                                                                                         ##
#################################################################################################################################################################################


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
                            .select(parameters['activities_columns'])
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
                            .select(parameters['activities_columns'])
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
                            .select(parameters['activities_columns'])
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
                            .select(parameters['activities_columns'])
                            .cache())

payment_created = (dfpayment.select("p_payment_date", "p_payment_no") 
                            .withColumnRenamed("p_payment_no", "activity_id") 
                            .withColumnRenamed("p_payment_date", "activity_date") 
                            .withColumn("activity_type", lit("Billing")) 
                            .withColumn("activity_subtype", lit("Bill Payed")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .select(parameters['activities_columns'])
                            .cache())

switch_created = (dfswitch.select("s_switch_date", "s_switch_reason", "s_contract_no") 
                            .withColumnRenamed("s_contract_no", "activity_id") 
                            .withColumnRenamed("s_switch_date", "activity_date") 
                            .withColumn("activity_type", lit("Switch")) 
                            .withColumn("activity_subtype", col("s_switch_reason")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .select(parameters['activities_columns'])
                            .cache())

kwh_read = (dfconsumption.select("co_consumption_date", "co_kwh_month", "co_contract_no") 
                            .withColumnRenamed("co_contract_no", "activity_id") 
                            .withColumnRenamed("co_consumption_date", "activity_date") 
                            .withColumn("activity_type", lit("Consumption")) 
                            .withColumn("activity_subtype", lit("Meter Read")) 
                            .withColumn("year", year(col("activity_date"))) 
                            .withColumn("month", month(col("activity_date")))
                            .withColumn("day", dayofmonth(col("activity_date")))
                            .select(parameters['activities_columns'])
                            .cache())

# Get Customer Activities
dfactivities = (
    partner_rel
    .unionAll(contract_start)
    .unionAll(contract_end)
    .unionAll(bill_created)
    .unionAll(payment_created)
    .unionAll(switch_created)
    .unionAll(kwh_read)
    )

# Write Activities to S3
dfactivities.repartition(5).write.mode("overwrite").parquet(parameters['s3_output_activities'])