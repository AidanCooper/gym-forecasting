"""Functions for plotting data
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import src.exceptions as e
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from scipy import stats


def plot_24h(
    df,
    c: str = "red",
    ax=None,
    ylim: float = None,
    datetime_col: str = "time",
    mode: str = "interval",
    conf_interval: float = 0.95,
    alpha: float = 0.1,
) -> plt.figure:
    """
    Plot average 24h trend for provided DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame for which to plot 24h trend. Filtering should be applied beforehand
        (e.g. for day of week of interest, date range etc.)
    c : str
        Colour to use for plotted capacity data.
    ax
        Optionally specify a matplotlib axis to plot to; otherwise, one is created.
    ylim : float
        Optionally specify upper limit for y-axis; otherwise, automatically fit y
        axis to plotted data. Expressed as percentage (maximum 100.0).
    datetime_col : str
        Name of column containing datetime information.
    mode : str
        'interval' for plot of mean capacity with confidence interval.
        'spaghetti' for spaghetti plot of each individual date in DataFrame.
    conf_interval : float
        Confidence interval to use if `mode` == 'interval', expressed as decimal
        percentage. Otherwise, ignored.
    alpha : float
        alpha value to use for confidence interval in interval plots, and lines in
        spaghetti plots

    Returns
    -------
    plt.figure
        Plotted 24h gym capacity data.
    """
    # checks
    if datetime_col not in df.columns:
        raise e.ColumnNotFoundException(datetime_col)
    if not is_datetime(df[datetime_col]):
        raise e.ColumnNotDatetimeException(datetime_col)
    if ylim and (ylim < 0 or ylim > 100):
        raise e.LimitException(ylim)
    if conf_interval <= 0 or conf_interval >= 1:
        raise e.ConfidenceIntervalException(conf_interval)

    if ax:
        fig = None
    else:
        fig, ax = plt.subplots(figsize=(12, 6))

    dfp = df.copy()
    if mode == "interval":
        dfp["hours"] = [val.time() for val in dfp[datetime_col]]
        dfp = dfp.groupby("hours")["capacity"].agg(["mean", "std", "sem"]).reset_index()
        dfp["hours"] = dfp["hours"].apply(lambda x: x.hour + x.minute / 60)
        bound = (1 - conf_interval) / 2 + conf_interval  # for stats.norm.ppf
        dfp["lower"] = dfp["mean"] - stats.norm.ppf(bound) * dfp["std"]
        dfp["upper"] = dfp["mean"] + stats.norm.ppf(bound) * dfp["std"]

        # plot
        ax.fill_between(
            dfp["hours"],
            dfp["lower"],
            dfp["upper"],
            color=c,
            alpha=alpha,
            label=f"{conf_interval*100}% confidence interval",
        )
        ax.plot(
            dfp["hours"],
            dfp["mean"],
            c=c,
            linestyle="--",
            label=f"Mean capacity",
        )
        ax.legend(frameon=True)
    elif mode == "spaghetti":
        for date in dfp[datetime_col].dt.date.unique():
            dfpd = dfp[dfp[datetime_col].dt.date == date].copy()
            dfpd["hours"] = [val.time() for val in dfpd[datetime_col]]
            dfpd["hours"] = dfpd["hours"].apply(lambda x: x.hour + x.minute / 60)
            ax.plot(
                dfpd["hours"],
                dfpd["capacity"],
                c=c,
                linestyle="-",
                alpha=0.2,
            )
    else:
        print("`mode` must be 'interval' or 'spaghetti'.")
        return

    if not ylim:
        ylim = ax.get_ylim()[1]
    ax.set_ylim(0, min(100, ylim))

    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02}:00" for h in range(0, 24, 2)], rotation=15)
    ax.set_xlim(0, 24)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=False))
    ax.grid()
    ax.set_xlabel("Time of Day")
    ax.spines[:].set_visible(True)

    plt.close()

    if fig:
        return fig
    else:
        return ax
