# -*- coding: utf-8 -*-
"""
File: sentiment_analysis.py
Modifier for Cluster: Su Karaca
Author: Maxine Xu
Description: This script applies the Bert model
to the files in the clusterdata
folder and finds the 8-class emotion label and
probability for the paragraphs
within each file. The output files are then saved
to the 8-class paragraph data folder.
"""

import os
import sys

import pandas as pd
import torch
from transformers import BertTokenizer

from utils.bert_functions import SentimentClassifier, create_data_loader

# Remove unused import
# from utils.bert_functions import eval_model


def main(data_folder_path, model_path, output_path):
    # replace with path to 'best_model_state.bin' file
    file_names = os.listdir(data_folder_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Checking to see if output folder exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # creating a dictionary where the keys are the shortened book names and
    # the values are their dataframes
    dataframes = {}

    for file in file_names:
        file_path = os.path.join(data_folder_path, file)
        df_name = os.path.splitext(file)[0]
        dataframes[df_name] = pd.read_csv(file_path)

    # load in model
    model = SentimentClassifier(8)
    model.load_state_dict(torch.load(model_path))
    model = model.to(device)

    # applying fine-tuned model
    tokenizer = BertTokenizer.from_pretrained(
        "Yuetian/bert-base-uncased-finetuned-plutchik-emotion"
    )

    def encode_text(x):
        return tokenizer.encode(x, max_length=512)

    # renaming columns for uniformity and tokenizing text
    for k, v in dataframes.items():
        if "paragraph" in v.columns:
            v.rename(columns={"paragraph": "text"}, inplace=True)
        v["tokens"] = v["text"].apply(encode_text)

    # looping through each text dataframe and
    # applying the model to find the 8-class
    # label and probability.
    for df_name, df in dataframes.items():
        data_loader = create_data_loader(df, tokenizer, 512)
        # Removed unused eval_model function
        prob_df = SentimentClassifier.predict(model, data_loader, len(df))
        # writing the new dataframe with label and probability to csv file
        path = f"{output_path}/{df_name[:-11]}.csv"
        with open(path, "w", encoding="utf-8-sig") as f:
            prob_df.to_csv(f)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python your_script.py "
            "<data_folder_path> <model_path> <output_path>"
        )
        sys.exit(1)

    data_folder_path = sys.argv[1]
    model_path = sys.argv[2]
    output_path = sys.argv[3]

    main(data_folder_path, model_path, output_path)
