# Dask on CML

![images/DASK.png]

Run Dask on CML with the workers API.

In the hands of an experienced practitioner, AutoML holds much promise for automating away some of the tedious parts of building machine learning systems.
TPOT is a library for performing sophisticated search over whole ML pipelines, selecting preprocessing steps and algorithm hyperparameters to optimize for your use case.
While saving the data scientist a lot of manual effort, performing this search is computationally costly.
In this Applied ML Prototype, we go beyond what we can do achieve with a laptop, and use the Cloudera Machine Learning Workers API to spin up an on-demand Dask cluster to distribute AutoML computations.
This sets us up for automated machine learning at scale!

## Deploying on Cloudera Machine Learning (CML)

There are three ways to launch this project on CML:

1. From AMP Catalog - Navigate to the AMP Catalog in a CML workspace, select the "AutoML with TPOT" tile, click "Launch as Project", click "Configure Project".
2. As ML Prototype - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the repo URL, click "Create Project", click "Configure Project"
3. Manual Setup - In a CML workspace, click "New Project", add a Project Name, select "Git" as the Initial Setup option, copy in the repo URL, click "Create Project".  All library and model dependencies are installed inline in the notebook.

Once the project has been initialized in a CML workspace, run the `dask.ipynb` notebook by starting a Python 3.7+ JupyterLab or notebook session.