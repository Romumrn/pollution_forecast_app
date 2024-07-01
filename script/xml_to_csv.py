import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import glob
import time
import pickle

start_time = time.time()

# Load the Excel data into a DataFrame
df_position = pd.read_excel("C:/Users/Administrateur/Documents/fr-2023-d-lcsqa-ineris-20230717.xls")

# Create a lookup dictionary from the DataFrame
position_lookup = df_position.set_index('NatlStationCode').to_dict(orient='index')

# Pollutant conversion dictionaries
convertpollutant = {
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/1': 'SO2',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/3': 'SA',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/4': 'SPM',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/5': 'PM10',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6': "BS",
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/7': 'O3',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8': 'NO2',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/9': 'NOX',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/10': 'CO',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/11':'H2S',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/12':'Pb',
    'http://dd.eionet.europa.eu/vocabularyconcept/aq/pollutant/13' : 'Hg',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/21': 'C6H5-CH3',
    'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001': 'PM2.5',
}

convertverified = {
 "1": "Verified",
 "2": "Preliminary verified",
 "3": "Not verified" 
}

convertvalidation = {
 "-99": "Not valid due to station maintenance",
 "-1": "Not valid",
 "1": "Valid",
 "2": "Valid, but below detection limit",
 "3": "Valid, but below detection limit .." 
}

# Define the namespace mappings
namespaces = {
    'gml': 'http://www.opengis.net/gml/3.2',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'aqd': 'http://dd.eionet.europa.eu/schemaset/id2011850eu-1.0',
    'base': 'http://inspire.ec.europa.eu/schemas/base/3.3',
    'base2': 'http://inspire.ec.europa.eu/schemas/base2/1.0',
    'ef': 'http://inspire.ec.europa.eu/schemas/ef/3.0',
    'ompr': 'http://inspire.ec.europa.eu/schemas/ompr/2.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'sam': 'http://www.opengis.net/sampling/2.0',
    'sams': 'http://www.opengis.net/samplingSpatial/2.0',
    'gmd': 'http://www.isotc211.org/2005/gmd',
    'gco': 'http://www.isotc211.org/2005/gco',
    'om': 'http://www.opengis.net/om/2.0',
    'swe': 'http://www.opengis.net/swe/2.0',
    'am': 'http://inspire.ec.europa.eu/schemas/am/3.0',
    'ad': 'urn:x-inspire:specification:gmlas:Addresses:3.0',
    'gn': 'urn:x-inspire:specification:gmlas:GeographicalNames:3.0'
}

big_list = []

# List XML files
list_xml_files = glob.glob("C:/Users/Administrateur/Documents/talend/data/xml/*.xml")

# Compile XPath expressions
xpath_obs = etree.XPath('.//om:OM_Observation', namespaces=namespaces)
xpath_begin_time = etree.XPath('.//gml:beginPosition', namespaces=namespaces)
xpath_end_time = etree.XPath('.//gml:endPosition', namespaces=namespaces)
xpath_result_time = etree.XPath('.//gml:timePosition', namespaces=namespaces)
xpath_procedure = etree.XPath('.//om:procedure', namespaces=namespaces)
xpath_parameter = etree.XPath('.//om:parameter/om:NamedValue', namespaces=namespaces)
xpath_observed_property = etree.XPath('.//om:observedProperty', namespaces=namespaces)
xpath_feature_of_interest = etree.XPath('.//om:featureOfInterest', namespaces=namespaces)
xpath_values = etree.XPath('.//swe:values', namespaces=namespaces)
xpath_measure_unit = etree.XPath('.//swe:uom', namespaces=namespaces)

c = 0
chunk_counter = 0
chunk_size = 200

def save_chunk(chunk_counter, big_list):
    filename = f"data_chunk_{chunk_counter}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(big_list, f)
    print(f"------- Saved {filename} with {len(big_list)} records.  -----")
    big_list.clear()

for xml_file in list_xml_files:
    try:
        # Parse the XML file
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # Find all OM_Observation elements
        observations = xpath_obs(root)

        # Iterate over each observation and extract the required information
        for obs in observations:
            obs_id = obs.attrib.get('{http://www.opengis.net/gml/3.2}id', 'N/A')
            
            # Extract phenomenonTime
            begin_time = xpath_begin_time(obs)[0].text if xpath_begin_time(obs) else 'N/A'
            end_time = xpath_end_time(obs)[0].text if xpath_end_time(obs) else 'N/A'

            # Extract resultTime
            result_time = xpath_result_time(obs)[0].text if xpath_result_time(obs) else 'N/A'
            
            # Extract procedure
            procedure_href = xpath_procedure(obs)[0].attrib.get('{http://www.w3.org/1999/xlink}href', 'N/A')
            
            # Extract parameters
            parameters = {param.find('.//om:name', namespaces).attrib.get('{http://www.w3.org/1999/xlink}href', 'N/A'):
                        param.find('.//om:value', namespaces).attrib.get('{http://www.w3.org/1999/xlink}href', 'N/A')
                        for param in xpath_parameter(obs)}

            # Extract observedProperty
            observed_property_href = xpath_observed_property(obs)[0].attrib.get('{http://www.w3.org/1999/xlink}href', 'N/A')
            
            # Extract featureOfInterest
            feature_of_interest_href = xpath_feature_of_interest(obs)[0].attrib.get('{http://www.w3.org/1999/xlink}href', 'N/A')
            location_id = feature_of_interest_href.split("-")[-1].split("_")[0]

            # Lookup location information
            location_info = position_lookup.get(location_id, {})
            name = location_info.get('Name', '')
            municipality = location_info.get('Municipality', '')
            latitude = location_info.get('Latitude', '')
            longitude = location_info.get('Longitude', '')
            altitude = location_info.get('Altitude', '')

            # Extract measure unit
            measure_unit = xpath_measure_unit(obs)[0].attrib.get('code', 'N/A') if xpath_measure_unit(obs) else 'N/A'

            # Extract and parse the values
            values_element = xpath_values(obs)
            if values_element and values_element[0].text:
                raw_values = values_element[0].text.strip()
                block_separator = '@@'
                token_separator = ','

                blocks = raw_values.split(block_separator)
                parsed_values = [block.split(token_separator) for block in blocks]
                
                # Append parsed values to big_list
                for block in parsed_values:
                    if len(block) > 1:
                        start = block[0]
                        end = block[1]
                        verif  = convertverified[block[2]]
                        valid = convertvalidation[block[3]]
                        value = block[4]

                        big_list.append({
                            "id": location_id,
                            "start": start,
                            "end": end,
                            "Polluant": convertpollutant.get(observed_property_href, 'Unknown'),
                            "value": value,
                            "measure_unit": measure_unit,
                            "verif": verif,
                            "valid": valid,
                            "name": name,
                            "municipality": municipality,
                            "latitude": latitude,
                            "longitude": longitude,
                            "altitude": altitude
                        })
        c += 1

        # Save chunk periodically
        if c % chunk_size == 0:
            chunk_counter += 1
            save_chunk(chunk_counter, big_list)

        print(f" - Processing data since {round((time.time() - start_time) / 60, 5)} mins, processed {round(c/len(list_xml_files)* 100 , 4) } % - ", end='\r')
    except Exception as e:
        print(f"PROBLEM WITH {xml_file}: {e}")

# Save any remaining data
if big_list:
    chunk_counter += 1
    save_chunk(chunk_counter, big_list)

# # Combine all pickle files into a final DataFrame and save as CSV
# all_data = []
# for i in range(1, chunk_counter + 1):
#     with open(f"data_chunk_{i}.pkl", 'rb') as f:
#         chunk_data = pickle.load(f)
#         all_data.extend(chunk_data)

# df = pd.DataFrame(all_data)
# df = df.sort_values(by=['id', 'Polluant', "start"])
# df.to_csv("data_pollutant_from_xml.csv", index=False)

# print("-- DONE in %s seconds --" % (time.time() - start_time))
