USE customer
CREATE TABLE table_business_partner (
		BUSINESS_PARTNER_NO VARCHAR(14) NOT NULL,
		BUSINESS_PARTNER_NAME VARCHAR(25) NOT NULL,
		BUSINESS_PARTNER_LASTNAME VARCHAR(25),
		MPRN DATE NOT NULL,
		BUSINESS_PARTNER_TELEPHONE VARCHAR(14),
		BUSINESS_PARTNER_EMAIL VARCHAR(25) NOT NULL,
		BUSINESS_PARTNER_CREDIT_STATUS INT NOT NULL,
		BUSINESS_PARTNER_SPECIAL_NEEDS INT NOT NULL,
		BUSINESS_PARTNER_BIRTHDATE VARCHAR(14) NOT NULL UNIQUE,
	PRIMARY KEY(BUSINESS_PARTNER_NO)
)

CREATE TABLE table_instalment_details (
		INSTALMENT_NO INT NOT NULL UNIQUE,
		METER_CONFIG_CODE INT NOT NULL,
		METER_TYPE VARCHAR NOT NULL,
		METER_READING_UNIT VARCHAR NOT NULL,
		ADDRESS VARCHAR NOT NULL,
		INSTALMENT_DATE DATE NOT NULL
	PRIMARY KEY(INSTALMENT_NO)
)

CREATE TABLE table_switch (
		CONTRACT_NO CHAR(14 CHAR) NOT NULL UNIQUE,
		SWITCH_DATE DOUBLE NOT NULL,
		SWITCH_REASON DATE NOT NULL,
	PRIMARY KEY(CONTRACT_NO)
)