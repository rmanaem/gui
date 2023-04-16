"""Utility functions and constants of the app."""
import json
import os

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html

COLORS = [
    px.colors.qualitative.G10,
    px.colors.sequential.Teal,
    px.colors.sequential.Brwnyl,
    px.colors.sequential.Burg,
    px.colors.sequential.Purp,
]


def pull_files(path):
    """
    Creates a list of paths for .json files in the input path.

    Parameters
    ----------
    path : str
        Path of the directory containing .json files to be visualized.

    Returns
    -------
    list
        List of paths.
    """
    files = []
    for i in os.listdir(path):
        if i[-5:] == ".json":
            files.append((path + "/" + i, i[: len(i) - 5]))
    return files


def process_file(file, color):
    """
    Creates a dataframe from input file's data.
    Loads the data from the file into a dataframe and adds
    Result, Metadata, and Color (using a single color sequence
    from COLORS per file) columns to the dataframe using
    the data.

    Parameters
    ----------
    file : tuple
        (dataset-pipeline file path, dataset-pipeline name).
    color : int
        Index number for selecting a color sequence from COLORS.

    Returns
    -------
    pandas.core.frame.DataFrame
        A dataframe containing Subject, Dataset-Pipeline, Result
        Metadata, and Color columns.
    """
    data = None
    with open(file[0], "r") as dataset:
        data = json.load(dataset)
    x = []
    for k in data.keys():
        z = len(COLORS[color]) - 1
        for v in data[k].keys():
            x.append(
                (k, v, data[k][v]["Result"]["result"], data[k][v], COLORS[color][z])
            )
            z -= 1
    x = [
        (i[0], i[1], -1, i[3], i[4])
        if i[2] is None
        else (i[0], i[1], float(i[2]), i[3], i[4])
        for i in x
    ]
    df = pd.DataFrame(
        {
            "Subject": [i[0] for i in x],
            "Dataset-Pipeline": [file[1] + "-" + i[1] for i in x],
            "Result": [i[2] for i in x],
            "Metadata": [i[3] for i in x],
            "Color": [i[4] for i in x],
        }
    )
    return df


def process_files(path):
    files = pull_files(path)
    dfs = []
    for i, j in enumerate(files):
        dfs.append(process_file(j, i))
    return pd.concat(dfs)


def pull_directories(path):
    files = []
    for directory in os.listdir(path):
        files.append((directory, pull_files(os.path.join(path, directory)), []))
    for i in files:
        for z, w in enumerate(i[1]):
            i[2].append(process_file(w, z))
    return [(i[0], pd.concat(i[2])) for i in files]


def generate_summary(df):
    total = str(df.shape[0])
    missing = str(df[df["Result"] == -1].shape[0])
    header = html.H4("Summary", className="card-title")
    summary = [
        header,
        "Total number of datapoints: " + total,
        html.Br(),
        "Total number of missing datapoints: " + missing,
        html.Br(),
    ]
    pipelines = df["Dataset-Pipeline"].unique().tolist()
    for p in pipelines:
        s = (
            p
            + ": "
            + str(df[(df["Dataset-Pipeline"] == p) & (df["Result"] == -1)].shape[0])
        )
        summary.append(s)
        summary.append(html.Br())

    return dbc.Card(dbc.CardBody(summary, className="card-text"))
