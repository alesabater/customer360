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
    "s3_output" : "customer360-{u}-trusted-eaberlin/smart_power/customer_attributes".format(u=username),
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

# Get contract information 
contract_amt = (dfcontract.filter(col("c_business_partner_no") == 50919955)
                .groupBy(col("c_business_partner_no"))
                .agg(
                    collect_set("c_contract_no").alias("contracts"),
                    count("*").alias("contract_amount"),
                    min("c_contract_start_date").alias("first_contract_date"))
                .cache())

contract_act_amt = (dfcontract.filter(year("c_contract_end_date")==9999)
                    .filter(col("c_business_partner_no") == 50919955)
                    .groupBy("c_business_partner_no")
                    .agg(
                        collect_set("c_contract_no").alias("contracts_act"),
                        count("*").alias("amount_act"),
                        min("c_contract_start_date").alias("first_contract_act_date"))
                    .withColumnRenamed("c_business_partner_no","c_act_business_partner_no")
                    .cache())

# Get switch amount
switch_amt = (dfswitch
             .filter(col("s_business_partner_no") == 50919955)
             .groupBy("s_business_partner_no").agg(
                 count("*").alias("switch_amount"), 
                 collect_list("s_switch_date").alias("switch_dates"))
             .cache())

# Get Billing information
billing_avg_partner = (dfbilling
                      .filter(col("b_business_partner_no") == 50919955)
                      .groupBy("b_business_partner_no")
                      .agg(
                          avg("b_billing_amount").alias("avg_billing"),
                          avg("b_billing_kwh").alias("avg_kwh"),
                          )
                       .cache())

billing_avg_year = (dfbilling
                      .filter(col("b_business_partner_no") == 50919955)
                      .withColumn("year", year("b_billing_date"))
                      .groupBy("b_business_partner_no","year")
                      .agg(
                          avg("b_billing_amount").alias("avg_billing_year"),
                          avg("b_billing_kwh").alias("avg_kwh_year"),
                          )
                      .withColumnRenamed("b_business_partner_no","b_year_business_partner_no")
                      .cache())

billing_avg_month = (dfbilling
                      .filter(col("b_business_partner_no") == 50919955)
                      .withColumn("year", year("b_billing_date"))
                      .withColumn("month", month("b_billing_date"))
                      .groupBy("b_business_partner_no","year", "month")
                      .agg(
                          avg("b_billing_amount").alias("avg_billing_month"),
                          avg("b_billing_kwh").alias("avg_kwh_month"),
                          )
                      .withColumnRenamed("b_business_partner_no","b_month_business_partner_no")
                      .cache())

dfattributes = (dfpartner
              .join(contract_amt, col("business_partner_no")==col("c_business_partner_no"))
              .join(contract_act_amt, col("business_partner_no")==col("c_act_business_partner_no"))
              .join(switch_amt, col("business_partner_no")==col("s_business_partner_no"))
              .join(billing_avg_partner, col("business_partner_no")==col("b_business_partner_no"))
              .join(billing_avg_year, col("business_partner_no")==col("b_year_business_partner_no"))
              .join(billing_avg_month, col("business_partner_no")==col("b_month_business_partner_no"))
              .select(parameters['columns'])
             )

dfattributes.write.parquet(parameters['columns'])