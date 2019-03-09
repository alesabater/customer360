import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from awsglue.dynamicframe import DynamicFrame

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'username'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
username = args['username']
## @type: DataSource
## @args: [database = "username01_landing_db", table_name = "landing_table_billing", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []



datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "{u}_landing_db".format(u="username01"), table_name = "landing_table_billing", transformation_ctx = "datasource0")
datasource1 = glueContext.create_dynamic_frame.from_catalog(database = "{u}_landing_db".format(u="username01"), table_name = "landing_table_contract", transformation_ctx = "datasource1")
datasource2 = glueContext.create_dynamic_frame.from_catalog(database = "{u}_landing_db".format(u="username01"), table_name = "landing_table_payment", transformation_ctx = "datasource2")
datasource3 = glueContext.create_dynamic_frame.from_catalog(database = "{u}_landing_db".format(u="username01"), table_name = "landing_table_business_partner", transformation_ctx = "datasource3")
datasource4 = glueContext.create_dynamic_frame.from_catalog(database = "{u}_landing_db".format(u="username01"), table_name = "landing_table_switch", transformation_ctx = "datasource4")
datasource5 = glueContext.create_dynamic_frame.from_catalog(database = "{u}_landing_db".format(u="username01"), table_name = "landing_table_consumption_monthly", transformation_ctx = "datasource05")
## @type: ApplyMapping
## @args: [mapping = [("business_partner_no", "long", "business_partner_no", "long"), ("contract_no", "long", "contract_no", "long"), ("billing_no", "long", "billing_no", "long"), ("billing_date", "string", "billing_date", "date"), ("billing_type", "string", "billing_type", "string"), ("billing_kwh", "string", "billing_kwh", "double"), ("billing_amount", "string", "billing_amount", "double")], transformation_ctx = "applymapping1"]
## @return: applymapping0
## @inputs: [frame = datasource0]
applymapping0 = ApplyMapping.apply(frame = datasource0, mappings = [("business_partner_no", "long", "b_business_partner_no", "long"), ("contract_no", "long", "b_contract_no", "long"), ("billing_no", "long", "b_billing_no", "long"), ("billing_date", "string", "b_billing_date", "date"), ("billing_type", "string", "b_billing_type", "string"), ("billing_kwh", "string", "b_billing_kwh", "double"), ("billing_amount", "string", "b_billing_amount", "double")], transformation_ctx = "applymapping0")
applymapping1 = ApplyMapping.apply(frame = datasource1, mappings = [("business_partner_no", "long", "c_business_partner_no", "long"),("contract_no", "long", "c_contract_no", "long"),("contract_type", "string", "c_contract_type", "string"),("contract_start_date", "string", "c_contract_start_date", "date"),("contract_end_date", "string", "c_contract_end_date", "date"),("contract_ebill_flag", "long", "c_contract_ebill_flag", "boolean")], transformation_ctx = "applymapping1")
applymapping2 = ApplyMapping.apply(frame = datasource2, mappings = [("business_partner_no", "long", "p_business_partner_no", "long"),("contract_no", "long", "p_contract_no", "long"), ("billing_no", "long", "p_billing_no", "long"), ("payment_no", "long", "p_payment_no", "long"), ("payment_date", "string", "p_payment_date", "string"), ("payment_amount", "string", "p_payment_amount", "double"), ("payment_type", "string", "p_payment_type", "string")], transformation_ctx = "applymapping2")
applymapping3 = ApplyMapping.apply(frame = datasource3, mappings = [("business_partner_type", "string", "business_partner_type", "string"),("business_partner_no", "long", "business_partner_no", "long"), ("business_partner_name", "string", "business_partner_name", "string"), ("business_partner_lastname", "string", "business_partner_lastname", "string"), ("business_partner_telephone", "string", "business_partner_telephone", "string"), ("business_partner_email", "string", "business_partner_email", "string"), ("business_partner_birthdate", "string", "business_partner_birthdate", "date"), ("business_partner_relation_start", "string", "relation_start_date", "date"),("business_partner_address", "string", "business_partner_address", "string")], transformation_ctx = "applymapping3")
applymapping4 = ApplyMapping.apply(frame = datasource4, mappings = [("business_partner_no", "long", "s_business_partner_no", "long"), ("contract_no", "long", "s_contract_no", "long"), ("switch_date", "string", "s_switch_date", "date"), ("switch_reason", "string", "s_switch_reason", "string")], transformation_ctx = "applymapping4")
applymapping5 = ApplyMapping.apply(frame = datasource5, mappings = [("business_partner_no", "long", "co_business_partner_no", "long"),("contract_no", "long", "co_contract_no", "long"),("c_date", "string", "co_consumption_date", "date"),("kwh_month", "string", "co_kwh_month", "double")], transformation_ctx = "applymapping5")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice0"]
## @return: resolvechoice0
## @inputs: [frame = applymapping0]
resolvechoice0 = ResolveChoice.apply(frame = applymapping0, choice = "make_struct", transformation_ctx = "resolvechoice0")
resolvechoice1 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice1")
resolvechoice2 = ResolveChoice.apply(frame = applymapping2, choice = "make_struct", transformation_ctx = "resolvechoice2")
resolvechoice3 = ResolveChoice.apply(frame = applymapping3, choice = "make_struct", transformation_ctx = "resolvechoice3")
resolvechoice4 = ResolveChoice.apply(frame = applymapping4, choice = "make_struct", transformation_ctx = "resolvechoice4")
resolvechoice5 = ResolveChoice.apply(frame = applymapping5, choice = "make_struct", transformation_ctx = "resolvechoice5")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields0"]
## @return: dropnullfields0
## @inputs: [frame = resolvechoice0]
dropnullfields0 = DropNullFields.apply(frame = resolvechoice0, transformation_ctx = "dropnullfields0")
dropnullfields1 = DropNullFields.apply(frame = resolvechoice1, transformation_ctx = "dropnullfields1")
dropnullfields2 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields2")
dropnullfields3 = DropNullFields.apply(frame = resolvechoice3, transformation_ctx = "dropnullfields3")
dropnullfields4 = DropNullFields.apply(frame = resolvechoice4, transformation_ctx = "dropnullfields4")
dropnullfields5 = DropNullFields.apply(frame = resolvechoice5, transformation_ctx = "dropnullfields5")

#partitiondate0 = dropnullfields0.toDF().withColumn("year", split(col("date"), "-")[0]).withColumn("month", split(col("date"), "-")[1]).withColumn("day", split(col("date"), "-")[2])
#partitiondate1 = dropnullfields1.toDF().withColumn("year", split(col("date"), "-")[0]).withColumn("month", split(col("date"), "-")[1]).withColumn("day", split(col("date"), "-")[2])
#partitiondate2 = dropnullfields2.toDF().withColumn("year", split(col("date"), "-")[0]).withColumn("month", split(col("date"), "-")[1]).withColumn("day", split(col("date"), "-")[2])
#partitiondate3 = dropnullfields3.toDF().withColumn("year", split(col("date"), "-")[0]).withColumn("month", split(col("date"), "-")[1]).withColumn("day", split(col("date"), "-")[2])
#partitiondate4 = dropnullfields4.toDF().withColumn("year", split(col("date"), "-")[0]).withColumn("month", split(col("date"), "-")[1]).withColumn("day", split(col("date"), "-")[2])
#partitiondate5 = dropnullfields5.toDF().withColumn("year", split(col("date"), "-")[0]).withColumn("month", split(col("date"), "-")[1]).withColumn("day", split(col("date"), "-")[2])

#finalframe0 = DynamicFrame.fromDF(partitiondate0, glueContext, "finalframe0")
#finalframe1 = DynamicFrame.fromDF(partitiondate1, glueContext, "finalframe1")
#finalframe2 = DynamicFrame.fromDF(partitiondate2, glueContext, "finalframe2")
#finalframe3 = DynamicFrame.fromDF(partitiondate3, glueContext, "finalframe3")
#finalframe4 = DynamicFrame.fromDF(partitiondate4, glueContext, "finalframe4")
#finalframe5 = DynamicFrame.fromDF(partitiondate5, glueContext, "finalframe5")

output0 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields0, connection_type = "s3", connection_options = {"path":"s3://customer360-{u}-trusted-eaberlin/smart_power/table_billing".format(u=username)}, format = "parquet", transformation_ctx = "output0")
output1 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields1, connection_type = "s3", connection_options = {"path":"s3://customer360-{u}-trusted-eaberlin/smart_power/table_contract".format(u=username)}, format = "parquet", transformation_ctx = "output1")
output2 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields2, connection_type = "s3", connection_options = {"path":"s3://customer360-{u}-trusted-eaberlin/smart_power/table_payment".format(u=username)}, format = "parquet", transformation_ctx = "output2")
output3 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path":"s3://customer360-{u}-trusted-eaberlin/smart_power/table_business_partner".format(u=username)}, format = "parquet", transformation_ctx = "output3")
output4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields4, connection_type = "s3", connection_options = {"path":"s3://customer360-{u}-trusted-eaberlin/smart_power/table_switch".format(u=username)}, format = "parquet", transformation_ctx = "output4")
output5 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields5, connection_type = "s3", connection_options = {"path":"s3://customer360-{u}-trusted-eaberlin/smart_power/table_consumption_monthly".format(u=username)}, format = "parquet", transformation_ctx = "output5")


job.commit()