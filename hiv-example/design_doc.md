# Design Document Template

## Overview
We are designing an interface for users to query data from an HIV experiment. XLS file with columns of metadata are associated with a sample ID and each sample also has sequencing information.  We want to build a web interface that can let researchers easily query the system to find sequences subject to metadata constraints. We will have 10000 samples and each sequece is 100kb long.

First version of what we build will use a simple database, and will consist of a script to load data into the database and a simple web form that lets users query easily. We will write a simple script to allow us to query the database. In the future we will make a web interface.

## Background: 
### Motivations
We want to make it easy for HIV researches to correlate clinical measurements with sequences
### Other solutions
TBD
### Current Goals
Simple interface to handle small amounts of data.
Small number of users at once.

### Non-Goals
We don't need to support thousands of users.
We don't need to train ML on this (yet)
We don't need to worry about public access / security; only used within the lab
If input data changes, we can delete and recreate the entire DB, edit/update not required.


### Future goals
train an ML model
Expose the query interface publicly
Expose a method for others to contribute data from the public.
Web interface — we need to design the system to make it easy to make a web interface.

## Detailed Design
We will require that the user provide a CSV file.

We have three major pieces:

1. The part that loads in the data (ETL)

One script will load data fom the CSV file into a SQLite database. Metadata will be loaded from /path/to/csv_file and sequence data will be loadedd from /path/to/sequence/data. Database file will be written to /path/to/database.

`python load_hiv_csv_data.py /path/to/csv_file /path/to/sequence/data /path/to/database.db`

If either input file is not readable or does not exist, print an error and quit.

If the db directory doesn't exist, print an error.

If the db file doesn't exist, we will create a new one and populate with the data

If the db file does exist, we will print an error and quit.
 
The following columns must exist in the CSV file.

for each sample_id in the csv, we will load the sequence data from `$(sample_id).fastq`.

If the sample file does not exist or is not readable for a specific sample: print error message with sample id, quit.

column name in csv — column id in sql — type — nullable
Sample ID — sample_id — unique integer 
Acute_Tx — acute_tx — boolean (in the CSV 0/1)
CCR5 — boolean (in the CSV 0/1)
B57	Viral load — b57_viral_load float NULL if "not detected"
TxInitiation(Yrs)
TxTime (Years)	EGF	FGF-2	IFN-g	IL-7	IL-8	IP-10	MIP_1a	MIP-1b	VEGF	LS-VITROS	VITROS Avidity	Lag	Gal9 (ng/ml)	Japan sGal9 pg/ml	HIV RNA	HIV DNA: Pol	HIV DNA: 2 LTR	HIV RNA/HIV DNA Pol	2LTR%	CD3+CD4+HLA-DR+CD38+	CD3+CD4+PD1+	NAÏVE	TEMRA	CM	EM
Sequence — sequence — BLOB

Ensure that db is only accessible to people who can access input files. (no writing to a+r folders)

Missing data: we will ignore any row with a missing cell except "not detected" in b57 viral load 


2. The database 

We will currrently use SQLite to store the data. We will create one table called `hiv_data` with columns as listed above. The DB will not be edited, and only written once from scratch.

3. The part that queries the database.

`python3 query_hiv_data.py `


TODO: what do we do about missing cell data?? 
For now, we will ignore and log all rows with at least one missing cell.

Sample ids with missing sequences, and vice versa.


### User requirements
< 10 seconds for query
don't need a lot of concurrency
input data doesn't change very often
### New/changed data structures?
N/A
### What APIs will you use/change?
N/A
### Throughput/latency/cost/efficiency concerns?
none
### Data validation/what are potential error states?
input data file has the right columns
data types are correct

### Logging/monitoring/observability
not yet.

### Security/Privacy
we need to think about user privacy because we have sequence data (TBD)

### What will you test?
Corner cases: numbers should be treated as numbers
Corner cases: missing data. Test to ensure that adding a row with missing data does nothing.
End-to-end test: load a CSV, and query to see whether it is in the db.
Seqence testing: test line sequences with line breaks.
Sample ids with missing sequences, and vice versa.

## Third Party dependencies

Library to read fastq files
Library to read CSVs?
Libraries to do computation on the data?
Web interface framework (?) Flask.
DB interface?
What database are we going to use?


## Work Estimates

## Alternative Approaches
Web interface: phase II.
BigQuery: can we just use GCP? Probably but we can do that in phase II when we're sure that this is useful and when we get more scale?



## Related Work?


