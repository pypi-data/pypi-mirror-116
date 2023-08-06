import json
import yaml
import os
import requests

import logging
logging.basicConfig(level=logging.NOTSET)

class ExpensifyClient():
    """
    Python client wrapper for Expensify API endpoints. https://integrations.expensify.com/Integration-Server/doc/#authentication
    """

    HOST = 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations'

    def __init__(self, username, password, sandbox=False):

        self.sandbox = sandbox
        self.password = password
        self.username = username

    ########################################################################
    # Helper Functions                                                     #
    ########################################################################

    def replace_ftl_characters(self, characters):
        """
        Generate the ?replace ftl template for the given list of characters
        :param characters: list of tuples with the character to be replaced and what it's being replaced with
        """
        replace_statements = []
        for character_tuple in characters:
            if "\\" in character_tuple[0]:
                character_tuple[0] = f"\\{character_tuple[0]}"

            replace_statements.append(
                f"?replace(\"{character_tuple[0]}\", \"{character_tuple[1]}\")"
            )

        return "".join(replace_statements)

    def get_report_ftl_transactions(self, transaction_parameters):
        """
        Function that returns the given transaction parameters as FTL template lines. Always return the
        transaction ID to ensure we denote individual transactions
        :param transaction_parameters: List of parameters at the Expensify transaction level
        :type transaction_parameters: list
        :return: FTL string for transactions
        :rtype: str
        """
        transaction_header = "\t\ttransactions:\n" \
                             "\t\t\t<#list report.transactionList as expense>\n"
        transaction_strings = []

        # First transaction denotes it's an individual transaction
        transaction_strings.append(
            f"\t\t\t- transactionID:" + " ${expense.transactionID}\n"
        )
        for parameter in transaction_parameters:
            transaction = f"\t\t\t\t<#if expense.{parameter}?hasContent>\n" \
                          f"\t\t\t\t{parameter}:" + " ${expense." + f"{parameter}" + "}\n" \
                                                                             "\t\t\t\t</#if>\n"
            transaction_strings.append(transaction)

        return transaction_header + "".join(transaction_strings) + "\t\t\t</#list>"


    def get_report_ftl_header(self, report_parameters):
        """
        Function that returns the header of Expensify's ftl template for reports
        :param report_parameters: List of parameters at the Expensify Report Level
        :type report_parameters: list
        :return: FTL string as header for reports
        :rtype: str
        """
        header = "reports:\n" \
                 "<#list reports as report>\n" \
                 "\t${report.reportID}:\n"
        report_fields = []
        for parameter in report_parameters:
            replace_string = self.replace_ftl_characters([(':', '-')])
            report_fields.append(
                f"\t\t{parameter}: " + "${report." + f"{parameter}" + f"{replace_string}\n" + "}\n"
            )

        return header + "".join(report_fields)

    def create_report_ftl_template(self, report_parameters, transaction_parameters):
        """
        Given report_parameters and transaction_parameters create the FTL string for expensify
        :param report_parameters: Dictionary of Expensify parameters at the report level
        :type report_parameters: list
        :param transaction_parameters: Dictionary of Expensify parameters at the transaction level
        :type transaction_parameters: list
        :return: FTL file
        """
        ftl_file = open("ftl_template.ftl", "w")
        header = self.get_report_ftl_header(report_parameters)
        transactions = self.get_report_ftl_transactions(transaction_parameters)
        file_content = header + transactions + "\n</#list>"
        ftl_file.write(file_content)
        ftl_file.close()
        return ftl_file

    def delete_report_ftl_template(self, ftl_file_path):
        """
        Given a ftl file path, delete it
        :param ftl_file_path: File name
        :type ftl_file_path: str
        """
        if os.path.exists(ftl_file_path):
            os.remove(ftl_file_path)
        else:
            logging.info(f"The file at {ftl_file_path} does not exist")


    
    ########################################################################
    # Formatting Functions                                                 #
    ########################################################################

    def get_reports(self, filters, report_parameters, transaction_parameters):
        """
        Return a python dict of reports for the given parameters
        :param filters: Dictionary of Expensify filters on reports
        :type filters: dict
        :param report_parameters: Dictionary of Expensify parameters at the report level
        :type report_parameters: list
        :param transaction_parameters: Dictionary of Expensify parameters at the transaction level
        :type transaction_parameters: list
        :return: Dictionary with report ids as the keys and their corresponding data
        :rtype: dict
        """
        filters = filters if filters else {}

        # Get the .ftl template that will be used to generate the report in Expensify
        export_template = self.generate_report_export_template(report_parameters, transaction_parameters)

        # Create the combination of reports in Expensify's server that we can then download
        file_name = self.get_report_download_file(filters, 'csv', export_template)

        # Download the file content, yaml loads it into a python dictionary
        raw_reports = self.download_reports(file_name)
        csv_reports = raw_reports.decode("utf-8")
        # YAML loader doesn't allow tabs
        csv_reports = csv_reports.replace('\t', '  ')
        reports = yaml.load(csv_reports)['reports']

        return reports

    def generate_report_export_template(self, report_parameters, transaction_parameters):
        """
        Return a template file (.ftl) that, when sent on an API call to Expensify determines
        what report fields will be sent back. Parameters must have 'report_parameters' and
        'transaction_parameters', which are Expensifys defined parameters
        https://integrations.expensify.com/Integration-Server/doc/export_report_template.html
        :param report_parameters: Dictionary of Expensify parameters at the report level
        :type report_parameters: list
        :param transaction_parameters: Dictionary of Expensify parameters at the transaction level
        :type transaction_parameters: list
        :return: file name that is created and can be sent over Expensify's api to download reports
        """
        if not report_parameters or not transaction_parameters:
            logging.error("Report or Transaction parameters not found in generate_report_export_template")
            return
        file = self.create_report_ftl_template(report_parameters, transaction_parameters)

        return file.name

    ########################################################################
    # API Call Functions                                                   #
    ########################################################################

    def get_report_download_file(self, filters, file_type, export_template_name):
        """
        This function takes in a filter for reports and a given export template that defines the fields for each report.
        This hits Expensify's API and returns a report download file which is used to download the reports via the
        Expensify Download Reports function
        :param filters: Dictionary of expensify filters
        :type filters: dict
        :param file_type: String of download type (json, csv, excel)
        :type file_type: str
        :param export_template_name: file name, we search our current directory for the file
        :type export_template_name: str
        :return: String file name
        :rtype: str
        """
        export_template = open(export_template_name, "r")
        export_template_data = export_template.read()
        export_template.close()

        params = {
            "requestJobDescription": json.dumps({
                "type": "file",
                "credentials": {
                    "partnerUserID": self.username,
                    "partnerUserSecret": self.password,
                },
                "onReceive": {
                    "immediateResponse": ["returnRandomFileName"]
                },
                "inputSettings": {
                    "type": "combinedReportData",
                    "filters": filters
                },
                "outputSettings": {
                    "fileExtension": file_type
                },
                "onFinish": []
            })
        }

        payload = {**params, **{"template": export_template_data}}
        headers = {"content-type": "application/x-www-form-urlencoded"}

        response = requests.get(self.HOST, auth=None, params=payload, headers=headers, verify=True, timeout=10.000)

        if response.status_code == 200:
            # Delete our ftl template once we send it
            self.delete_report_ftl_template(export_template_name)

            return response.content.decode("utf-8")
        else:
            logging.error("Failed to fetch download file name from Expensify, API returned: %s" % response.content)

    def download_reports(self, filename):
        """
        Download reports from Expensify API
        :param filename: (str) report filename
        :return: (str) data organized in .ftl template form
        """
        logging.info("triggered action 'expensify_download_reports'")
        payload = {
            "requestJobDescription": json.dumps({
                "type": "download",
                "credentials": {
                    "partnerUserID": self.username,
                    "partnerUserSecret": self.password,
                },
                "fileName": filename,
                "fileSystem": "integrationServer"
            })
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.get(self.HOST, auth=None, params=payload, headers=headers, verify=True, timeout=10.000)

        if response.status_code == 200:
            return response.content
        else:
            logging.error("Failed to fetch a file from Expensify, API returned: %s" % response.content)
