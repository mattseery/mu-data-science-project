# Data Science Major Project (Macquarie University)
This github repository contains the code, presentation and key deliverables for the client Lexxe.

## Brief project description
The team of 5 students, including myself, were presented with a corpus of xml files scraped from various online news sites.

The principal requirements set for the team were to submit code that could:
- Detect breaking news items separate from regular news articles and once detected does not return the same story from another news service again.
- Return news articles based on a keyword search and not report the same story from another news provider.

NB: The contact from Lexxe rejected the proposal to use machine learning / natural language processing.

## Results
After multiple testing of the final code submitted to the client, the following results were obtained:
- Multiple testing for detecting breaking news items gave at least 67% accuracy with a maximum of 88% accuracy obtained. This exceeded the 60% minimum accuracy set by the client.
- 5 keywords were tested with 2 exceeding the 60% minimum accuracy. Another 2 words returned 53% accuracy while the last word could only achieve a 25% accuracy.


## Dependencies

### Python Packages
To install dependencies use pip by running `pip install -r ./requirements.txt`or alternatively you can conda by running `conda install --yes --file ./requirements.txt`

See requirements.txt for required python packages.

It is recommended that [Anaconda](https://www.anaconda.com/) or [Miniconda](https://conda.io/miniconda.html) is used as the interpreter.


### Storage

If no articles are found in the configured storage, the program will automatically parse and store all xml files that are found in the `snippet` folder in the route of the project

You can choose between either using a local file, or a MongoDB as a storage backend.
The local file storage (the default setting) requires no configuration.

If using MongoDB, you will need to ensure that the connection settings are correct, the default settings should work with a standard installation of MongoDB. All of these can be edited in either config.yml or via command line arguments.

The Default parameters are:
```
DB:
HOST: 127.0.0.1
PORT: 27017
DB: lexxe
```


#### Articles
The storage has the following schema.

Field Name | Data Type | Details
--- | --- | ---
_id | Mongodb id object | The PK for this document
docid | String | A unique id for the document
date | String | The date the article was scraped
time | String | The time the article was scraped
istopnews | Boolean| Was the article was in the top news section of the site
source | String | The news source
url | String | The URL of the scraped page
title | String | The title of the article
content | String | The contents of the article
Sindices | List of Dicts | The sindex values of the article
datetime | ISO 8601 DateTime object | The date and time the article was scraped


## Configuration

There are two ways to configure the solution. First is via command line arguments, and second is via the config.yml file in the projects root directory.

You can see the command line options for configuration by running `python ./main.py -h`

The command line is preferential in many cases, especially should you want to change the configuration for a single run, however if you want to set up a default configuration that you expect to use in the future, modification of the config.yml file is suggested. Should you not know what certain parameters are for, simply consult the output of the help command as shown above.


A complete list of settings can be found by parsing the help parameter to the program (ie `python ./main.py --help`)


### config.yml
```
LOG_DIR: log
```
The directory we want to log data to.
```
DEFAULT_DATA_PATH: ./snippet
```
The folder we want to load data from should our data store be empty.
```
DB:
  HOST: 127.0.0.1
  PORT: 27017
  DB: lexxe
```
The connection parameters for MongoDB
```
PROCESSING:
  DUPLICATE_DIFFERENCE_THRESHOLD: 0.1
  BREAKING_THRESHOLD: .50
```
The threshold to consider for duplicates and breaking news.

### features.txt
features.txt contains JSON which can be used to configure the features searched for, and how valuable each feature should be.
Features are split into different categories depending on where they should occur.

## Running

The script can be run with the following command. `python ./main.py`

You can also pass the output directly to the evaluation program with the following command  `python ./main.py | python ./evaluator.py`

## Tests

To run tests, simply run: `python -m unittest`

Tests for the project can be found in the tests folder.

You must ensure that tests use the project root as their working directory.


## Troubleshooting

### Missing packages/wrong Python version

If you are seeing issues about missing packages, or having the wrong python version, then it is a good idea to test you are using the correct interpreter.
You can do this by running `python -V` (Note: the V is case sensitive)

If you followed the advice to use Anaconda as the project interpreter, you should see the output:

```
 ~ $ python -V
Python 3.6.5 :: Anaconda, Inc.
```

### Cannot open file ‘main.py’

If you see output similar to:
```
python: can't open file 'main.py': [Errno 2] No such file or directory
```

Please ensure you have navigated to the root directory of the project before running `python ./main.py`

### Collection “Lexxe” is missing or unavailable

Under certain configurations, Pymongo may not automatically create the database and collection. In such a scenario, simply use compass or the command line to create a “Lexxe” database, and “articles” collection like so:

![mongodb-troubleshoot](mongo-troubleshoot.jpg)