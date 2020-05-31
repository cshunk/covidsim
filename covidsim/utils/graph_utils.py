import matplotlib
import numpy as np

from dataclasses import dataclass

from covidsim.datastructures import SeriesRange

@dataclass
class ColorSet:
    dark_color: str
    light_color: str


@dataclass
class ColorSchemes:
    blue: ColorSet = ColorSet('navy', 'lavender')
    red: ColorSet = ColorSet('tab:red', 'wheat')
    green: ColorSet = ColorSet('darkgreen', 'mintcream')


def plot_series_range(data: SeriesRange, plt, ax, label, color: ColorSet):
    x = np.arange(0,len(data.mean), 1)
    plt.plot(data.high, color=color.light_color, alpha=0.5)
    plt.plot(data.low, color=color.light_color, alpha=0.5)

    ax.fill_between(x, data.high, data.low, color=color.light_color, alpha=0.5)

    plt.plot(data.mean, color=color.dark_color)

    if label is not None:
        ax.set_ylabel(label, color=color.dark_color, fontsize=14)
    else:
        ax.set_visible(False)

