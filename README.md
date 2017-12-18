# **DSG Python3 Utilities**

This is the source code for the `dsgutils` python3 package

See [`examples`](https://github.com/datascienceisrael/python3-dsgutils/blob/master/examples.ipynb) for usage examples.

----------
# **Documentation**

## **Pandas**

### Munging
`from dsgutils.pd.munging import...`

- `drop_by_cardinality` : Method for dropping columns from a dataframe based on their cardinality.
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to drop values from
		- values_to_drop - list of values or integer (Optional, default is 1) 
		Columns where their cardinality is one of the values will be dropped. All null columns are of cardinality 0.
		- returned_dropped - boolean (Optional, default is False)
		Whether to return the dropped columns, if True will return a tuple of the new dataframe and a dictionary with column names and cardinality of dropped columns
	- **Returns**
	pd.DataFrame, or (pd.DataFrame, dict) dependent on the `return_dropped` value
- `order_df` : Method for ordering the columns of a dataframe for better readability
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe to order
		- first - list of column names (Optional, []) 
		List of the columns to bring to the front, in order
		- last - list of column names (Optional, []) 
		List of the columns to put at the end, in order
	- **Returns**
	pd.DataFrame
- `camelcase2snake_case` : Method for renaming columns from CamelCase to snake_case format
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to rename its columns
	- **Returns**
	pd.DataFrame

### Viz
`from dsgutils.pd.viz import...`

- `display_corr_matrix` : Method for plotting a correlation matrix for a subset of its columns
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to plot correlation matrix for
		- on_columns - list of columns (Required)
		Columns for which to plot the correlation matrix for
		- ax - pyplot axis object (Optional)
		The axis to plot to, if not supplied will create one and return it
		- cmap - pyplot color map object (Optional)
		Color map for the correlation plot 
		- heatmap_kwargs - can supply any of the heatmap kwargs for customization, refer to [seaborn heatmap docs](https://seaborn.pydata.org/generated/seaborn.heatmap.html#seaborn.heatmap) for available arguments 
	- **Returns**
	pyplot axis object