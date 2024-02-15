# -*- coding: utf-8 -*-
"""
File: plutchik_viz.py
Modifier for Cluster: Su Karaca
Author: Maxine Xu
Description: This script creates three types of visualizations for
novel-level analysis: a visualization with eight bar graphs that
tracks the probabilities for each of the emotion labels throughout
a novel, a bar graph of the probabilities over a threshold of 0.5 for the
designated majority emotion label, and a pie  chart, which
displays the distribution of the majority emotion labels.
"""

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


def generate_output_folders(output_folder_base):
    all_emotion_output_folder = os.path.join(
        output_folder_base, "8-class all emotions viz/"
    )
    piechart_output_folder = os.path.join(
        output_folder_base, "8-class pie chart viz/"
    )
    thresh_output_folder = os.path.join(
        output_folder_base, "8-class threshold viz/"
    )

    output_folders = [
        all_emotion_output_folder,
        piechart_output_folder,
        thresh_output_folder,
    ]

    for folder in output_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    return (
        all_emotion_output_folder,
        piechart_output_folder,
        thresh_output_folder,
    )


def main(data_folder_path, output_folder_base):
    file_names = os.listdir(data_folder_path)
    file_names = [string for string in file_names if "csv" in string]

    dataframes = {}

    for file in file_names:
        file_path = os.path.join(data_folder_path, file)
        df_name = os.path.splitext(file)[0]
        dataframes[df_name] = pd.read_csv(file_path)

    (
        all_emotion_output_folder,
        piechart_output_folder,
        thresh_output_folder,
    ) = generate_output_folders(output_folder_base)

    all_emotion_colors = [
        "gold",
        "saddlebrown",
        "darkviolet",
        "darkorange",
        "mediumblue",
        "darkgreen",
        "crimson",
        "pink",
    ]

    pie_chart_colors = [
        "darkviolet",
        "mediumblue",
        "gold",
        "saddlebrown",
        "darkorange",
        "pink",
        "crimson",
        "darkgreen",
    ]

    thresh_colors = [
        "crimson",
        "pink",
        "darkgreen",
        "darkviolet",
        "gold",
        "mediumblue",
        "darkorange",
        "saddlebrown",
    ]

    for k, df in dataframes.items():
        df.rename(columns={"Unnamed: 0": "paragraph index"}, inplace=True)

        # Plotting 8 bar graphs for each novel
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(16, 24))

        for i, column in enumerate(df.columns[-8:]):
            row, col = i // 2, i % 2
            ax = axes[row, col]
            ax.bar(df.index, df[column], color=all_emotion_colors[i])
            ax.set_xlabel("Paragraph Index")
            ax.set_ylabel("Probability")
            ax.set_title(column)
            ax.set_ylim(0, 1)

        fig.suptitle(f"{k} Plutchik Emotion Probabilities")
        plt.tight_layout()
        plt.savefig(
            os.path.join(all_emotion_output_folder, f"{k}_allemotions.png")
        )
        plt.close()

        # Generating a pie chart of the counts of
        # labelled emotions for every novel
        value_counts = df["8-class label"].value_counts()
        plt.figure(figsize=(10, 10))
        plt.pie(
            value_counts,
            labels=value_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=pie_chart_colors,
            textprops={"fontsize": 10},
        )
        plt.axis("equal")
        plt.title(f"Distribution of Plutchik Emotions in {k}", fontsize=12)
        plt.savefig(os.path.join(piechart_output_folder, f"{k}_piechart.png"))
        plt.close()

        # Plotting a bar graph of the labelled emotions
        # with a threshold of 0.5 for every novel
        df_filtered = df[df["8-class prob"] >= 0.5]
        grouped = df_filtered.groupby("8-class label")
        fig, ax = plt.subplots(figsize=(15, 9))

        for i, (label, group) in enumerate(grouped):
            ax.bar(
                group["paragraph index"],
                group["8-class prob"],
                color=thresh_colors[i],
                label=label,
            )

        ax.set_xlabel("Paragraph Index")
        ax.set_ylabel("Emotion Probability")
        ax.set_title(f"{k} Plutchik Emotion Probability Throughout the Novel")
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
        ax.set_ylim(0.5, 1)

        plt.savefig(
            os.path.join(thresh_output_folder, f"{k}_thresh.png"),
            bbox_inches="tight",
        )
        plt.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python your_script.py <data_folder_path> <output_folder_base>"
        )
        sys.exit(1)

    data_folder_path = sys.argv[1]
    output_folder_base = sys.argv[2]

    main(data_folder_path, output_folder_base)
