# Pollution Forecast App

This repository contains the script and documentation for the project we completed during data science training. The goal is to create a web application that can predict pollution based on previous records and provide the results in a comprehensive dashboard.

## Part 1: Data

### Subpart 1: Pollutant

We get data from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/).

We collected data in CSV format from 2021 to now ([link](https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/)), but before 2021 ([link](https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/old/)) it was only available in XML. To download this data, I used Talend Open Studio because it is well-suited for data loading. Here is the job schema I used to download the CSV and XML files and the Python scripts for converting XML to CSV.

#### Job 2021 to Now (CSV Format)
![New data](./img/job_csv.png "Talend job 2021-Now")

(Add more information about the different components that I used...)

Example of CSV file (from FR_E2_2021-10-22.csv):

```
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

(Add more information about the different components that I used...)

The first script called [/xml_to_csv.py](./script/xml_to_csv.py) processes air quality data from XML files, converting them to a structured format and storing the results in chunks using pickle. It starts by loading monitoring station information from an [Excel file](https://www.data.gouv.fr/fr/datasets/r/eeebe970-6e2b-47fc-b801-4a38d53fac0d) into a DataFrame and creates a lookup dictionary for easy access. The script defines conversion dictionaries for specific values and sets up namespace mappings for XML parsing.

It finds all XML files in a specified directory and pre-compiles XPath expressions for efficient parsing. The script iterates through each XML file, extracting and processing data using XPath expressions. Relevant information such as observation times, procedures, parameters, observed properties, feature of interest, and parsed values are collected and appended to a list. Periodically, the script saves this list to a file using pickle and clears the list to handle the next chunk of data.

You can then run the second script called [group_chunk.py](./script/group_chunk.py), which processes and combines these data chunks into a single CSV file while managing memory efficiently. It lists all pickle files and creates an intermediate directory for temporary CSV files. The script sets a row limit per intermediate CSV file and initializes an empty DataFrame for combining data chunks. For each pickle file, it loads the data into a DataFrame and appends it to the combined DataFrame. If the combined DataFrame exceeds the row limit, it saves the current data to an intermediate CSV file and resets the DataFrame. After processing all pickle files, any remaining data is saved to an intermediate CSV file. (And then if it's possible the script reads all intermediate CSV files, and tries to concatenates them into a final DataFrame, sorts the data, and saves it to a single CSV file.)

Example of data (intermediate0.csv):

```
id,start,end,Polluant,value,verif,valid,name,municipality,latitude,longitude,altitude
FR33305,2018-09-12T00:00:00+00:00,2018-09-12T01:00:00+00:00,NO2,16.7,Not verified,Valid,Bourg-en-Bresse,BOURG-EN-BRESSE,46.211666,5.226389,220
FR33305,2018-09-12T01:00:00+00:00,2018-09-12T02:00:00+00:00,NO2,12.6,Not verified,Valid,Bourg-en-Bresse,BOURG-EN-BRESSE,46.211666,5.226389,220
```

### Subpart 2: Climatic Condition 

As the pollution data, we get data from [data.gouv.fr](https://meteo.data.gouv.fr/datasets/donnees-climatologiques-de-base-quotidiennes/), the data are separated into two categories: wind and other. I created two Python scripts to automate these tasks.

The first script, called [dl_climate_data.py](./script/dl_climate_data.py), downloads multiple CSV files from a specified URL, saving them into a directory. It iterates over department numbers (1 to 95) and constructs URLs to download four CSV files compressed (.gz) per department:
1. Previous RR-T-Vent data (1950-2022)
2. Previous autres-parametres data (1950-2022)
3. Latest RR-T-Vent data (2023-2024)
4. Latest autres-parametres data (2023-2024)

It uses the `requests` library to fetch these files, saving them locally if the request is successful.

Then, I used the second script called [process_climate_data.py](./script/process_climate_data.py). This script processes the downloaded CSV files for each department. It reads and filters the data to remove rows recorded before 2017. It concatenates the filtered data for 'Vent' and 'autres-parametres' files into single DataFrames per department, retaining only data after 2017 (since we do not have pollution data before 2017). Finally, it merges the two DataFrames and saves the combined data into a new CSV file named `data_climate{i}_cleaned.csv`, where `{i}` is the department number.

Example of climate CSV file (data_climate21_cleaned.csv): 
```
NUM_POSTE,NOM_USUEL,LAT,LON,ALTI,AAAAMMJJ,DHUMEC,QDHUMEC,PMERM,QPMERM,PMERMIN,QPMERMIN,INST,QINST,GLOT,QGLOT,DIFT,QDIFT,DIRT,QDIRT,INFRART,QINFRART,UV,QUV,UV_INDICEX,QUV_INDICEX,SIGMA,QSIGMA,UN,QUN,HUN,QHUN,UX,QUX,HUX,QHUX,UM,QUM,DHUMI40,QDHUMI40,DHUMI80,QDHUMI80,TSVM,QTSVM,ETPMON,QETPMON,ETPGRILLE,QETPGRILLE,ECOULEMENTM,QECOULEMENTM,HNEIGEF,QHNEIGEF,NEIGETOTX,QNEIGETOTX,NEIGETOT06,QNEIGETOT06,NEIG,QNEIG,BROU,QBROU,ORAG,QORAG,GRESIL,QGRESIL,GRELE,QGRELE,ROSEE,QROSEE,VERGLAS,QVERGLAS,SOLNEIGE,QSOLNEIGE,GELEE,QGELEE,FUMEE,QFUMEE,BRUME,QBRUME,ECLAIR,QECLAIR,NB300,QNB300,BA300,QBA300,TMERMIN,QTMERMIN,TMERMAX,QTMERMAX,RR,QRR,TN,QTN,HTN,QHTN,TX,QTX,HTX,QHTX,TM,QTM,TNTXM,QTNTXM,TAMPLI,QTAMPLI,TNSOL,QTNSOL,TN50,QTN50,DG,QDG,FFM,QFFM,FF2M,QFF2M,FXY,QFXY,DXY,QDXY,HXY,QHXY,FXI,QFXI,DXI,QDXI,HXI,QHXI,FXI2,QFXI2,DXI2,QDXI2,HXI2,QHXI2,FXI3S,QFXI3S,DXI3S,QDXI3S,HXI3S,QHXI3S
21056001,BEIRE LE CHATEL,47.413833,5.208333,250,20230101,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,2.2,9.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0.0,1.0,8.4,1.0,304.0,9.0,16.3,1.0,1324.0,9.0,12.1,1.0,12.4,1.0,7.9,1.0,,,,,0.0,9.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,
21056001,BEIRE LE CHATEL,47.413833,5.208333,250,20230102,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1.4,9.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1.2,1.0,8.2,1.0,1724.0,9.0,12.7,1.0,743.0,9.0,10.1,1.0,10.5,1.0,4.5,1.0,,,,,0.0,9.0,,,,,,,,,,,,,,,,,,,,,,,,,,,,
```

### Subpart 3: Combine All Data

(We need to find a way to combine these DataFrames with the location data, as the names of weather and pollution stations are not similar.)

## Part 2: Data Processing for Machine Learning

### Subpart 1: Data Cleaning

### Subpart 2: Create the Machine Learning Model

## Part 3: Dashboard
