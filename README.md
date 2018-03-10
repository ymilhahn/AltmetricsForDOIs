Altmetrics for DOIs
===================
A Python script which requests [Altmetric scores](https://api.altmetric.com) for a given list of DOIs of scientific articles and writes the scores to a csv file.

## Background
Altmetrics are an alternative way to measure the impact of research in the scientific community and on society. Altmetric.com gathers scores from a variety of sources, for example mentions on twitter or in mass media articles.  
Through the systematic analysis of altmetric scores it can be measured which research gets attention by society or by the media. One can for example investigate which papers had a public impact over a certain amount of time.

## Installation and execution
Python 3.x is required.  
See official Python Docs: [Python Setup and Usage](https://docs.python.org/3/using/index.html)

## Procedure
### 1. Manual: Create file with DOIs
- Source:
	- can be exported e.g. from scopus.com
	- can be extracted from plaintext (via `extract_dois_from_text.py`)


### 2. Automatic via get_altmetric_scores_for_dois.py
- Asks for the file containing the DOIs
- Sends a request for each DOI to the Altmetric API
- Writes all Altmetric scores for each DOI into a single csv file
- Creates an error file containing all DOIs for which the request wasn't successful

### 3. Manual: Check results file
- Compare the number of rows (plus the number of errors) to the initial number of DOIs to see if the request finished prematurely

## In- and Output

### Input

#### CSV file with DOIs

| Example | [example/myDOIs.csv](./example/myDOIs.csv) |
|-----------------|-------------------|
| File format     | csv               |
| First row       | Header: "DOI"     |
| Following rows  | one row = one DOI |

Consists of one column containing the DOIs of all scientific papers that you want to examine.

### Output
#### results file

| Example | [example/myDOIs_result.csv](./example/myDOIs_result.csv) |
|-----------------|-------------------------------|
| File format     | csv                           |
| First row       | column names                  |
| Following rows  | one row = one DOI/publication |

- `Title` – title of the text corresponding to the DOI
- `Cited by...` – the various altmetric scores as integers, for example the number of times the text was mentioned in a tweet (`cited_by_tweeters_count`) or in a media article (`cited_by_msm_count`)

#### error file

| Example | [example/myDOIs_errors.txt](./example/myDOIs_errors.txt) |
|-----------------|-----|
| File format     | txt |

A list of all errors that occurred, for example all DOIs that were not found on the Altmetric servers.

## API and Data Usage
The API is maintained by Altmetric.  
All data received over the API is [licensed by Altmetric.com](https://api.altmetric.com/index.html#datalicense) and must be attributed.

Consider to [register an API key](https://www.altmetric.com/research-access/) if you need a high volume of data.


## License
- **Conception:** Prof. Dr. Markus Lehmkuhl (KIT & FU Berlin)
- **Implementation:** Yannick Milhahn (TU Berlin & FU Berlin), Clarissa Elisabeth Staudt (TU Berlin & FU Berlin)

Distributed under GPLv3 License. See LICENSE for more information.
