from math import ceil
from typing import List

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

method_to_short = {'EFV3_IONISING_RADIATION': "Ionising rad.",
                   'EFV3_PARTICULATE_MATTER_FORMATION': "Part. matter",
                   'EFV3_CLIMATE_CHANGE': "Climate change",
                   'EFV3_ACIDIFICATION': "Acidification"}

method_to_unit = {"EFV3_IONISING_RADIATION": "kBq U235",
                  "EFV3_PARTICULATE_MATTER_FORMATION": "Disease inc.",
                  "EFV3_CLIMATE_CHANGE": "kg CO2eq",
                  "EFV3_ACIDIFICATION": "mol H+eq"}

short_to_unit = {method_to_short[method]: method_to_unit[method] for method in
                 method_to_short.keys()}

matplotlib.rcParams.update({'font.size': 6})

colors = ['#852D25', '#c74438', '#E9B5B0', '#0093A7', "#1E1E1E", "#3E4A83", "#FFCD31",
          "#A72587", "#BD987A"]

# Create legend in fig rather than an axis
def add_fig_legend(fig, labels, colors, loc='lower center'):
    # Get colours for current style
    # Set up handles (the bits that are drawn in the legend)
    handles = []
    for group_idx in range(len(labels)):
        # Create a simple patch that is the correct colour
        colour = colors[group_idx]
        handles.append(Patch(edgecolor=colour, facecolor=colour, fill=True))
    # Acutally create our figure legend, using the handles and labels
    fig.legend(handles=handles, labels=labels, loc=loc, ncol=len(labels))

def multicriteria_bar_plot(scores: List, names: List[str],
                           names_to_remove, colors=None, show=False):
    tables = []
    for i in range(len(scores)):
        table = pd.concat(
            score.to_unpivoted_df() for score in scores[i] if
            score.name not in names_to_remove)
        table["design"] = names[i]
        tables.append(table)
    table = pd.concat(tables)
    table["method"] = table["method"].replace(method_to_short)
    methods = pd.unique(table["method"])
    methods.sort()
    fig, axes = plt.subplots(1, methods.size, sharex=True)
    for i, method in enumerate(methods):
        unit = short_to_unit[method]
        method_table = table[table["method"] == method]
        method_table = method_table.pivot(index="design", columns="name", values="score")
        method_table = method_table.reindex(names)
        method_table.plot(kind='bar', stacked=True, ax=axes[i], color=colors)
        axes[i].set_title(method, fontsize=5)
        axes[i].set_ylabel(unit)
        axes[i].set_xlabel('')
        axes[i].ticklabel_format(axis='y', style='sci', scilimits=[-2,3])
        #axes[i].get_xaxis().set_visible(False)
        legend_texts = [text.get_text() for text in axes[i].get_legend().texts]
        axes[i].legend_.remove()
        axes[i].tick_params(axis='x', labelrotation=40)
    fig.tight_layout()
    fig.set_size_inches(6, 2.25)
    plt.subplots_adjust(bottom=0.36, top=0.9, left=0.07)
    add_fig_legend(fig, legend_texts, colors)
    fig.patch.set_facecolor('white')
    if show:
        plt.show()
    return fig

#two_yaxis_line_plot(pd.DataFrame(env_scores), "lifetime (year)",
#                          f"{impact_short_name} ({impact_unit})", "CIS",
#                          f"{impact_short_name} ({impact_unit})", colors[0],
#                          None, pd.DataFrame(perf_cost_scores), "lifetime (year)",
#                          "Cost per suppl. Mpixel", None,
#                          f"Cost of performance ({impact_unit}/{PERF_UNIT})", colors[3],
#                          's', show=True)

def two_yaxis_line_plot(df1, x1, y1, hue1, color1, marker1, df2, x2, y2, hue2,
                        color2, marker2, perf_unit, vlines, show=False):
    sns.set_style("whitegrid")
    impact_names = pd.unique(df1["method"])
    fig, ax1 = plt.subplots(2, ceil(len(impact_names) / 2), sharex=True)

    for i in range(len(impact_names)):
        impact_name = impact_names[i]
        impact_short_name = method_to_short[impact_name]
        impact_unit = short_to_unit[impact_short_name]
        df1_impact = df1[df1["method"] == impact_name]
        df2_impact = df2[df2["method"] == impact_name]
        # Plot the primary y-axis data
        sns.lineplot(data=df1_impact, x=x1, y=y1, ax=ax1[i//2, i%2], style=hue1, color=color1, marker=marker1)

        # Create the secondary y-axis
        sns.set_style("white")
        ax2 = ax1[i//2, i%2].twinx()
        sns.lineplot(data=df2_impact, x=x2, y=y2, ax=ax2, style=hue2, color=color2, marker=marker2, label="ECP")
        ax1[i//2, i%2].set_ylabel(f"{impact_short_name} ({impact_unit})", color=color1)
        ax2.set_ylabel(f"{impact_unit}/{perf_unit}", color=color2)
        ax1[i//2, i%2].set(xlim=(df1_impact[x1].min(), df1_impact[x1].max()))
        ax1[i//2, i%2].set(ylim=(0, df1_impact[y1].max()))
        #ax2.yaxis.set_ticks(np.arange(0, 0.15, 0.025))
        ax2.set(ylim=(0, df2_impact[y2].max()))

        ax1[i // 2, i % 2].legend(loc=(0.2, 0.79))
        ax2.legend(loc=(0.6, 0.9))

        # Vertical lines
        for _, vline in vlines.iterrows():
            ax1[i // 2, i % 2].axvline(x=vline["x"],
                                       ymin=0, ymax=1,
                                       label=vline["name"],
                                       linestyle=":",
                                       color="#3E4A83")

            #if i // 2 == ceil(len(impact_names) / 2) - 1:
            plt.text(vline["x"], 0, " " + vline["name"], fontsize=6)

    #plt.subplots_adjust(bottom=0.15, top=0.95, left=0.08, right=0.9)
    fig.tight_layout()
    fig.set_size_inches(6.5, 4.3)
    if show:
        plt.show()
    return fig

def relative_bar_plot(df, x, y, hue, show=False):
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(1, 1)

    df_local = df.replace(method_to_short)
    sorter = df.groupby(hue)["score"].sum().sort_values().index.to_list()
    #df_local[hue] = df_local[hue].astype("category")
    #df_local[hue] = df_local[hue].cat.set_categories(sorter)
    #df_local = df_local.sort_values([hue])
    df_local = df_local.sort_values(x)
    g = sns.histplot(df_local, x=x, hue=hue, weights=y, multiple='stack',
                     palette=sns.color_palette(colors, len(colors)),
                     hue_order=sorter)
    sns.despine(left=True)
    ax.set(ylim=(0, 1))
    ax.set_xlabel("Impact method")
    ax.set_ylabel("Relative impact")
    g.legend_.set_title(None)
    fig.set_size_inches(3, 2.55)
    plt.subplots_adjust(bottom=0.12)
    if show:
        plt.show()
    return fig

def heatmap_multicriteria(df, impact_method_names, row_name, col_name, score_suffix, row_order=None, col_order=None, show=False):
    fig, axs = plt.subplots(ncols=len(impact_method_names) + 1, gridspec_kw=dict(
        width_ratios=[0.9 / len(impact_method_names) for _ in
                      range(len(impact_method_names))] + [0.1]))
    all_values = df[[f"{impact_method_name}_{score_suffix}" for impact_method_name in
                     impact_method_names]]
    vmin = all_values.min(axis=None)
    vmax = all_values.max(axis=None)
    for i in range(len(impact_method_names)):
        data = df.pivot(index=row_name, columns=col_name,
                        values=f"{impact_method_names[i]}_{score_suffix}")
        if row_order is not None:
            data = data.reindex(index=row_order)
        if col_order:
            data = data[col_order]
        sns.heatmap(data, annot=True, cbar=False, ax=axs[i], vmin=vmin, vmax=vmax,
                    cmap=sns.cubehelix_palette(as_cmap=True), fmt='.3g',
                    yticklabels=True if i == 0 else False)
        axs[i].set_title(
            f"{method_to_short[impact_method_names[i]]} ({method_to_unit[impact_method_names[i]]})")
        for t in axs[i].texts: t.set_text("± " + t.get_text() + " %")
        if i != 0:
            axs[i].set(ylabel="")
    fig.colorbar(axs[0].collections[0], cax=axs[len(impact_method_names)])
    axs[len(impact_method_names)].set(ylabel="absolute relative difference (%)")
    axs[0].tick_params(axis='y', rotation=0)
    plt.tight_layout()
    fig.set_size_inches(6, 2)
    plt.subplots_adjust(top=0.9)
    if show:
        plt.show()
    return fig
