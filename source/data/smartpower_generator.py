import logging
import argparse
from faker import Faker
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()

def read_arguments():
    parser = argparse.ArgumentParser(description='Create Users, S3 buckets and Glue Databases for Customer360 Workshop')
    parser.add_argument('-f', '--file', help='path for JSON file containing users metadata')
    parser.add_argument('-r', '--region', help='Region in which secrets are created', default='eu-west-1')
    parser.add_argument('--delete-s3-buckets', action='store_true', help='Flag to delete all participants S3 buckets')
    parser.add_argument('--delete-glue-databases', action='store_true', help='Flag to delete all participants Glue databases')
    args = parser.parse_args()
    print(args)
    json_arg = vars(args)['file']
    region_arg = vars(args)['region']
    delete_s3 = vars(args)['delete_s3_buckets']
    delete_glue = vars(args)['delete_glue_databases']
    return {'json_path': json_arg, 'region': region_arg, 'delete_s3': delete_s3, 'delete_glue': delete_glue}


def main():
    args = read_arguments()


if __name__ == '__main__':
    main()
