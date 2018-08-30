import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML

def display_corr_matrix(dataframe, on_columns, ax=None, cmap=None, **heatmap_kwargs):
    """
    Displays a triangular correlation matrix
    :param dataframe: DataFrame to display correlation for
    :param on_columns: List of numerical column names to display correlation for
    :param ax: Axis to plot on
    :param cmap: Color map for the correlation matrix
    :param heatmap_kwargs: Key word arguments that acceptable by seaborn.heatmap
    :return: matplotlib.Axis object
    """
    df = dataframe[on_columns]

    # Compute the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    if not ax:
        f, ax = plt.subplots(figsize=(15, 13))

    if not cmap:
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Use default kwargs only if none were supplied
    default_kwargs = {
        'vmax': 1,
        'vmin': -1,
        'center': 0,
        'square': True,
        'linewidths': .5,
        'cbar_kws': {'shrink': .5}
    }

    for def_key, def_val in default_kwargs.items():
        if def_key not in heatmap_kwargs:
            heatmap_kwargs[def_key] = def_val

    ax = sns.heatmap(corr, mask=mask, cmap=cmap, ax=ax, **heatmap_kwargs)

    return ax


def display_df_info(df, df_name, max_rows=None, max_columns=None):
    """
    Display data and stats (null counts, unique counts and data types)
    :param df: DataFrame to display
    :param df_name: Name for the dataframe
    :param max_rows: Maximum rows to display on the table overview (stats always include the entire dataframe)
    :param max_columns: Maximum columns to display on the table overview (stats always include the entire dataframe)
    """
    # Head
    display(HTML('<h4>{name}</h4>'.format(
        name=df_name)))
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):
        display(df)

    # Attributes
    display(HTML("<h4>Data attributes</h4>"))
    display_df = pd.DataFrame.from_dict(
        {'Null counts': df.isnull().sum(), 'Data types': df.dtypes, 'Unique values': df.nunique()})
    display(display_df)


def display_stacked_cat_bar(df, groupby, on, order=None, unit=None, palette=None, horizontal=True, figsize=(11, 11)):
    """
    Displays a stacked bar plot given two categorical variables
    :param df: DataFrame to display data from
    :param groupby: Column name by which bars would be grouped
    :param on: Column name of the different bar blocks
    :param order: Order in which to draw the bars by
    :param unit: Scale to which unit
    :param palette: Color palette to use for drawing
    :param horizontal: Horizontal or vertical barplot
    :param figsize: Figure size
    :return: matplotlib.Axis object
    """

    # Create a binary dataframe
    stacked_bar_df = pd.concat([df[groupby], pd.get_dummies(df[on])], axis=1)
    bins = list(stacked_bar_df.columns[1:])
    stacked_bar_df = stacked_bar_df.groupby(groupby)[bins].sum().reset_index()

    if order:
        if not isinstance(order, list):
            raise ValueError('"order" must be a list')
        if set(order) != set(bins):
            raise ValueError('"order" iterable must contain all possible values: {}'.format(str(bins)))

        stacked_bar_df = stacked_bar_df[[groupby] + order]
        bins = order

    # Scale if given unit
    if unit:
        # Calculate total
        stacked_bar_df['total'] = stacked_bar_df[bins].sum(axis=1)

        # Scale
        for bin_label in bins:
            stacked_bar_df[bin_label] /= stacked_bar_df['total']
            stacked_bar_df[bin_label] *= unit

        # Drop irrelevant 'total' column
        stacked_bar_df = stacked_bar_df.iloc[:, :-1]

    # Cumsum row wise
    for idx in range(1, len(bins)):
        stacked_bar_df[bins[idx]] = stacked_bar_df[bins[idx]] + stacked_bar_df[bins[idx - 1]]

    # Get relevant palette
    if palette:
        palette = palette[:len(bins)]
    else:
        palette = sns.color_palette()[:len(bins)]

    # Plot
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)

    if horizontal:
        for color, bin_label in reversed(list(zip(palette, bins))):
            sns.barplot(y=groupby, x=bin_label, data=stacked_bar_df, color=color, label=bin_label, ax=ax)
    else:
        for color, bin_label in reversed(list(zip(palette, bins))):
            sns.barplot(x=groupby, y=bin_label, data=stacked_bar_df, color=color, label=bin_label, ax=ax)

    ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')

    if unit:
        if horizontal:
            ax.set(xlim=(0, unit))
        else:
            ax.set(ylim=(0, unit))

    if horizontal:
        ax.set(xlabel='')
    else:
        ax.set(ylabel='')

    return ax
