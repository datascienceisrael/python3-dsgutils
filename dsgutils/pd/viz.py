import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML, Markdown
from collections import defaultdict
from itertools import combinations

def printmd(string):
    display(Markdown(string))

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


def display_n_most_correlated(df, n=5, to_color=True):
    """
    Takes a DataFrame and returns a DataFrame of correlations -
    Each column is paired with the n columns most correlated to it

    :param df: DataFrame to display data from
    :param n: number of top values to present
    :param to_color: flag - do the user want to color
                     the correlaton values red and green
    :return: styled correlation dataframe, presenting the top
            n most correlated columns and values per column
    """

    def mask_variable_largest_per_row(df, n_max):
        """
        Create a mask, where only the largest n_max values are kept in the dataframe
        :param df: DataFrame to display data from
        :param n_max: number of top values to keep per row
        :return: css property for styling
        """
        a = df.values
        m, n = a.shape

        nan_row_count = np.isnan(a).sum(1)
        n_reset = n - n_max - nan_row_count
        n_reset.clip(min=0, max=n - 1, out=n_reset)

        sidx = a.argsort(1)
        mask = n_reset[:, None] > np.arange(n)

        c = sidx[mask]
        r = np.repeat(np.arange(m), n_reset)
        a[r, c] = np.nan
        return df

    def color_negative_red_positive_green(val):
        """
        Takes a scalar and returns a string with
        the css property `'color: red'` for negative
        strings, `'color: green'` for positive strings and
        black otherwise.
        :param val: numeric value
        :return: css property for styling
        """
        if val < 0:
            color = 'red'
        elif val > 0:
            color = 'green'
        else:
            color = 'black'

        return 'color: %s' % color

    if not isinstance(df, pd.core.frame.DataFrame):
        raise ValueError('df must be a pandas DataFrame')

    # Set the maximal number of columns to consider
    n = min(n, len(df._get_numeric_data().columns))

    # Compute the correlation matrix
    corrs = df[list(set(df._get_numeric_data().columns))].corr()
    corrs[corrs == 1] = np.nan

    # Manipulate the correlation matrix to get the top n values
    corrs_sorted_inner = mask_variable_largest_per_row(corrs, n).stack() \
        .groupby(level=[0]).apply(lambda x: x.groupby(level=[1]).sum().sort_values(ascending=False))

    corrs_outer_sorted = corrs_sorted_inner.groupby(level=[0]).sum().sort_values(ascending=False)

    corrs_sorted_total = pd.DataFrame(corrs_sorted_inner.reindex(index=corrs_outer_sorted.index, level=0), \
                                      columns=['Correlation Value'])

    corrs_sorted_total.index.name = ['Column', 'Top Correlated Columns']

    # Color values
    if to_color:
        corrs_sorted_total = corrs_sorted_total.style.applymap(color_negative_red_positive_green)

    return corrs_sorted_total

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


def value_count_plot(df, cat_features, save_plot = False, path_dir = None ):
    
    """
    Plot value count of every categorical features having less than 30 different values. List all categorical features having more than 30. 
    :param df: DataFrame to display data from
    :param cat_features: List of categorical features
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot    
   
    """
    cat_features = list(set(cat_features))    
    if len(cat_features) != []:
        less_than_30 = []
        more_than_30 = []
        for col in cat_features :
            if df[col].nunique() < 30 :
                less_than_30.append(col)
            else :
                more_than_30.append(col)
        if less_than_30 != [] :
            for i, col in sorted(list(enumerate(less_than_30)), key=lambda x: x[1]):
                fig, ax = plt.subplots()
                fig.set_size_inches(4.5,  5.5)
                fig.set_size_inches(4,  4)
                ax = df[col].value_counts().plot(kind='barh')
                ax.set_title(str("Distribution of " + col), fontsize=10)
                plt.show(block=False)
            if save_plot == True:
                plt.savefig((str(path_dir) + "less_than_30_value_count_ordinal.png"))
                plt.clf()
        if more_than_30 != [] :
            print(', '.join(more_than_30), 'have more than 30 different values')
    else:
        print("No categorial features to plot")


def value_count_top(df, cat_features, top = 10, save_plot = False, path_dir = None ):
    """ 
    Plot value count top values of a list of categorical features
    :param df: DataFrame to display data from
    :param cat_features: List of categorical features
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot   
    """
    cat_features = list(set(cat_features))
    cols = cat_features
    if len(cols) != 0:
        for i, col in sorted(list(enumerate(cols)), key=lambda x: x[1]):
            fig, ax = plt.subplots()
            fig.set_size_inches(4.5,  5.5)
            fig.set_size_inches(4,  4)
            ax = df[col].value_counts()[:top].plot(kind='barh')
            plt.title(str("Distribution of TOP " +str(top) +" "+ col), fontsize=10)
            plt.show(block=False)
        if save_plot == True:
            plt.savefig((str(path_dir) + "top_"+str(top)+"_value_count_ordinal.png"))
            plt.clf()
    else:
        print("No categorial features to plot")

        
def value_count_bottom(df, cat_features, bottom = 10, save_plot = False, path_dir = None ):
    """
    Plot value count bottom values of a list of categorical features
    :param df: DataFrame to display data from
    :param cat_features: List of categorical features
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
    """
    cat_features = list(set(cat_features))
    cols = cat_features
    if len(cols) != 0:
        for i, col in sorted(list(enumerate(cols)), key=lambda x: x[1]):
            fig, ax = plt.subplots()
            fig.set_size_inches(4.5,  5.5)
            fig.set_size_inches(4,  4)
            ax = df[col].value_counts()[-bottom:].plot(kind='barh')
            plt.title(str("Distribution of BOTTOM "+str(bottom)+ " " + col), fontsize=10)
            plt.show(block=False)
        if save_plot == True:
            plt.savefig((plot_dir + "bottom_"+str(bottom)+"_value_count_ordinal.png"))
            plt.clf()
    else:
        print("No categorial features to plot")
        
        
def distrib_numerical(df, numerical_feat, percentiles = 0.05, kde = True, save_plot = False, path_dir = None): 
    """
    Plot distribution of numerical features with the gaussian kernel density if there are more than 10 different values
    (previously: distrib_ordinal or distrib_continuous)
    :param df: DataFrame to display data from
    :param numerical_feat: List of Continuous features
    :param percentiles: removes the bottom and top outliers 
    :param kde: if True, plot a gaussian kernel density estimate for the distribution
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
    """
    numerical_feat = list(set(numerical_feat))
    kde_orig = kde
    if len(numerical_feat) != 0:
        p_size = min(2, len(numerical_feat))
        j = int(len(numerical_feat) / 2) + 1
        plt.figure(figsize=(4.5 ** p_size, 4 ** p_size))
        for i, col in enumerate(numerical_feat):
            if percentiles != None:
                good_data = df[df[col].quantile(percentiles) < df[col]] 
                good_data = good_data[good_data[col] < good_data[col].quantile(1-percentiles)]
            else :
                good_data = df
            plt.subplot(j, p_size, i + 1)
            # Check the need for the kde only if it's True
            if (kde_orig):
                if (good_data[~good_data[col].isnull()][col].nunique() <= 10):
                    kde = False
                else:
                    kde = True
                    
            sns.distplot(good_data[~good_data[col].isnull()][col], kde = kde)
            plt.title(str("Distribution of " + col), fontsize=10*p_size)
            plt.xticks(size=8*p_size)
            plt.yticks(size=8*p_size)
            plt.xlabel(col, size=20)
        plt.tight_layout()
        plt.show(block=False)
        if save_plot == True:
            plt.savefig((plot_dir + "Box_plot_continuous_feature.png"))
            plt.clf()
    else:
        print("No Continuous feature to plot")
        
        
def box_plot_continuous(df, cont_feat, percentiles = 0.05, save_plot = False, path_dir = None):   
    """
    Plot box_plot of continuous features
    :param df: DataFrame to display data from
    :param cont_feat: list of continuous features 
    :param percentiles: removes the bottom and top outliers 
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
    """
    cont_feat = list(set(cont_feat))
    if len(cont_feat) != 0:
        p_size = min(2, len(cont_feat))
        j = int(len(cont_feat) / 2) + 1
        plt.figure(figsize=(4.5 ** p_size, 4.5 ** p_size))
        for i, col in enumerate(cont_feat):
            if percentiles != None:
                good_data = df[df[col].quantile(percentiles) < df[col]] 
                good_data = good_data[good_data[col] < good_data[col].quantile(1-percentiles)] 
            else :
                good_data = df
                
            plt.subplot(j, p_size, i + 1)
            good_data[~good_data[col].isnull()][[col]].boxplot(fontsize=10*p_size)
            plt.title(str("Box plot of " + col),fontsize=10*p_size)
            plt.xticks(size=8*p_size)
            plt.yticks(size=8*p_size)
        plt.tight_layout()
        plt.show(block=False)
        if save_plot == True:
            plt.savefig((plot_dir + "Box_plot_continuous_feature .png"))
            plt.clf()
    else:
        print("No Continuous feature to plot")

        
def count_month_year (df, month_col, year_col, save_plot = False, path_dir = None):
    """
    Plot number of raws per month_col and year_col
    :param df: DataFrame to display data from
    :param month_col: month column 
    :param year_col: year column
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
    """
    sns.set(style="white")
    g = sns.catplot(x=month_col, hue=year_col, data=df, kind="count",
                       palette="BuPu", height=6, aspect=1.5)
    plt.show(block=False)
    if save_plot == True:
        plt.savefig((plot_dir + "count_month_year.png"))
        plt.clf()
    sns.set(style="darkgrid") # return to darkgrid style
    

def count_plot_col_per_date(df, date_col, col, num_label = 15, save_plot = False, path_dir = None):
    """
    Count of number of row per date and another column
    :param df: DataFrame to display data from
    :param: date_col: date column we want to sort by 
    :param: col: the column we want to plot
    :param: num_label: we show x labels only every num_label
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
    """
    sns.set(font_scale=1)
    pltdec = df.groupby([date_col, col]).size().unstack()
    fig, axs = plt.subplots();
    plot_ = pltdec.plot.bar(stacked=True, ax=axs , cmap=plt.get_cmap('tab20c'))
    fig.set_size_inches(14, 6);
    plt.suptitle(str('Number of samples per '+ date_col+ ' and '+ col), fontsize=25, fontweight='bold')
    axs.set_ylabel('Number of samples', fontsize=15)
    plt.xlabel('Date',fontsize=15)
    for ind, label in enumerate(plot_.get_xticklabels()):
        if ind % num_label == 0:  # every num_label label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    if save_plot == True:
        plt.savefig((plot_dir + "count_date_"+str(col)+".png"))
        plt.clf()

        
def countplot_cat1(df, cat1, title_suffix = '', perc = False, num_label = 15, save_plot = False, path_dir = None):
    """
    Plot the number of rows per categories in column cat1
    :param df: DataFrame to display data from
    :param cat1: We will show the number of sample for each value in this columns
    :param title_suffix: if we want to add a suffix to the title 
    :param perc: if True, plot percentage of the data instead of the number of sample
    :param num_label: we show x labels only every num_label
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
  
    """
    
    # Count the number of records for each value in category #1
    if perc == True : 
        comp_count = df[cat1].value_counts()/len(df[cat1])
        comp_count = comp_count.nlargest(len(comp_count))
    else : 
        comp_count = df[cat1].value_counts()
        comp_count = comp_count.nlargest(len(comp_count))
    sns.set(font_scale=1.2)
    plt.figure(figsize=(12,5))
    plot = sns.countplot(x=cat1, data=df)
    plt.title('Count the number of different %s values %s' % (cat1, title_suffix));
    plt.xticks(rotation=90)
    for ind, label in enumerate(plot.get_xticklabels()):
        if ind % num_label == 0:  # every num_label label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    plt.show()
    if save_plot == True:
        plt.savefig((plot_dir + "count_of"+str(cat1)+".png"))
        plt.clf()


def density_plot_cat1(df, cat1, bins, kde = False, title_suffix = '', save_plot = False, path_dir = None ):
    """
    Density plot of column cat1 with bins 
    :param df: DataFrame to display data from
    :param cat1: We will show the number of sample for each value in this columns
    :param bins: choose number of bins
    :param kde: Whether to plot a gaussian kernel density estimate for the distribution
    :param title_suffix: if we want to add a suffix to the title 
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot   
    
    """
    # Count the number of records for each value in category #1
    sns.set(font_scale=1.2)
    plt.figure(figsize=(12,5))
    plot = sns.distplot(df[~df[cat1].isnull()][cat1], kde=kde, bins=bins)
    plt.title('Density of %s %s' % (cat1, title_suffix));
    if (df[cat1].dtype == 'O'):
        plt.xticks(rotation=90)
    plt.show()
    if save_plot == True:
        plt.savefig((plot_dir + "count_of"+str(cat1)+".png"))
        plt.clf()
        
        
def num_of_cat2_per_cat1(df, cat1, cat2, figsize=(12,5), normalize = False, num_label = 1, save_plot = False, path_dir = None ):
    """
    Number of different values of column cat2 for every category of column cat1
    :param df: DataFrame to display data from
    :param cat1: we group df by column cat1
    :param cat2: We count the number of different values of column cat2 in every category of column cat1
    :param figsize: we can change the size of the plot 
    :param normalize: Normalize the counts if true 
    :param num_label: we show x labels only every num_label
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot   
    """
    # Group by category #1 and counts the unique values of category #2 for each group
    comp_count = df.groupby(cat1)[cat2].nunique().sort_values(ascending=False)
    if (normalize == True):
        comp_count = comp_count*100.0/(comp_count.sum())
     # Bar plot
    plt.figure(figsize=figsize)
    
    plot = sns.barplot(comp_count.index, comp_count.values, alpha=0.8)
    if (normalize == True):
        plt.ylabel(str('Number of ' + cat2 + ' [%]'), fontsize=12)
        plt.title(str('Percentage of '+ cat2+ ' per '+ cat1))
    else:
        plt.ylabel(str('Number of ' + cat2), fontsize=12)
        plt.title(str('Number of '+ cat2+ ' per '+ cat1))
    plt.xlabel(cat1, fontsize=12)
    plt.xticks(rotation=90)
    for ind, label in enumerate(plot.get_xticklabels()):
        if ind % num_label == 0:  # every 15th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    plt.show()
    if save_plot == True:
        plt.savefig((plot_dir + "count_of"+str(cat1)+"per _"+str(cat2)+".png"))
        plt.clf()

        
def count_of_cat2_per_cat1(df, cat1, cat2, figsize=(10,5), xlim =None, ylim= None, num_label =1, save_plot = False, path_dir = None):
    """
    Count of the Number of different values of column cat2 for every category of column cat1 
    :param df: DataFrame to display data from
    :param cat1: we group df by column cat1
    :param cat2: We show the number of sample for each value in column cat2
    :param figsize: we can change the size of the plot 
    :param xlim: If we want to set a limit on x on the plot
    :param ylim: If we want to set a limit on x on the plot
    :param num_label: we show x labels only every num_label
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot  

    """
    
    # Count of Number of cat2 per cat1 :
    store_count = df.groupby(cat1)[cat2, cat1].nunique()[cat2].value_counts()
    store_count = store_count.nlargest(len(store_count))
    plt.figure(figsize = figsize)
    plot = sns.barplot(store_count.index, store_count.values, alpha=0.8)
    plt.title(str('Count of Number of ' + cat2 + ' per ' +cat1))
    plt.ylabel('Number of occurence', fontsize=12)
    plt.xlabel(str('Number of ' + cat2), fontsize=12)
    for ind, label in enumerate(plot.get_xticklabels()):
        if ind % num_label == 0:  # every 15th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    if ylim != None:
        plot.axes.set_ylim(0, ylim)
    if xlim !=None:
        plot.axes.set_xlim(0, xlim)
    plt.show()
    if save_plot == True:
        plt.savefig((plot_dir + "count_of"+str(cat1)+"per _"+str(cat2)+".png"))
        plt.clf()

        
def count_of_cat3_per_cat1cat2(df, cat1, cat2, cat3, num_label, save_plot = False, path_dir = None ):
    """
    Count of the Number of different values of column cat3 for every category of column cat1 and column cat2 
    :param df: DataFrame to display data from
    :param cat1: we group df by column cat1
    :param cat2 : we group by column cat2
    :param cat3: We show the number of sample for each value in column cat3
    :param num_label: we show x labels only every num_label
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot  
    """
    
    search_term_count = df.groupby([cat1, cat2])[cat1,cat2, cat3].nunique()[cat3].value_counts()
    search_term_count = search_term_count.nlargest(len(search_term_count))
    plt.figure(figsize=(10,5))
    plot = sns.barplot(search_term_count.index, search_term_count.values, alpha=0.8)
    plt.title(str('Count of Number of '+cat3+' per '+cat1+' and per '+ cat2))
    plt.ylabel('Number of occurence', fontsize=12)
    plt.xlabel(str('Number '+ cat3 + ' per '+ cat1+ ' and per ' + cat2), fontsize=12)
    for ind, label in enumerate(plot.get_xticklabels()):
        if ind % num_label == 0:  # every 15th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    plt.show()
    if save_plot == True:
        plt.savefig((plot_dir + "count_of"+str(cat3)+"per _"+str(cat2)+ "and"+str(cat1)+".png"))
        plt.clf()

        
def boxplot_2_features(df, x, y, ylim_i = 0, set_y_limit = False, order_boxplot = False, print_value = False, num_label = 1, save_plot = False, path_dir = None):
    
    """
    Box plot of different categories of column x, for values of y (float)
    :param df: DataFrame to display data from
    :param x: we group df by column x
    :param y : we scatter at the values of y for every category of x
    :param ylim_i: the limite we want to set for y in the plot (if set_y_limit = True)
    :param set_y_limit: True if we don't want to show all the values of y
    :param order_boxplot: True if we want to order the plot by the value count of x
    :param print_value: True if we want to print the value count of x
    :param num_label: we show x labels only every num_label
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot
    """
    
    value_counts_temp = df[x].value_counts()
    sns.set(font_scale=2)
    f, ax = plt.subplots(figsize=(18, 7));
    if order_boxplot :
        plot =sns.boxplot(x=x, y=y, data=df, order = value_counts_temp.index)
    else:
        plot =sns.boxplot(x=x, y=y, data=df) 
    ax.set_title('Boxplot of {} group by {}'.format(y, x));
    plt.xticks(rotation=90);
    if set_y_limit:
        ax.set_ylim(0, ylim_i);
    for ind, label in enumerate(plot.get_xticklabels()):
        if ind % num_label == 0:  # every 15th label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
    if print_value :
        print(value_counts_temp)
    if save_plot == True:
        plt.savefig((plot_dir + "boxplot"+str(y)+"per _"+str(x)+".png"))
        plt.clf()

        
def scatter_2_features(df, x, y, ylim_i = 0, set_y_limit = False, xlim_i = 0, set_x_limit = False, order_boxplot = False, print_value = False, num_label = 1):
    
    """
    Scatter plot of different categories of column x, for values of y (float)
    :param df: DataFrame to display data from
    :param x: we group df by column x
    :param y : we look at the values of y for every category of x
    :param ylim_i: the limite we want to set for y in the plot (if set_y_limit = True)
    :param set_y_limit: True if we don't want to show all the values of y
    :param order_boxplot: True if we want to order the plot by the value count of x
    :param print_value: True if we want to print the value count of x
    :param num_label: we show x labels only every num_label
    """
        
    value_counts_temp = df[x].value_counts()
    f, ax = plt.subplots(figsize=(18, 7));
    plot =plt.scatter(df[x], df[y])
    plt.xticks(rotation=90);
    ax.set_title('Scatter plot of {} group by {}'.format(y, x));
    plt.xlabel(str(x))
    plt.ylabel(str(y))
    if set_y_limit:
        ax.set_ylim(top = ylim_i);
    if set_x_limit:
        ax.set_xlim(right = xlim_i);
    if print_value:
        print(value_counts_temp)

        
def stacked_bar_plot(df, cat1, cat2, bar_size=30, nan_colums_thresh=0, figsize=(20, 10), percentile=0.001, plot_flag = 1, normalize = False, sort_bars = False, return_pivot = False): 
    """
    Stacked Bar Plot Number of samples per cat1 and cat2
    :param df: dataframe we want to see 
    :param cat1: we group df by column cat1
    :param cat2 : we group by column cat2
    :param bar_size: size of the bars
    :param nan_colums_thresh: Drops rows having more than nan_colums_thresh Nan values
    :param figsize: size of the figure
    :param percentile: if we want to hide what over the 100-percentile and under percentile of the data
    :param plot_flag: if == 1, lot the graph 
    :param normalize: if True, plot a Normalize by the sum of the row
    :param sort_bars: sort the search term index in descending order
    :param return_pivot: if True, return the pivot table

    """
    
    df_for_pivot = df[[cat1, cat2]].groupby([cat1, cat2]).size().reset_index(name='counts')
    df_pivot = df_for_pivot.pivot(index=cat1, columns=cat2, values='counts')
    
    if normalize == True:
        df_pivot['sum_cols'] = df_pivot.sum(axis = 1)
        # Normalize by the sum of the row
        df_pivot_percent = df_pivot.div(df_pivot.sum_cols, axis=0)
        # Drop the sum column
        df_pivot_clean = df_pivot_percent.drop(columns=['sum_cols'])
        not_nan_positions_ratio = 100
    else:
        # Drops rows having more than nan_colums_thresh Nan values
        # In case of search_term VS search_position, drops rows with all NaN and only search_position = 11 is not NaN
        df_pivot_clean = df_pivot.dropna(thresh=nan_colums_thresh)
    
        # sort the search term index in descending order
        if sort_bars:
            ordered_index = df_pivot_clean.sum(axis=1).sort_values(ascending=False).index
            df_pivot_clean = df_pivot_clean.reindex(ordered_index)

        # Calculate the ratio of the informative search terms size compared to the overall size of the different search terms
        not_nan_positions_ratio = 100 * df_pivot_clean.shape[0] / (df_pivot.shape[0])
   
    
    if plot_flag == 1:
        # Choose only the top percentile data to avoid data resolution problems
        # df_to_plot = df_pivot_clean[df_pivot_clean.sum(axis = 1) > df_pivot_clean.sum(axis = 1).quantile(percentile)]

        # Choose only the top 30 bars to avoid data resolution problems
        df_to_plot = df_pivot_clean.iloc[0:bar_size, ]

        # Stacked bar plot
        df_to_plot.plot.bar(stacked=True, figsize=figsize, cmap=plt.get_cmap('tab20c'))
        if normalize == True:
            plt.ylabel("Normalized distribution", fontsize=15)
        else:
            plt.suptitle(str('Number of samples per '+ cat1 + ' and '+ cat2), fontsize=20, fontweight='bold')
            plt.ylabel('Number of samples', fontsize=15)
                
    if return_pivot == True :  
        return (df_pivot_clean, not_nan_positions_ratio)
    

def plot_correlations_per_categories(df_plot, cat1, cat2, feature_x, target_y, title_suffix = ''):
    """
    Correlation plot of cat1 with target_y, grouped by cat2
    :param df_plot: dataframe we want to see with the column Correlation of cat1 and cat2
    :param cat1: we group df by column cat1
    :param cat2 : we group by column cat2
    :param feature_x : the feature x 
    :param target_y : the target feature 
    :param title_suffix : if we want to add a suffix to the title 
    """    
    # Plot the correlations
    g = sns.catplot(x=cat1, y='Correlation', hue=cat2, data=df_plot, height = 5, aspect = 3, kind = 'strip')
    plt.title('Correlations of %s per %s %s' % (feature_x, target_y, title_suffix))
    plt.xticks(rotation=90);
    plt.ylim(-1, 1);

    
def na_count(df):
    """
    Tells the shape of the data, calculate the number of Na values per columns in percentages and in number, and classify them from largest to smallest.
    :param df: dataframe we want to see 
    """
    print("Size of the current file is:", df.shape)
    print("")
    printmd("*__Percentage of Na per columns in the data:__*")
    # Calculate the number of the NA values and its precentage
    df_temp = df.isnull().sum().reset_index()
    df_temp.columns = ['column_name', 'na_size']
    df_temp['na_size_percentage'] = round(df_temp.na_size*100.0/df.shape[0], 2)
    df_temp = df_temp.sort_values(by='na_size', ascending=False)
    print(df_temp.loc[df_temp['na_size'] > 0])
    #     print((round(df.isnull().sum()/df.shape[0]*100)))
    print("")
    
    
def get_percentage_missing(series):
    """ 
    Calculates percentage of NaN values in DataFrame
    :param series: Pandas DataFrame object
    :return: float
    """
    num = series.isnull().sum()
    den = len(series)
    return round(num/den*100, 2)
    
    
def percentage_missing_plots(df, perc_missing = 0.1, save_plot = False, path_dir = None):
    """ 
    Plot percentage of NaN values in DataFrame, having more than perc_missing missing values
    :param df: dataframe we want to see     
    :param perc_missing: max percentage of missing value we don't want to show
    :param save_plot: if True save plot to path_dir
    :param path_dir: path directory where you want to save the plot  
    
    """
    
    # Missing value proportion in each column:
    perc = {}
    for col in df.columns:
        perc_col = get_percentage_missing(df[col])
        if perc_col > float(perc_missing*100):
            perc[col] = perc_col
            # perc = dict(sorted(perc.items(), key=lambda x: x[1]))
    if perc != {}:
        perc_df = pd.DataFrame(sorted(list(perc.items()), key=lambda x: x[1]))
#         plt.figure(figsize=(10, 10));
        ax = perc_df.plot(x=0, y=1, kind='barh', legend=False);
        ax.yaxis.tick_left();
        plt.title(str('Percentage of Missing value in the data \n (Having more than ' + str(
            perc_missing * 100) + '% missing values)'), fontsize=15);
        plt.xticks(size=15);
        plt.yticks(size=15);
        plt.ylabel('Features', fontsize=15);
        plt.xlabel('Percentage', fontsize=15);
        plt.show(block=False);
        if save_plot == True:
            plt.savefig(path_dir + "percentage_missing.png")
            plt.clf()
    else:
        print("There are no missing value in the data set")
        

def data_categorical(df, cat_features = [], cont_features = []):
    """
    List all object type columns, print number of unique values for every categorical feature, print 5 unique samples if every Categorical feature
    :param df: dataframe we want to see 
    :param cat_features: Known list of categorical features (can be empty)
    :param cont_features: Known list of continuous features (can be empty)
    :return cat_features: the list of categorical features
    """
    subset_cat = []
    subset_dict={}
    # Add all the object type features to config.cat_features 
    for col in df.columns:
        if df[col].dtype == 'object' and col not in cont_features:
            subset_cat.append(col)
            if col not in cat_features :
                cat_features.append(col)
    if cat_features !=[]:
        print('Categorical features : ', ' '.join(cat_features))
        printmd('**Number of unique values for every feature:**')
        print(pd.DataFrame(df[cat_features].nunique(), columns = ['Unique values']).sort_values(by = 'Unique values', ascending=False))
        printmd("**5 uniques samples of every Categorical Features :**")
        for col in cat_features :
            subset_dict[col]= df[col].unique()[:5]
        print(pd.DataFrame.from_dict(subset_dict, orient='index').transpose())
    return (cat_features)
        
        
def data_continuous(df, cat_features = [], cont_features = []) :
    """
    Return a list of int or float type columns, convert all columns of cont_features to numericPrint the description of all continuous features
    :param df: dataframe we want to see 
    :param cat_features: Known list of categorical features (can be empty)
    :param cont_features: Known list of continuous features (can be empty)
    :return cont_features: the list of categorical features
    """
    subset_cont =[]
    for col in list(df.columns):
        if df[col].dtype == 'int' or df[col].dtype == 'float64':
            if col not in cont_features and col not in cat_features:
                print(col, "was added to continuous features")
                cont_features.append(col)
                subset_cont.append(col)
    for col in cont_features:
        if col not in subset_cont:
            subset_cont.append(col)
    print('Continuous features : ', ' '.join(subset_cont))
    printmd("**Description of continuous columns:**")
    print(round(df[subset_cont].describe()))
    return (cont_features)


def data_all_types(df):
    
    """
    Print the type of every columns in the data.   
    :param df: dataframe we want to see 
    """
    
    printmd ("**Type of every column in the data**")
    print("")
    print(df.dtypes)
    
    
def zero_one_card(df):
    """
    Show 1 or 0 cardinality columns 
    :param : df : The dataframe
    """
    unique_values = defaultdict()
    for col in df.columns:
        if df[col].nunique() < 2:
            unique_values[col] = df[col].nunique()
    if len(unique_values) > 0:
        printmd(str("* Columns: *"+', '.join(list(unique_values.keys()))+"* have less than two different values"))
        for col in unique_values.keys():
            printmd(str('*   *' + col + "* has " + str(df[col].nunique()) + ' differents values :' + str(df[col].unique())))
    else:
        printmd("* No columns have less than 2 different values")
        

def same_num_of_unique_val(df):
    """
    Show columns having same values_counts, and print a dataframes of the value_counts of both columns and their respectives values.
    :param : df : The Dataframe
    """
    value_count =dict()
    for col in df.columns:
        value_count[col] = list(df[col].value_counts())
    similar_columns = [i for i in combinations(df.columns,2) if (value_count[i[0]]==value_count[i[1]] and i[0] != i[1])]
    if similar_columns != []:
        for (col1, col2) in similar_columns :
            printmd(str("* *" + str(col1) +"* and *"+ str(col2)+ "* have same number of values "))
            a = pd.DataFrame(df[col1].value_counts()).reset_index()
            a.columns = [str('values_'+col1), 'count']
            b = pd.DataFrame(df[col2].value_counts()).reset_index()
            b.columns = [str('values_'+col2), 'count']
            to_display = a.merge(b, on = 'count')
            display(to_display[['count', str('values_'+col1), str('values_'+col2)]])

    else :
        printmd("* No columns have same number of unique values")
        
        
def show_data(df):
    """
    Print the number of rows of the data loaded and shows the first five rows.
    :param : df : The dataframe
    
    """
    printmd(str("The Data contains **" + str(df.shape[0])+ '** rows.'))
    printmd("*__Sample of the data :__*")
    display(df.head(n=5))
    print("")
    print("")


def display_group_density_plot(df, groupby, on, palette, figsize):
    """
    Displays a density plot by group, given a continuous variable, and a group to split the data by
    :param df: DataFrame to display data from
    :param groupby: Column name by which plots would be grouped (Categorical, maximum 10 categories)
    :param on: Column name of the different density plots
    :param palette: Color palette to use for drawing
    :param figsize: Figure size
    :return: matplotlib.axes._subplots.AxesSubplot object
    """

    if not isinstance(df, pd.core.frame.DataFrame):
        raise ValueError('df must be a pandas DataFrame')

    if not groupby:
        raise ValueError('groupby parameter must be provided')

    elif not groupby in df.keys():
        raise ValueError(groupby + ' column does not exist in the given DataFrame')

    if not on:
        raise ValueError('on parameter must be provided')

    elif not on in df.keys():
        raise ValueError(on + ' column does not exist in the given DataFrame')

    if len(set(df[groupby])) > 10:
        groups = df[groupby].value_counts().index[:10]

    else:
        groups = set(df[groupby])

    # Get relevant palette
    if palette:
        palette = palette[:len(groups)]
    else:
        palette = sns.color_palette()[:len(groups)]

    # Plot
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')

    for value, color in zip(groups, palette):
        sns.kdeplot(df.loc[df[groupby] == value][on], shade=True, color=color, label=value)

    ax.set_title(str("Distribution of " + on + " per " + groupby + " group"), fontsize=10)
    return ax