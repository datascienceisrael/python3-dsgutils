import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def display_corr_matrix(dataframe, on_columns, ax=None, cmap=None, **heatmap_kwargs):
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
        'vmax': 0.3,
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