import requests
import os


dir= "data"
if not os.path.isdir(dir ):
    os.makedirs(dir )


# https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_XX_previous-1950-2022_RR-T-Vent.csv.gz
# https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_XX_previous-1950-2022_autres-parametres.csv.gz
# https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_XX_latest-2023-2024_RR-T-Vent.csv.gz
# https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_XX_latest-2023-2024_autres-parametres.csv.gz

import requests

for i in range(1, 96):
    # Pad the number with a leading zero if it's a single digit
    if len(str(i)) == 1:
        i = "0" + str(i)
    else:
        i = str(i)
    
    print(i)
    
    # Make the request to download the previous RR-T-Vent data
    req1 = requests.get(f"https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_{i}_previous-1950-2022_RR-T-Vent.csv.gz")
    
    # Check if the request was successful
    if req1.status_code == 200:
        with open(f"{dir}/Q_{i}_previous-1950-2022_RR-T-Vent.csv.gz", mode='wb') as localfile:
            localfile.write(req1.content)
    
    # Make the request to download the previous autres-parametres data
    req2 = requests.get(f"https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_{i}_previous-1950-2022_autres-parametres.csv.gz")
    
    # Check if the request was successful
    if req2.status_code == 200:
        with open(f"{dir}/Q_{i}_previous-1950-2022_autres-parametres.csv.gz", mode='wb') as localfile:
            localfile.write(req2.content)
    
    # Make the request to download the latest RR-T-Vent data
    req3 = requests.get(f"https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_{i}_latest-2023-2024_RR-T-Vent.csv.gz")
    
    # Check if the request was successful
    if req3.status_code == 200:
        with open(f"{dir}/Q_{i}_latest-2023-2024_RR-T-Vent.csv.gz", mode='wb') as localfile:
            localfile.write(req3.content)
    
    # Make the request to download the latest autres-parametres data
    req4 = requests.get(f"https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/QUOT/Q_{i}_latest-2023-2024_autres-parametres.csv.gz")
    
    # Check if the request was successful
    if req4.status_code == 200:
        with open(f"{dir}/Q_{i}_latest-2023-2024_autres-parametres.csv.gz", mode='wb') as localfile:
            localfile.write(req4.content)