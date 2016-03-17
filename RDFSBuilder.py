import csv
import os


def getName(eventCode, dictionary):
    for item in dictionary:
        if item[0] == eventCode:
            return item[1]
    return 'NoName'

# Set path to rdf file 
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
fn = "gdelt_ebola.out"
cameo = "CAMEO.eventcodes.txt"
out = "KR.ttl"
prefix = "eventDB:"

# Read in data
f = open(os.path.join(__location__, fn))
entries = list(csv.reader(f, delimiter='\t'))
f.close()

f = open(os.path.join(__location__, cameo))
cameoXR = list(csv.reader(f, delimiter='\t'))
f.close()

# Open file for writing
fw = open(os.path.join(__location__, out), 'w+')

# remove headers
cameoXR.pop(0)
entries.pop(0)

print "Writing Headers...\n"

# Write header to file
fw.write("@prefix eventDB: <http://www.kearnsw.com/> .\n"
         "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
         "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
         "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")

charsToRemove = [' ', "'", ',', '(', ')', '[', ']', '.', '-', '+']
listOfActors = ['']
listOfCountries = ['']
listOfAfricanCountries = ['AFR', 'GIN', 'CFR', 'EAF', 'NAF', 'SAF', 'WAF', 'DZA', 'AGO',
                          'BEN', 'BWA', 'BDI', 'CMR', 'CAF', 'TCD', 'COD', 'ETH', 'GMB',
                          'KEN', 'LSO', 'LBY', 'LBR', 'MDG', 'MOZ', 'NAM', 'NER', 'NGA',
                          'ZAF', 'SLE', 'SDN', 'ZMB', 'ZWE']
listOfNATOCountries = ['USA', 'NMR', 'EUR', 'GBR', 'FRA', 'CAN', 'BEL', 'DNK', 'ISL',
                       'ITA', 'LUX', 'NLD', 'NOR', 'PRT', 'GRC', 'TUR', 'DEU', 'ESP',
                       'CZE', 'HUN', 'POL', 'BGR', 'EST', 'LVA', 'LTU', 'ROM', 'SVK',
                       'SVN', 'HRV', 'ALB']
listOfRussianAlliedCountries = ['CHN', 'RUS', 'IRN', 'SYR']

print "Building File...\n"
for entry in entries:
    # Cross-reference event codes and their name
    eventName = getName(entry[27], cameoXR)

    # remove special characters that are not recognized by RDF-S
    entry[6] = entry[6].translate(None, ''.join(charsToRemove)).strip()
    entry[16] = entry[16].translate(None, ''.join(charsToRemove)).strip()
    entry[5] = entry[5].translate(None, ''.join(charsToRemove)).strip()
    entry[15] = entry[15].translate(None, ''.join(charsToRemove)).strip()
    eventName = eventName.translate(None, ''.join(charsToRemove)).strip()

    # Write event classes
    fw.write(prefix + entry[0] + '\t a \t' + prefix + 'event' + ' ;\n')
    if entry[5]:
        fw.write('\t' + prefix + 'hasActor1Code' + '\t' + prefix + entry[5] + ' ;\n')
    if entry[15]:
        fw.write('\t' + prefix + 'hasActor2Code' + '\t' + prefix + entry[15] + ' ;\n')
    fw.write('\t' + prefix + 'hasDate' + '\t' + '\"' + entry[1] + '\"' + ' ;\n'
             '\t' + prefix + 'hasCode' + '\t' + prefix + entry[27] + ' ;\n'
             '\t' + prefix + 'hasName' + '\t' + prefix + eventName + ' .\n')

    # Write Actor classes
    if entry[6] not in listOfActors:
        fw.write(prefix + entry[6] + '\t a \t' + prefix + 'actor' + ' ;\n'
                 '\t' + 'rdfs:subClassOf' + '\t' + prefix + entry[5] + ' ;\n'
                 '\t' + prefix + 'hasCountryCode' + '\t' + prefix + entry[7] + ' ;\n'      # Country Code
                 '\t' + prefix + 'hasGroupCode' + '\t' + prefix + entry[8] + ' ;\n'      # Group Code
                 '\t' + prefix + 'hasTypeCode' + '\t' + prefix + entry[12] + ' .\n')    # Type Code
        listOfActors.append(entry[6])

    if entry[16] not in listOfActors:
        fw.write(prefix + entry[16] + '\t a \t' + prefix + 'actor' + ' ;\n'
                 '\t' + 'rdfs:subClassOf' + '\t' + prefix + entry[15] + ' ;\n'
                 '\t' + prefix + 'hasCountryCode' + '\t' + prefix + entry[17] + ' ;\n'     # Country Code
                 '\t' + prefix + 'hasGroupCode' + '\t' + prefix + entry[18] + ' ;\n'     # Group Code
                 '\t' + prefix + 'hasTypeCode' + '\t' + prefix + entry[22] + ' .\n')    # Type Code
        listOfActors.append(entry[16])

    # Write Country Classes
    if entry[7] not in listOfCountries:
        fw.write(prefix + entry[7] + '\t a \t' + prefix + 'country' + ' ;\n')
        if entry[7] == '':
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + 'noCountry' + ' .\n')
        elif entry[7] in listOfAfricanCountries:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'africanCountry' + ' .\n')
        elif entry[7] in listOfNATOCountries:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'NATOCountry' + ' .\n')
        elif entry[7] in listOfRussianAlliedCountries:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'russianAlliedCountry' + ' .\n')
        else:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'otherCountry' + ' .\n')
        listOfCountries.append(entry[7])

    if entry[17] not in listOfCountries:
        fw.write(prefix + entry[17] + '\t a \t' + prefix + 'country' + ' ;\n')
        if entry[17] == '':
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + 'noCountry' + ' .\n')
        elif entry[17] in listOfAfricanCountries:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'africanCountry' + ' .\n')
        elif entry[17] in listOfNATOCountries:
            fw.write('\t' + 'rdfs:susbClassOf' + '\t' + prefix + 'NATOCountry' + ' .\n')
        elif entry[17] in listOfRussianAlliedCountries:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'russianAlliedCountry' + ' .\n')
        else:
            fw.write('\t' + 'rdfs:subClassOf' + '\t' + prefix + 'otherCountry' + ' .\n')
        listOfCountries.append(entry[17])
fw.close()

