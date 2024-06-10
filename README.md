# Pollution Forecast App

This repository contains the script and documentation for the project we completed during the data science training.

## Part 1: Data

### Subpart 1: Pollutant

We get data from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/).

Here we were able to collect data in CSV format from 2021 to now ([link](https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/)), but before 2021 ([link](https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/old/)) it was only available in XML. So the goal was to transform those XML files. To download those data I chose to use Talend Open Studio because I wanted to learn how to use it and it seemed well-suited for data loading. Here is the job schema that I used to download the CSV and XML files and then the pyhton scripts that I used to process the conversion from XML to CSV.

#### Job 2021 to Now (csv Format)
![New data](./img/job_csv.png "Talend job 2021-Now")


#### Job 2017 to 2021 (xml format)
![New data](./img/job_xml.png "Talend job 2017-201")

add more blabla