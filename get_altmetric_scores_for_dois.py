# imports
import csv
import re
import json
import requests
import sys
import datetime

# fields to be scrapped from altmetric
metric_keys = [
    "cited_by_posts_count",
    "cited_by_delicious_count",
    "cited_by_fbwalls_count",
    "cited_by_feeds_count",
    "cited_by_forum_count",
    "cited_by_gplus_count",
    "cited_by_linkedin_count",
    "cited_by_msm_count",
    "cited_by_peer_review_sites_count",
    "cited_by_pinners_count",
    "cited_by_policies_count",
    "cited_by_qs_count",
    "cited_by_rdts_count",
    "cited_by_rh_count",
    "cited_by_tweeters_count",
    "cited_by_videos_count",
    "cited_by_weibo_count",
    "cited_by_wikipedia_count"
    "score"
]

# relevant errors for user (printed in output csv)
error_csv = "Errors: \nDOIs not found:\n"
number_of_errors = 0

def getInputFile():
    input_fi = ""
    # check if file name was provied as parameter
    if len(sys.argv) > 1:
        input_fi = str(sys.argv[1])

    # otherwise ask for it
    else:
        print("Please specify your input file. \nExample: test.csv")
        input_fi = input("Enter file name: ")
    return input_fi


def getDOIs(input_file):
    doi_list_csv = open(input_file, "r", encoding="latin1")
    doi_list = csv.reader(doi_list_csv, delimiter=";")
    dois = []

    next(doi_list) # skip header

    for doi in doi_list:
        dois.append(doi[0])

    print("Found", len(dois), "DOIs in input list.\n")
    doi_list_csv.close()
    return dois


def createOutputFile(input_file_name):
    output_file = input_file_name + "_result.csv"

    output_dois = open(output_file, "w")
    tablehead = "DOI;Title;Autor;Year_published;" + ";".join(metric_keys) + " \n"
    output_dois.write(tablehead)

    output_dois.close()

    print("Output file '" + output_file + "' was created.\n")
    return output_file


def getInformations(dois, output_file, input_file_name):
    global error_csv
    global number_of_errors
    print("Sending a GET request to the altmetric server.\n")
    for doi in dois:
        # Get request for this doi will be sent to altmetric
        request_url = "https://api.altmetric.com/v1/doi/" + doi
        response = requests.get(request_url)

        if response is None or response.status_code != 200:
            error_msg = "ERROR: There was a problem getting the data from the altmetric server.\nServer response: " + str(response.status_code) + "\nRequested URL: " + str(request_url)
            print(error_msg)
            # errors will be shown in output txt
            error_csv = error_csv + "\n" + str(request_url)
            number_of_errors = number_of_errors + 1
            writeEmptyLine(output_file, doi)

        else:
            # print complete response
            # print(response.json())
            parsed_json = json.loads(response.text)
            print("Found:  ", parsed_json['doi'])
            writeLine(output_file, parsed_json)
        print("\n")
    writeErrors(input_file_name)


def writeException (output_dois, attribute):
    print("WARNING:", attribute, "attribute not found")
    output_dois.write("NULL")


def writeEmptyLine(output_file, doi):
    try:
        with open(output_file, "a") as output_dois:
            try:
                output_dois.write(doi)
            except (Exception):
                writeException(output_dois, "doi")

            output_dois.write("\n")
            print("writing empty line to output file")
        output_dois.close()

    except (OSError, IOError) as e:
        print("ERROR: Output file not found.\n")
        sys.exit(1)


def writeLine(output_file, parsed_json):
    try:
        with open(output_file, "a") as output_dois:
            try:
                output_dois.write(parsed_json["doi"])
            except (Exception):
                writeException(output_dois, "doi")
            output_dois.write(";")

            try:
                output_dois.write('"' + parsed_json["title"] + '"')
            except (Exception):
                writeException(output_dois, "title")
            output_dois.write(";")

            try:
                first_author = parsed_json["authors"][0].rsplit(None, 1)
                try:
                    if (len(first_author[1]) < 3 and first_author[1].isupper()):
                        first_author = first_author[0]
                    else:
                        first_author = first_author[1]
                except (Exception):
                    first_author = first_author[0]
                output_dois.write(first_author.strip())
            except (Exception):
                writeException(output_dois, "authors")
            output_dois.write(";")

            try:
                output_dois.write(datetime.datetime.fromtimestamp(int(parsed_json["published_on"])).strftime('%Y'))
            except (Exception):
                writeException(output_dois, "published_on")
            output_dois.write(";")

            global metric_keys

            for key in metric_keys:
                try:
                    output_dois.write(str(parsed_json[key]))
                except (Exception):
                    writeException(output_dois, key)
                output_dois.write(";")

            output_dois.write("\n")
            print("writing gathered info to output file")
        output_dois.close()

    except (OSError, IOError) as e:
        print("ERROR: Output file not found.\n")
        sys.exit(1)


def writeErrors(input_file_name):
    file_name = str(input_file_name) +  "_errors.txt"
    try:
        with open(file_name, "w") as output_dois:
            output_dois.write(error_csv)
            print("Error file '",file_name,"' was created. ", number_of_errors, "error(s) found.")
        output_dois.close()

    except (OSError, IOError) as e:
        print("ERROR: Output file not found.\n")
        sys.exit(1)


#
# main function
#

if __name__ == "__main__":

    # reads in or asks user for input file
    input_file = getInputFile()

    if input_file != "":
        # creates an output file containing only headings
        input_file_name = input_file.rsplit(".", 1)[0] # remove file extension from name
        output_file = createOutputFile(input_file_name)

        # matches the dois
        dois = getDOIs(input_file)

        # GET request to server
        getInformations(dois, output_file, input_file_name)


    else:
        print("\nERROR: Please enter a valid file name.\n")
        getInputFile()
