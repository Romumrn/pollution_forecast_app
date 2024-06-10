# Pollution Forecast App

This repository contains the script and documentation for the project we completed during data science training. The goal is to create a web application that can predict pollution based on previous records and provide the results in a comprehensive dashboard.

## Part 1: Data

### Subpart 1: Pollutant

We get data from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/).

We collected data in CSV format from 2021 to now ([link](https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/)), but before 2021 ([link](https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/old/)) it was only available in XML. To download this data, I used Talend Open Studio because it is well-suited for data loading. Here is the job schema I used to download the CSV and XML files and the Python scripts for converting XML to CSV.

#### Job 2021 to Now (CSV Format)
![New data](./img/job_csv.png "Talend job 2021-Now")

(Add more information about the different composants that I used...)

Example of CSV file (from FR_E2_2021-10-22.csv):

```csv
Date de début;Date de fin;Organisme;code zas;Zas;code site;nom site;type d'implantation;Polluant;type d'influence;discriminant;Réglementaire;type d'évaluation;procédure de mesure;type de valeur;valeur;valeur brute;unité de mesure;taux de saisie;couverture temporelle;couverture de données;code qualité;validité
2021/10/22 00:00:00;2021/10/22 01:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;1.1;1.1;µg-m3;;;;A;1
2021/10/22 01:00:00;2021/10/22 02:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;0.8;0.8;µg-m3;;;;A;1
2021/10/22 02:00:00;2021/10/22 03:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;;;µg-m3;;;;N;-1
2021/10/22 03:00:00;2021/10/22 04:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;1.7;1.7;µg-m3;;;;A;1
2021/10/22 04:00:00;2021/10/22 05:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;2.7;2.725;µg-m3;;;;A;1
2021/10/22 05:00:00;2021/10/22 06:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;11.1;11.05;µg-m3;;;;A;1
2021/10/22 06:00:00;2021/10/22 07:00:00;ATMO GRAND EST;FR44ZAG02;ZAG METZ;FR01011;Metz-Centre;Urbaine;NO;Fond;A;Oui;mesures fixes;Auto NO Conf meth CHIMILU;moyenne horaire validée;7.9;7.9;µg-m3;;;;A;1
```

#### Job 2017 to 2021 (XML Format)
![Old data](./img/job_xml.png "Talend job 2017-2021")

(Add more information about the different composants that I used...)

This [script](./script/xml_to_csv.py) processes air quality data from XML files, converting them to a structured format and storing the results in chunks using pickle. It starts by loading monitoring station information from an [Excel file](https://www.data.gouv.fr/fr/datasets/r/eeebe970-6e2b-47fc-b801-4a38d53fac0d) into a DataFrame and creates a lookup dictionary for easy access. The script defines conversion dictionaries for specific values and sets up namespace mappings for XML parsing.

It finds all XML files in a specified directory and pre-compiles XPath expressions for efficient parsing. The script iterates through each XML file, extracting and processing data using XPath expressions. Relevant information such as observation times, procedures, parameters, observed properties, feature of interest, and parsed values are collected and appended to a list.

Periodically, the script saves this list to a file using pickle and clears the list to handle the next chunk of data.

You can then run the second [script](./script/group_chunk.py), which processes and combines these data chunks into a single CSV file while managing memory efficiently. It lists all pickle files and creates an intermediate directory for temporary CSV files.

The script sets a row limit per intermediate CSV file and initializes an empty DataFrame for combining data chunks. For each pickle file, it loads the data into a DataFrame and appends it to the combined DataFrame. If the combined DataFrame exceeds the row limit, it saves the current data to an intermediate CSV file and resets the DataFrame.

After processing all pickle files, any remaining data is saved to an intermediate CSV file. The script reads all intermediate CSV files, concatenates them into a final DataFrame, sorts the data, and saves it to a single CSV file. It then cleans up by removing all intermediate CSV files and the intermediate directory, ensuring efficient handling of large datasets without exceeding memory limits.

### Subpart 2: Temperature

### Subpart 3: Wind

### Subpart 4: Rain or whatever

### Subpart 5: Combine all data

## Part 2: Data processing for Machine learning

### Subpart 1: Data cleaning

### Subpart 2: Create the machin learning model

## Part 3: Dashboard