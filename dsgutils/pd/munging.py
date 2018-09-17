import re
import numpy as np
import pandas as pd
from IPython.display import display, HTML, Markdown

def printmd(string):
    display(Markdown(string))


def drop_by_cardinality(dataframe, values_to_drop=1, return_dropped=False):
    """
    Drops columns by their cardinality.
    :param dataframe: DataFrame to drop columns from
    :type dataframe: pd.DataFrame
    :param values_to_drop: Which cardinalities to drop
    :type values_to_drop: Iterable
    :param return_dropped: Whether to return the names of the dropped values or not.
    If true a tuple returns with the second value being the list of dropped column names (Default: False)
    :type return_dropped: Boolean
    :return: Returns the new dataframe, or tuple of (dataframe, dict of dropped columns and their cardinality) depends on return_dropped value
    :rtype pd.DataFrame / (pd.DataFrame, dict)
    """

    # Error checks
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("First argument must be a pd.DataFrame")

    if isinstance(values_to_drop, int):
        values_to_drop = [values_to_drop]

    # Compute cardinality
    cardinality = dataframe.nunique()

    # Find columns to drop and their cardinality
    cols_to_drop = dict()
    for value_to_drop in values_to_drop:
        matching = cardinality[cardinality == value_to_drop]
        for col, card in zip(matching.index, matching):
            cols_to_drop[col] = card

    # Drop the columns
    for col in cols_to_drop:
        dataframe.drop(col, axis=1, inplace=True)

    if return_dropped:
        return dataframe, cols_to_drop
    else:
        return dataframe


def order_df(df, first=None, last=None):
    """
    Order a dataframe that the 'first' columns are first and 'last' are last. It is not necessary to provide
    all the columns, if a subset of the columns is supplied, the columns not supplied columns will stay inplace.
    :param df: Dataframe to order
    :type df: pd.DataFrame
    :param first: List of columns to put first
    :type first: list
    :param last: List of columns to put last
    :type last: list
    :return: Ordered dataframe
    :rtype pd.DataFrame
    """
    if not first:
        first = []
    if not last:
        last = []
    # Order the columns in a more convenient manner

    first.extend(list(set(df.columns) - set(first) - set(last)))

    if last:
        first.extend(last)

    return df[first]


def camelcase2snake_case(dataframe):
    """
    Converts columns from CamelCase to snake_case
    :param dataframe: Dataframe to convert its columns
    :type dataframe: pd.DataFrame
    :return: Dataframe with snake_case columns
    :rtype pd.DataFrame
    """

    def convert(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    return dataframe.rename(columns={old_col: convert(old_col) for old_col in dataframe.columns})


def pivot_by_2_categories(df, cat1, cat2):
    """
    Create pivot table of df by category 1 and category 2.
    param: df: the dataframe
    param: cat1: the first category
    param: cat2: the second category
    return: pivot table 
    """
    # Stacked dataframe of cat2 VS cat1
    df_for_pivot = df[[cat1, cat2]].groupby([cat1, cat2]).size().reset_index(name='counts')
    df_pivot = df_for_pivot.pivot(index=cat1, columns=cat2, values='counts')
    return(df_pivot)


def date_to_month_year(df, date_col):
    """
    Create year column and month column from a specific column of the dataframe. 
    param: df: the dataframe
    param: date_col: the date column
    """
    df_new = df
    if date_col != None :
        df_new[str(date_col +'_year')] = pd.DatetimeIndex(df_new[date_col]).year
        df_new[str(date_col +'_month')] = pd.DatetimeIndex(df_new[date_col]).month
    return(df_new)


def delete_column_to_ignore(df, unused_columns):
    """
    Remove col in unused_columns if they are still in the dataframe. 
    param: df: the dataframe
    param: unused_columns: List of columns we want to delete
    param: df : the dataframe
    """
    unused_columns = list(set(unused_columns))
    del_cols = []
    df_new = df.copy()
    for col in unused_columns:
        if col in df_new.columns:
            del df_new[col]
            del_cols.append(col)
    if del_cols!= []:
        printmd(str('* Columns *'+ ', '.join(del_cols)+ '* removed from DataFrame'))
    return(df_new)


def delete_value_to_igonore(df, col_values_to_ignore):
    """
    Remove values of certain columns in the dataframe. 
    param: df: the dataframe
    param: col_values_to_ignore: dictionnary of columns with list values we want to ignore : {col1 : [value1, value2], col2 : [value3, value4]}
    param: df : the dataframe
    """
    df_new = df.copy()
    for col in col_values_to_ignore:
        df_new = df_new[~df_new[col].isin(col_values_to_ignore[col])]
        printmd(str("* Value *"+ str(' '.join(col_values_to_ignore[col])) +"* from column *" + str(col)+"* is removed"))
    printmd(str("* New data shape :"+ str(df_new.shape)))
    return(df_new)


def change_col_value_to_other(df, change_col_value ):
    """
    Change column value of specific column to other value. Add it to change_col_value as a dictionnary
    param: df : dataframe 
    param: change_col_value : dictionnary of value we want to change
    {col1 : {old_value1: new_value1, old_value2 : new_value2} , col2 : ...}
    return: df : the changed datafarame 
        
    """
    if change_col_value != {}:
        for col in change_col_value:
            if col in df.columns:
                for old_value in change_col_value[col]:
                    if old_value in df[col].unique():
                        new_value = change_col_value[col][old_value]
                        df[col].replace(old_value, new_value, inplace=True)
                printmd(str('* In *'+ col + "* values : " + ', '.join(set(change_col_value[col].keys())) + ' were changed to ' +
                            ', '.join(set(change_col_value[col].values()))))
    else:
        printmd(str('* No Specific Value of column to change '))
    return(df)


def change_col_to_date_format(df, time_features):
    """
    Change time_features to date format    
    param: df : dataframe 
    param: time_features : list of time_features 
    return: df : the changed datafarame 
    
    """
    for time_column in time_features :
        df[time_column]= pd.to_datetime(df[time_column])
    if time_features != 0:
        printmd(str("* *" + ', '.join(time_features) + '*  changed to date time type'))

    return(df)


def missing_val_imput(df, missing_value_imputation):
    """ 
    Change missing value of specific column to specific value
    param: df: dataframe 
    param: missing_value_imputation : dictionnary of columns with value to replace 
    return : df_new : the new dataframe
    """
    if missing_value_imputation != {}:
        df_new = df.copy()
        del df
        for col in list(missing_value_imputation.keys()) :
            df_new[col] = df_new[col].replace(np.nan ,missing_value_imputation[col])
            printmd(str("* In column *"+ str(col) + '* Nan were replaced by *'+ str(missing_value_imputation[col])+ '*' ))
    else:
        printmd("* No Missing value to replace in any column")
    return(df_new)


def delete_rows_missing_keys(df, keys_variables):
    """
    Delete rows with missing keys variables, and show them
    param: df: the dataframe
    param: keys_variables: List of keys variables in your dataset 
    return: df: the Dataframe
    """
    df1 = df.copy()
    initial = df1.shape[0]
    for col in keys_variables:
        df1 = df1.dropna(subset=[col])
        if initial-df1.shape[0] > 0:
            print('Column ', col, ' has ', str(initial-df1.shape[0]), ' Na(s).')
            df_merge = pd.merge(df, df1, how='outer', indicator=True)
            rows_in_df1_not_in_df2 = df_merge[df_merge['_merge']=='left_only'][df.columns]
            print(rows_in_df1_not_in_df2)
    printmd(str("In total, "+str(initial-df1.shape[0])+" rows contains NAs in the key variables"))
    return (df1)


def delete_duplicate_rows(df):
    """
    Delete duplicate rows and show a sample of the duplicates.
    param: df: the dataframe
    return: df: the Dataframe
    """
    initial = df.shape[0]
    df1 = df.copy().drop_duplicates()
    if initial-df1.shape[0] !=0 :
        printmd(str("* " + str(initial-df1.shape[0])+" duplicates were removed"))
        print('Sample of the duplicates :')
        print(df[df.duplicated(keep=False)].drop_duplicates().head(n=10))
    else : 
        printmd(str("* ")+ "No duplicates")
    return (df1)