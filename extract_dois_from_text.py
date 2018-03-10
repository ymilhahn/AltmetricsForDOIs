# imports
import csv
import re
import sys


# Regex pattern for DOI
# Source: https://github.com/bcaller/markdown_doi/blob/master/markdown_doi/md_doi.py
doi_pattern = r'''(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b(?![\d\-_@]))'''
doi_word = r'''\bdoi\b'''
# counts the number of the word DOI - used for tracking possible errors
doi_count = 0

def getInputFile():
    input_fi = ""
    # check if file name was provied as parameter
    if len(sys.argv) > 1:
        input_fi = str(sys.argv[1])

    # otherwise ask for it
    else:
        print("Please specify your input file. \nExample: myFulltext.txt")
        input_fi = input("Enter file name: ")
    return input_fi

def readInDocument(input_file):
    try:
        with open(input_file, "r", newline='') as csvfile:
            print("\nReading document.\n")
            line_count = 0
            document = ""
            reader = csv.reader(csvfile)
            for row in reader:
                for element in row:
                    document = document + element
                    document = document + "\n"
                line_count = line_count + 1
            print("Read ", line_count, "lines.")
            return document
    except (OSError, IOError) as e:
        print("ERROR: Input file not found.\n")
        sys.exit(1)


def matchDOIs(document):
    # matches all DOis and word "doi"
    matches_doi = re.findall(doi_pattern, document, re.DOTALL)
    matches_word = re.findall(doi_word, document, re.DOTALL | re.IGNORECASE)

    # counter
    n_doi = len(matches_doi)

    # notifies the user if no dois  could be matched
    if n_doi ==  0:
        printErrors("WARNING: No DOIs found.\n")
    # tries to find out if regex might have missed some dois
    if len(matches_word) !=  n_doi:
        printErrors("WARNING: DOIs could not be matched correctly.\nThe word count of 'doi' or 'DOI' does not match the number of DOIs identified.")
        printErrors("Found " + str(len(matches_word)) + " mentions of the phrase 'doi' and 'DOI'.\n")

    print("Found", n_doi, "DOIs.\n")

    # shows all doi matches
    # print("The following matches were found:")
    # print(matches_doi, "\n")

    return matches_doi

def printErrors(error):
    # TODO:
    # could print errors to the new csv
    print(error)


def createOutputFile(input_file_name):
    # prints all identified dois in new csv
    print("Creating output file with all identified DOIs.\n")

    output_file = input_file_name + "_dois.csv"

    output_dois = open(output_file,"w")
    output_dois.write("DOI\n")

    counter = 0
    for doi in matches_doi:
        if counter != len(matches_doi) - 1:
            dois = doi + "\n"
        else:
            dois = doi
        output_dois.write(dois)
        counter = counter + 1
    output_dois.close()
    print("Output file with the name", output_file, "was created.\n")


#
# main function
#

if __name__ == "__main__":
    # reads in or asks user for input file
    input_file = getInputFile()

    if input_file != "":
        # reads in the provided document
        document = readInDocument(input_file)

        # matches the dois
        matches_doi = matchDOIs(document)

        # creates an output file containing all dois
        input_file_name = input_file.rsplit(".", 1)[0] # remove file extension from name
        createOutputFile(input_file_name)

    else:
        print("\nERROR: Please enter a valid file name.\n")
        getInputFile()
