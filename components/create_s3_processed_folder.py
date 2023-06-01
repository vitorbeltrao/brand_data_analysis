'''
Script to bring raw layer data from s3 to processed, 
performing some transformations

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import boto3
import logging
import datetime

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')