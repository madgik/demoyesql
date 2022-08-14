import sqlparse
st = sqlparse.parse('log10 from (rand from (generate_series select count(*), 6 from (generate_series select count(*),10 from (optimizers) as T) S));')
