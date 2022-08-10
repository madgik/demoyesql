# YeSQL Demo

## Instructions

Download pypy3 from here https://www.pypy.org or run `apt-get install pypy3`. 

run 

`
cd interface/src/
pypy3 madserver.py
`

connect to a browser at http://localhost:8080/ and upload udfs/paste and run queries.

The queries run in the demo is available at `interface/src/queries.sql` 
and the UDF shown is available at `interface/src/udf.sql`

The users are allowed to create and test their own UDFs and queries. This demo scenario uses the sqlite database stored at 
`interface/src/nsf_projects.db`. 
This database contains two tables: 1) `nsf` which contains one column `grantid` and 2) `publication` which contains two columns `c1` with an identifier and `c2` with the full text of the publication.
The users could also create more tables with various schemata in this database file to test more YeSQL features.


More examples, datasets and documentation for integration with MonetDB and SQLite are available at https://github.com/athenarc/YeSQL

