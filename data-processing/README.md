# About
All the data processing took place in Dataiku DSS. This included sourcing the data through Dataiku's provided Project Gutenberg plugin, which was immensely helpful in getting our data quickly and in a nice structured format.

The complete Dataiku DSS project is included in this directory.

In order to run the project, DSS should be setup with a Spark runtime environment. This can be CDH, HDP, MapR, EMR, Dataproc, HDInsights, local docker container or Spark on Kubernetes. The required python packages are included in the `dataiku-requirements.txt` file.

All the included data processing scripts below are based on python, pyspark, or spark scala. The loading and saving of datasets in these scripts will be particular to how Dataiku manages data. These lines can be replaced for importing the datasets from the appropriate location. Easy to modify and update :)

