import re

import pandas as pd


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



