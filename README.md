# **DSG Python3 Utilities**

This is the source code for the python3 `dsgutils` package

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
	
- `pivot_by_2_categories` :Create pivot table of df by category 1 and category 2.
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- cat1 - str (Required)
		we group df by column cat1
		- cat2 - str (Required)
		we group by column cat2
	- **Returns**
	pivot table 
	
- `date_to_month_year` :Create year column and month column from a specific column of the dataframe. 
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- date_col - date64 (Required)
		The date column
	- **Returns**
	pivot table 
	
- `delete_value_to_igonore` :  Remove values of certain columns in the dataframe.  
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- unused_columns - list (Required)
		List of columns we want to delete
	- **Returns** 
	- dataframe - pd.DataFrame, the dataframe 
	
- `delete_column_to_ignore` : Remove col in unused_columns if they are still in the dataframe. 
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- col_values_to_ignore - list (Required)
		dictionnary of columns with list values we want to ignore : {col1 : [value1, value2], col2 : [value3, value4]}
	- **Returns** 
	- dataframe - pd.DataFrame, the dataframe 
	
- `change_col_value_to_other` : Change column value of specific column to other value. Add it to change_col_value as a dictionnary
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- change_col_value - Dictionnary (Required)
		Dictionnary of columns were we want to change some values : 
        {col1 : {old_value1: new_value1, old_value2 : new_value2} , col2 : ...}
	- **Returns** 
	- dataframe - pd.DataFrame, the dataframe 
    
- `change_col_to_date_format` : Change time_features to date format 
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- time_features - list (Required)
		list of time_features
	- **Returns** 
	- dataframe - pd.DataFrame, the new dataframe 
- `missing_val_imput` : Change missing value of specific column to specific value 
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- missing_value_imputation - dictionnary (Required)
		dictionnary of columns with value to replace
	- **Returns** 
	- dataframe - pd.DataFrame, the new dataframe 
    
- `delete_rows_missing_keys` : Delete rows with missing keys variables, and show them
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- keys_variables - list (Required)
		List of keys variables in your dataset
	- **Returns** 
	- dataframe - pd.DataFrame, the new dataframe 
    
- `delete_duplicate_rows` : Delete duplicate rows and show a sample of the duplicates.
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
	- **Returns** 
	- dataframe - pd.DataFrame, the new dataframe 

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
	
- `display_df_info` : Method for displaying and overview of the dataframe, including null and unique counts.
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to show counts for
		- df_name - str (Required)
		Title of the dataframe
		- max_rows - int (Optional)
        Number of rows to display from the dataframe
		- max_columns - int (Optional)
        Number of columns to display from the dataframe
	- **Returns**
	None
	
- `display_stacked_bar` : Method for displaying a stacked bar plot given two categorical variables
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to display stacked bar plot for
		- groupby - str (Required)
		Column name by which bars would be grouped
		- on - str (Required)
        Column name of the different bar blocks
		- order - List of column names (Optional)
        Order in which to draw the bars by
        - unit - float (Optional)
        Scale to which unit
        - palette - matplotlib/seaborn color palette (Optional)
        Color palette to use for drawing
        - horizontal - boolean (Optional)
        Horizontal or vertical barplot
        - figsize - tuple (Optional)
        Figure size
	- **Returns**
	pyplot axis object
	   
- `value_count_plot` : Plot value count of every categorical features having less than 30 different values, from a list of categorical features, and list all categorical features having more than 30. 
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to display value count plot for
		- cat_features - list (Required)
		List of column name of which we want the value count plot of (only categories)
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `value_count_top` : Plot value count top values of a list of categorical features. 
	- **Variables (in order)**: 
		- dataframe - pd.DataFrame (Required)
		The dataframe to display plot for
		- cat_features - list (Required)
		List of column name of which we want the value count plot of (only categories)
		- top - int  (Optional)
        Top number of categories you want to see 
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `value_count_bottom` : Plot value count bottom values of a list of categorical features. 
	- **Variables (in order)**: 
		- dataframe - pd.DataFrame (Required)
		The dataframe to display plot for
		- cat_features - list (Required)
		List of column name of which we want the value count plot of (only categories)
		- bottom - int  (Optional)
        Bottom number of categories you want to see 
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `distrib_numerical` : Plot distribution of numerical features with the gaussian kernel density if there are more than 10 different values.
	- **Variables (in order)**: 
		- dataframe - pd.DataFrame (Required)
		The dataframe to display plot for
		- numerical_feat - list (Required)
		List of column name of which we want the value count plot of
		- percentiles - int (Optional)
        Removes the bottom and top outliers
		- kde - boolean (Optional)
        If True, plot a gaussian kernel density estimate for the distribution
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `box_plot_continuous` :Plot box_plot of continuous features.
	- **Variables (in order)**: 
		- dataframe - pd.DataFrame (Required)
		The dataframe to display plot for
		- cont_feat - list (Required)
		List of column name of which we want the box plot of
		- percentiles - int (Optional)
        Removes the bottom and top outliers
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `count_month_year` :    Plot number of raws per month_col and year_col
	- **Variables (in order)**: 
		- dataframe - pd.DataFrame (Required)
		The dataframe to display plot for
		- month_col - str (Required)
		Month column
		- year_col - str (Required)
        Year column
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `count_plot_col_per_date` :    Count of number of row per date and another column
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe to display plot for
		- date_col - str (Required)
		date column
		- col - str (Required)
        The other column we want to see  
		- num_label - int (Optional)
        We show x labels only every num_label
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `countplot_cat1` : Plot the number of rows per categories in column cat1
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- cat1 - str (Required)
		We will show the number of sample for each value in this columns
		- title_suffix - str (Optional)
        If we want to add a suffix to the title 
		- perc - str (Optional)
        If True, plot percentage of the data instead of the number of sample    
		- num_label - int (Optional)
        We show x labels only every num_label
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `density_plot_cat1` : Density plot of column cat1 with bins
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- cat1 - str (Required)
		We will show the number of sample for each value in this columns
		- bins - int (Required)
         Choose number of bins you want to set
		- kde - boolean (Optional)
        If True, plot a gaussian kernel density estimate for the distribution
		- title_suffix - str (Optional)
        If we want to add a suffix to the title 
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `num_of_cat2_per_cat1` : Number of different values of column cat2 for every category of column cat1
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- cat1 - str (Required)
		We group df by column cat1
		- cat2 - str (Required)
		We count the number of different values of column cat2 in every category of column cat1
		- figsize - tuple (Optional)
         Choose the figsize you want to set
		- normalize - boolean (Optional)
        If True, Normalize the counts
		- num_label - int (Optional)
        W show x labels only every num_label
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `count_of_cat2_per_cat1` : Count of the Number of different values of column cat2 for every category of column cat1
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- cat1 - str (Required)
		We group df by column cat1
		- cat2 - str (Required)
		We show the number of sample for each value in column cat2
		- figsize - tuple (Optional)
         Choose the figsize you want to set
		- normalize - boolean (Optional)
        If True, Normalize the counts
		- xlim - int (Optional)
        If we want to set a limit on x on the plot
		- ylim - int (Optional)
        If we want to set a limit on x on the plot        
		- num_label - int (Optional)
        W show x labels only every num_label
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `boxplot_2_features` :Box plot of different categories of column x, for values of y
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe
		- x - str (Required)
		we group df by column x
		- y - str (Required)
		we group by column y
		- ylim - int (Optional)
        If we want to set a limit on y on the plot  
		- set_y_limit - bolean (Optional)
        True if we want to set a limit on y on the plot
		- order_boxplot - bolean (Optional)
        True if we want to order the plot by the value count of x
		- print_value - bolean (Optional)
        True if we want to print the value count of x       
		- num_label - int (Optional)
        W show x labels only every num_label
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `scatter_2_features` :Box plot of different categories of column x, for values of y
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- x - str (Required)
		we group df by column x
		- y - str (Required)
		we scatter at the values of y for every category of x
		- ylim - int (Optional)
        If we want to set a limit on y on the plot  
		- set_y_limit - bolean (Optional)
        True if we want to set a limit on y on the plot
		- xlim - int (Optional)
        If we want to set a limit on x on the plot  
		- set_x_limit - bolean (Optional)
        True if we want to set a limit on x on the plot
		- order_boxplot - bolean (Optional)
        True if we want to order the plot by the value count of x
		- print_value - bolean (Optional)
        True if we want to print the value count of x       
		- num_label - int (Optional)
        W show x labels only every num_label
	- **Returns**
	None
	
- `stacked_bar_plot` :    Stacked Bar Plot Number of samples per cat1 and cat2
	- **Variables (in order)**:
		- dataframe - pd.DataFrame (Required)
		The dataframe 
		- cat1 - str (Required)
		we group df by column cat1
		- cat2 - str (Required)
		we group by column cat2
		- bar_size - int (Optional)
        size of the bars        
		- nan_colums_thresh - float (Optional)
        Drops rows having more than nan_colums_thresh Nan values        
		- figsize - tuple (Optional)
        size of the figure
		- percentile - float (Optional)
        if we want to hide what over the 100-percentile and under percentile of the data
		- plot_flag - bolean (Optional)
        if == 1, lot the graph        
		- normalize - bolean (Optional)
        if True, plot a Normalize by the sum of the row
		- sort_bars - bolean (Optional)
        sort the search term index in descending order
		- return_pivot - bolean (Optional)
        if True, return the pivot table       
	- **Returns**
	None
	
- `plot_correlations_per_categories` : Correlation plot of cat1 with target_y, grouped by cat2
	- **Variables (in order)**:(df_plot, cat1, cat2, feature_x, target_y, title_suffix = ''):
		- df_plot - pd.DataFrame (Required)
		The dataframe we want to see with the column 'Correlation' of cat1 and cat2 
		- cat1 - str (Required)
		we group df by column cat1
		- cat2 - str (Required)
		we group by column 		
        - feature_x - str (Required)
		we group df by column cat1
		- target_y - str (Required)
		we group by column cat2
		- title_suffix - str (Optional)
        If we want to add a suffix to the title 
	- **Returns**
	None
	
- `percentage_missing_plots` : Plot percentage of NaN values in DataFrame, having more than perc_missing missing values
	- **Variables (in order)**:
		- df_plot - pd.DataFrame (Required)
		The dataframe we want to see
		- perc_missing - int (Optional)
		max percentage of missing value we don't want to show
		- save_plot - boolean (Optional)
        True if you want to save plot
		- path_dir - str  (Optional)
        Path diretory if you want to save the plot
	- **Returns**
	None
	
- `data_categorical` : List all object type columns, print number of unique values for every categorical feature, print 5 unique samples if every Categorical feature
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
		- cat_features - list (Optional)
		Known list of categorical features (can be empty)
		- cont_features - list (Optional)
        Known list of continuous features (can be empty)
	- **Returns**
	cat_features - list : list of categorical features
	
- `data_continuous` : Return a list of int or float type columns, convert all columns of cont_features to numericPrint the description of all continuous features
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
		- cat_features - list (Optional)
		Known list of categorical features (can be empty)
		- cont_features - list (Optional)
        Known list of continuous features (can be empty)
	- **Returns**
	cont_features - list : list of continuous features    
	
- `data_all_types` : Print the type of every columns in the data.
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
	- **Returns**
	None
    
- `zero_one_card` : Show 1 or 0 cardinality columns 
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
	- **Returns**
	None
    
- `same_num_of_unique_val` : Show columns having same number of unique value 
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
	- **Returns**
	None
    
- `show_data` : Print the number of rows of the data loaded and shows the first five rows. 
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
	- **Returns**
	None    
    
### Feateng
`from dsgutils.pd.feateng import...`

- `alphanumeric_feature` : Convert text column to alpha numeric column, replacing non alpha numeric with a space. 
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		The dataframe we want to see 
		- text_column - str (Required)
		The column containing text
	- **Returns**
		- df_new - pd.DataFrame
        The new Dataframe

- `one_hot_encode` : Gets a DataFrame and a categorical column, and replace the
    column with one hot encoded vectors. If the values in the
    column are a list of categories, then the values are split
    according to the given delimiter. The user has an option of
    selecting cat_amount most frequent categories to take into
    consideration (limiting the amount of categories / vectors) 
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		to create one hot encoded vectors for 
		- feature_name - str (Required)
		Categorical feature to turn to one hot vectors
		- prefix - Prefix to attach to the one-hot vector names
		- is_list - Flag to indicate whether the values in feature_name are a list of categories
		- delim - If the values are a list, the delimiter to split the categories
		- cat_amount - Number of most frequent categories to turn to one-hot vectors                        Default is 0, meaning one-hot encode all categories
	- **Returns** None


- `get_time_features` : Add the following features to the dataframe, derived from the timestamp: year, month, day, hour, minute, second, weekday name and day of the year.
	- **Variables (in order)**:
		- df - pd.DataFrame (Required)
		 dataframe to add time features to 
		- datetime_col - str (Required)
		column name of the timestamp (can be a string column or of the type datetime)
		- datetime_format - date format
		- prefix - prefix for new column names
	- **Returns** None

### Text_Preprocess

- `clean_punctuation` : Strip string of punctuation. 
	- **Variables (in order)**:
		- s - a string to strip of punctuation (Required)
		- punc_to_keep - a set with all the punctuation marks to keep as a string, with no spaces e.g. {$#}
	- **Returns**
		- a string stripped of punctuation


- `remove_non_ascii` :Remove non-ASCII characters from list of tokenized words. 
	- **Variables (in order)**:
		- word - a word to clean, string (Required)
	- **Returns**
		- the original word with only ascii characters

- `unite_standalone_uppercase` : Unite single capital letters on a row, to one word. e.g.: U S A -> USA. 
	- **Variables (in order)**:
		- str_to_fix - word to examine and fix, string (Required)
	- **Returns**
		- new string with united single capital letters

- `camel_case_split` : Seperate camel case words to two single words. 
	- **Variables (in order)**:
		- str_to_split - a word to seperate, string (Required)
	- **Returns**
		- new string with split camel case words

- `lemmatize_word` : Lemmatize word according to the given POS tag. 
	- **Variables (in order)**:
		- word - a word to lemmatize, string (Required)
		- pos - part of speech tag: 's' / 'a' / 'r' / 'v' / 'n' / 'adverb', string (Required)
	- **Returns**
		- the lemmatized word

- `normalize_word` : Transform the given word from/to POS tags. 
	- **Variables (in order)**:
		- word - word to normalize, string (Required)
		- from_pos - Part of speach the word is in, string (Required)
		- to_pos - part of speech to convert to, string (Required) 
	- **Returns**
		- normalized word

### General 

- `cosine_list_similarity` : Get cosine similarity between two lists. 
	- **Variables (in order)**:
		- list_a - first list to compare (Required)
		- list_b - second list to compare (Required)
	- **Returns**
		- cosine similarity between the lists [0, 1]