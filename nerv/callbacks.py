"""
Logic of app callback functions.
"""
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html

# def switch_template_func(value, histogram_fig, scatter_fig, template1, template2):
#     template = template1 if value else template2
#     histogram_fig["layout"]["template"] = pio.templates[template]
#     scatter_fig["layout"]["template"] = pio.templates[template]

#     return histogram_fig, scatter_fig


def histogram_click_func(clickData):
    """
    Processes data from the histogram graph click event.

    Parameters
    ----------
    clickData : dict
        Data from latest histogram graph click event.

    Returns
    ----------
    dash._callback.Noupdate or dash_bootstrap_components._components.Card.Card
        No dash update if clickData is None otherwise, styled and structured
        metadata to be displayed in hist-metadata-div.
    """
    if not clickData:
        return dash.no_update
    subject = "Subject: " + clickData["points"][0]["customdata"][0]
    pipeline = "Dataset-Pipeline: " + clickData["points"][0]["y"]
    result = (
        "Result: N/A"
        if clickData["points"][0]["x"] == -1
        else "Result: " + str(clickData["points"][0]["x"])
    )
    header = html.H4("Metadata", className="card-title")
    metadata = [
        header,
        subject,
        html.Br(),
        pipeline,
        html.Br(),
        result,
        html.Br(),
        "Pipeline steps:",
        html.Br(),
        html.Br(),
    ]

    for k, v in list(clickData["points"][0]["customdata"][2].items())[:-1]:
        status = "Incomplete" if v["status"] is None else v["status"]
        inp = (
            "N/A"
            if v["inputID"] is None
            else html.A(
                str(v["inputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["inputID"]),
            )
        )
        out = (
            "N/A"
            if v["outputID"] is None
            else html.A(
                str(v["outputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["outputID"]),
            )
        )
        task = (
            "N/A"
            if v["taskID"] is None
            else html.A(
                str(v["taskID"]),
                href="https://portal.cbrain.mcgill.ca/tasks/inser_ID_here"
                + str(v["taskID"]),
            )
        )
        config = "N/A" if v["toolConfigID"] is None else str(v["toolConfigID"])
        step = dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        "Status: ",
                        status,
                        html.Br(),
                        "Input ID: ",
                        inp,
                        html.Br(),
                        "Output ID: ",
                        out,
                        html.Br(),
                        "Task ID: ",
                        task,
                        html.Br(),
                        "Tool Configuration ID: ",
                        config,
                    ],
                    title=k,
                ),
            ],
            start_collapsed=True,
        )
        metadata.append(step)

    return dbc.Card(dbc.CardBody(metadata, className="card-text"))


def plot_scatter_func(x, y, df):
    """
    Creates a scatter plot figure.
    If x or y is None, it uses the first and last dataset-pipeline
    in the dataframe as x and y.

    Parameters
    ----------
        x : str
            Name of the x-axis dataset-pipeline.
        y : str
            Name of the y-axis dataset-pipeline.

    Returns
    ----------
    plotly.graph_objs._figure.Figure
        A plotly graph figure object for the scatter plot
        where x and y inputs are the axes.
    """
    if not x or not y:
        return px.scatter(
            df,
            x=df[df["Dataset-Pipeline"] == df["Dataset-Pipeline"].unique().tolist()[0]][
                "Result"
            ],
            y=df[
                df["Dataset-Pipeline"] == df["Dataset-Pipeline"].unique().tolist()[-1]
            ]["Result"],
            marginal_x="histogram",
            marginal_y="histogram",
            color_discrete_sequence=px.colors.qualitative.G10[::-1],
        ).update_layout(
            xaxis={"rangeslider": {"visible": True}},
            xaxis_title=df["Dataset-Pipeline"].unique().tolist()[0],
            yaxis_title=df["Dataset-Pipeline"].unique().tolist()[-1],
        )
    else:
        return px.scatter(
            df,
            x=df[df["Dataset-Pipeline"] == x]["Result"],
            y=df[df["Dataset-Pipeline"] == y]["Result"],
            marginal_x="histogram",
            marginal_y="histogram",
            color_discrete_sequence=px.colors.qualitative.G10[::-1],
        ).update_layout(
            xaxis={"rangeslider": {"visible": True}}, xaxis_title=x, yaxis_title=y
        )


def scatter_click_func(clickData, x, y, df):
    """
    Processes data from the scatter plot graph click event.
    If x or y is None, it uses the first and last dataset-pipeline
    in the dataframe as x and y.

    Parameters
    ----------
    clickData : dict
        Data from latest histogram graph click event.
    x : str
        Name of the x-axis dataset-pipeline.
    y : str
        Name of the y-axis dataset-pipeline.

    Returns
    ----------
    dash._callback.Noupdate or dash_bootstrap_components._components.Card.Card
        No dash update if clickData is None otherwise, styled and structured
        metadata to be displayed in scatter-metadata-div.
    """
    if not clickData:
        return dash.no_update

    if not x or not y:
        xys = df["Dataset-Pipeline"].unique().tolist()
        x, y = xys[0], xys[-1]

    header = html.H4("Metadata", className="card-title")
    x_subject = (
        "Subject: "
        + df[
            (df["Dataset-Pipeline"] == x)
            & (df["Result"] == clickData["points"][0]["x"])
        ]["Subject"].iloc[0]
    )
    x_pipeline = "Dataset-Pipeline: " + x
    x_result = (
        "Result: N/A"
        if clickData["points"][0]["x"] == -1
        else "Result: " + str(clickData["points"][0]["x"])
    )
    metadata = [
        header,
        x_subject,
        html.Br(),
        x_pipeline,
        html.Br(),
        x_result,
        html.Br(),
        "Pipeline steps:",
        html.Br(),
        html.Br(),
    ]
    x_metadata = df[
        (df["Dataset-Pipeline"] == x) & (df["Result"] == clickData["points"][0]["x"])
    ]["Metadata"].iloc[0]
    for k, v in list(x_metadata.items())[:-1]:
        status = "Incomplete" if v["status"] is None else v["status"]
        inp = (
            "N/A"
            if v["inputID"] is None
            else html.A(
                str(v["inputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["inputID"]),
            )
        )
        out = (
            "N/A"
            if v["outputID"] is None
            else html.A(
                str(v["outputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["outputID"]),
            )
        )
        task = (
            "N/A"
            if v["taskID"] is None
            else html.A(
                str(v["taskID"]),
                href="https://portal.cbrain.mcgill.ca/tasks/inser_ID_here"
                + str(v["taskID"]),
            )
        )
        config = "N/A" if v["toolConfigID"] is None else str(v["toolConfigID"])
        step = dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        "Status: ",
                        status,
                        html.Br(),
                        "Input ID: ",
                        inp,
                        html.Br(),
                        "Output ID: ",
                        out,
                        html.Br(),
                        "Task ID: ",
                        task,
                        html.Br(),
                        "Tool Configuration ID: ",
                        config,
                    ],
                    title=k,
                ),
            ],
            start_collapsed=True,
        )
        metadata.append(step)

    y_subject = (
        "Subject: "
        + df[
            (df["Dataset-Pipeline"] == y)
            & (df["Result"] == clickData["points"][0]["y"])
        ]["Subject"].iloc[0]
    )
    y_pipeline = "Dataset-Pipeline: " + y
    y_result = (
        "Result: N/A"
        if clickData["points"][0]["y"] == -1
        else "Result: " + str(clickData["points"][0]["y"])
    )
    metadata += [
        html.Br(),
        y_subject,
        html.Br(),
        y_pipeline,
        html.Br(),
        y_result,
        html.Br(),
        "Pipeline steps:",
        html.Br(),
        html.Br(),
    ]
    y_metadata = df[
        (df["Dataset-Pipeline"] == y) & (df["Result"] == clickData["points"][0]["y"])
    ]["Metadata"].iloc[0]
    for k, v in list(y_metadata.items())[:-1]:
        status = "Incomplete" if v["status"] is None else v["status"]
        inp = (
            "N/A"
            if v["inputID"] is None
            else html.A(
                str(v["inputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["inputID"]),
            )
        )
        out = (
            "N/A"
            if v["outputID"] is None
            else html.A(
                str(v["outputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["outputID"]),
            )
        )
        task = (
            "N/A"
            if v["taskID"] is None
            else html.A(
                str(v["taskID"]),
                href="https://portal.cbrain.mcgill.ca/tasks/inser_ID_here"
                + str(v["taskID"]),
            )
        )
        config = "N/A" if v["toolConfigID"] is None else str(v["toolConfigID"])
        step = dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        "Status: ",
                        status,
                        html.Br(),
                        "Input ID: ",
                        inp,
                        html.Br(),
                        "Output ID: ",
                        out,
                        html.Br(),
                        "Task ID: ",
                        task,
                        html.Br(),
                        "Tool Configuration ID: ",
                        config,
                    ],
                    title=k,
                ),
            ],
            start_collapsed=True,
        )
        metadata.append(step)

    return dbc.Card(dbc.CardBody(metadata, className="card-text"))
