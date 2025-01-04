import os.path

from matplotlib import pyplot as plt
import seaborn as sns


def save_plots(df, res_dir):
    plt.figure(figsize=(6, 8))
    df_plot = df.drop(columns=["name", "TP", "FP", "FN"])
    colors = ['#FF6347', '#8A2BE2', '#00FA9A', '#FF4500', '#2E8B57',
              '#FFD700', '#D2691E', '#6495ED', '#DC143C']
    for i, column in enumerate(df_plot.columns, start=1):
        plt.subplot(3, 3, i)
        sns.violinplot(data=df_plot, y=column, orient="v", color=colors[i - 1])
        plt.title(f'{column}')
        plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(res_dir, "violin_plots_divided.png"), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(8, 6))
    sns.violinplot(data=df_plot, palette=colors)
    plt.tight_layout()
    plt.savefig(os.path.join(res_dir, "violin_plots.png"), dpi=300, bbox_inches='tight')
