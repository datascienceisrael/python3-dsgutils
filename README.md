# **DSG Python3 Utilities**

This is the source code for the `dsgutils` python3 package

----------

## **Contents**

### Pandas data munging
`from dsgutils.pd.munging import...`

- `drop_by_cardinality` : Method for dropping columns from a dataframe based on their cardinality.
- `order_df` : Method for ordering the columns of a dataframe for better readability. Not all columns must be specified, can supply only a subset of columns. Supports declaring first columns and/or last columns.