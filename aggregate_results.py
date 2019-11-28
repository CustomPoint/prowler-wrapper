#!/bin/env python3
import os
import csv
from pprint import pprint

SCORES = {
    'Show report generation info': 'NO PRINT',
    'Avoid the use of the root account (Scored)': '0 BAD',
    'Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password (Scored)': 'NO PRINT',
    'Ensure credentials unused for 90 days or greater are disabled (Scored)': '0 BAD',
    'Ensure access keys are rotated every 90 days or less (Scored)': '0 BAD',
    'Ensure IAM password policy requires at least one uppercase letter (Scored)': '0 BAD',
    'Ensure IAM password policy require at least one lowercase letter (Scored)': '0 BAD',
    'Ensure IAM password policy require at least one symbol (Scored)': '0 BAD',
    'Ensure IAM password policy require at least one number (Scored)': '0 BAD',
    'Ensure IAM password policy requires minimum length of 14 or greater (Scored)': '0 BAD',
    'Ensure IAM password policy prevents password reuse: 24 or greater (Scored)': '0 BAD',
    'Ensure IAM password policy expires passwords within 90 days or less (Scored)': '0 BAD',
    'Ensure no root account access key exists (Scored)': '0 BAD',
    'Ensure MFA is enabled for the root account (Scored)': 'NO PRINT',
    'Ensure hardware MFA is enabled for the root account (Scored)': 'NO PRINT',
    'Ensure security questions are registered in the AWS account (Not Scored)': '0 BAD',
    'Ensure IAM policies are attached only to groups or roles (Scored)': '0 BAD',
    'Enable detailed billing (Scored)': '0 BAD',
    'Ensure IAM Master and IAM Manager roles are active (Scored)': 'NO PRINT',
    'Maintain current contact details (Scored)': '0 BAD',
    'Ensure security contact information is registered (Scored)': '0 BAD',
    'Ensure IAM instance roles are used for AWS resource access from instances (Not Scored)': '0 BAD',
    'Ensure a support role has been created to manage incidents with AWS Support (Scored)': '0 BAD',
    'Do not setup access keys during initial user setup for all IAM users that have a console password (Not Scored)': '0 BAD',
    'Ensure IAM policies that allow full "*:*" administrative privileges are not created (Scored)': '0 BAD',
    'Ensure CloudTrail is enabled in all regions (Scored)': '0 BAD',
    'Ensure CloudTrail log file validation is enabled (Scored)': '0 BAD',
    'Ensure the S3 bucket CloudTrail logs to is not publicly accessible (Scored)': '0 BAD',
    'Ensure CloudTrail trails are integrated with CloudWatch Logs (Scored)': '0 BAD',
    'Ensure AWS Config is enabled in all regions (Scored)': '1 OK',
    'Ensure S3 bucket access logging is enabled on the CloudTrail S3 bucket (Scored)': '0 BAD',
    'Ensure CloudTrail logs are encrypted at rest using KMS CMKs (Scored)': '0 BAD',
    'Ensure rotation for customer created CMKs is enabled (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for unauthorized API calls (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for Management Console sign-in without MFA (Scored)': 'NO PRINT',
    'Ensure a log metric filter and alarm exist for usage of root account (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for IAM policy changes (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for CloudTrail configuration changes (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for AWS Management Console authentication failures (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for disabling or scheduled deletion of customer created CMKs (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for S3 bucket policy changes (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for AWS Config configuration changes (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for security group changes (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL) (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for changes to network gateways (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for route table changes (Scored)': '0 BAD',
    'Ensure a log metric filter and alarm exist for VPC changes (Scored)': '0 BAD',
    'Ensure appropriate subscribers to each SNS topic (Not Scored)': '0 BAD',
    'Ensure no security groups allow ingress from 0.0.0.0/0 to port 22 (Scored)': '0 BAD',
    'Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389 (Scored)': '0 BAD',
    'Ensure VPC Flow Logging is Enabled in all VPCs (Scored)': '1 OK',
    'Ensure the default security group of every VPC restricts all traffic (Scored)': '0 BAD',
    'Ensure routing tables for VPC peering are "least access" (Not Scored)': '0 BAD',
    'Ensure users with AdministratorAccess policy have MFA tokens enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Ensure there are no EBS Snapshots set as Public (Not Scored) (Not part of CIS benchmark)': '0 BAD',
    'Ensure there are no S3 buckets open to the Everyone or Any AWS user (Not Scored) (Not part of CIS benchmark)': '0 BAD',
    'Ensure there are no Security Groups without ingress filtering being used (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Ensure there are no Security Groups not being used (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Ensure there are no EC2 AMIs set as Public (Not Scored) (Not part of CIS benchmark)': '0 BAD',
    'Ensure there are no ECR repositories set as Public (Not Scored) (Not part of CIS benchmark)': '0 BAD',
    'Ensure there are no Public Accessible RDS instances (Not Scored) (Not part of CIS benchmark)': '0 BAD',
    'Check for internet facing Elastic Load Balancers (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check for internet facing EC2 Instances (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check for Publicly Accessible Redshift Clusters (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if Elasticsearch Service domains allow open access (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if Elasticsearch Service domains have logging enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if Amazon Macie is enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if GuardDuty is enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if CloudFront distributions have logging enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if Elastic Load Balancers have logging enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if S3 buckets have server access logging enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if S3 buckets have Object-level logging enabled in CloudTrail (Not Scored) (Not part of CIS benchmark)':'NO PRINT',
    'Check if Redshift cluster has audit logging enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if Route53 hosted zones are logging queries to CloudWatch Logs (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if Lambda functions invoke API operations are being recorded by CloudTrail (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if API Gateway has logging enabled (Not Scored) (Not part of CIS benchmark)': 'NO PRINT',
    'Check if SQS queues have Server Side Encryption enabled (Not Scored) (Not part of CIS benchmark)':'NO PRINT',
    'Check if ACM certificates have Certificate Transparency logging enabled (Not Scored) (Not part of CIS benchmark)':'NO PRINT',
    'Check if RDS Snapshots are public (Not Scored) (Not part of CIS benchmark)':'NO PRINT',
    'Check if SQS queues have policy set as Public (Not Scored) (Not part of CIS benchmark)':'NO PRINT'
}


def printing_old(records_dict):
    for account, regions in records_dict.items():
        print()
        print("Results for [", account, "]")
        for region, issues in regions.items():
            print("\t Issues in region [", region, "]")
            for issue in issues:
                print("\t - Result:", issue[1], " [ TEST - ", issue[0], "]")


def printing_new(records_dict):
    for account, items in records_dict.items():
        print()
        account_name, account_id = account.split('#')
        print("Results for [", account_name, "] [ ID:", account_id, "]")
        for key, status in items.items():
            if key not in SCORES:
                key = substring_after(key,'] ')
            if key not in SCORES:
                print("= !!! (TODO: Add this to SCORES) Check not found:", key)
                continue
            if 'NO PRINT' in SCORES[key]:
                continue
            nr_bad_regions = len(status['bad_regions'])
            nr_ok_regions = len(status['ok_regions'])
            if SCORES[key] == '0 BAD' and nr_bad_regions > 0:
                pass
            elif '1 OK' in SCORES[key] and nr_bad_regions > 0 and nr_ok_regions == 0:
                pass
            else:
                continue

            print('\t -', key, "[ -", nr_bad_regions, '+', nr_ok_regions, " ]", " = ", SCORES[key])
            for region, issue in status['bad_regions']:
                print('\t \t =', region, ':', issue)


def construct_dict(records_warning):
    ordered_dict = {}
    for record in records_warning:
        profile = record['PROFILE'] + "#" + record['ACCOUNT_NUM']
        title_text = record['TITLE_TEXT']
        if profile not in ordered_dict:
            ordered_dict[profile] = {}
        if title_text not in ordered_dict[profile]:
            ordered_dict[profile][title_text] = {'bad_regions': [], 'ok_regions': []}

        if "WARN" in record['RESULT'] or "FAIL" in record['RESULT']:
            ordered_dict[profile][title_text]['bad_regions'].append((record['REGION'], record['NOTES']))
        else:
            ordered_dict[profile][title_text]['ok_regions'].append((record['REGION'], record['NOTES']))
    return ordered_dict


def filter_warn(list_of_records):
    records_w_warn = [record for record in list_of_records if "WARN" in record['RESULT']]
    print("= Filtered records with warnings")
    return records_w_warn

def substring_after(s, delim):
    return s.partition(delim)[2]

def get_all_csv_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        file_list = [root + "/" + f for f in files]
    print("= Found CSVs in directory ", path, ":")
    return file_list


def aggregate_results(csv_file_list):
    records_list = []
    for csv_file in csv_file_list:
        with open(csv_file, 'r') as records_file:
            records = csv.DictReader(records_file)
            records_list.extend([x for x in records])
    try:
        print("= Example :", records_list[0])
    except Exception as e:
        print("List is:", records_list)
        raise e
    return records_list


if __name__ == '__main__':
    csv_file_list = get_all_csv_files('reports')
    print("Found the following files: ", csv_file_list)
    records_list = aggregate_results(csv_file_list)
    # TODO: Remove old way of doing things if not necessary
    # records_warning = filter_warn(records_list)
    # records_dict = construct_dict(records_warning)
    # printing(records_dict)

    # TODO: Improve new way of doing things
    records_dict = construct_dict(records_list)
    printing_new(records_dict)

