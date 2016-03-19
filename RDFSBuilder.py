import csv
import os

def set_path(var):
    global path    # Needed to modify global copy of globvar
    path = var
    return path

def getName(eventCode, dictionary):
    for item in dictionary:
        if item[0] == eventCode:
            return item[1]
    return 'NoName'

def writeClass(prefix, instance, class_):
    if instance != '':
        path.write(prefix + instance + '\t a \t' + prefix + class_ + ' ;\n')
    return 0

def writeProperty(prefix, predicate, object_):
    if object_ != '':
        path.write('\t' + predicate + '\t' + prefix + object_ + ' ;\n')
    return 0

def writeTerminus(prefix, predicate, object_):
    if object_ != '':
        path.write('\t' + predicate + '\t' + prefix + object_ + ' .\n')
    return 0

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

set_path(fw)
# remove headers
cameoXR.pop(0)
entries.pop(0)

print "Writing Headers...\n"

# Write header to file
fw.write("@prefix eventDB: <http://www.kearnsw.com/eventDB#> .\n"
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
    for i in range(len(entry)):
        entry[i] = entry[i].translate(None, ''.join(charsToRemove)).strip()
    eventName = eventName.translate(None, ''.join(charsToRemove)).strip()

    # Write event classes
    writeClass(prefix, entry[0], 'event')
    writeProperty(prefix, 'eventDB:hasActor1', entry[6])
    writeProperty(prefix, 'eventDB:hasActor2', entry[16])
    writeProperty(prefix, 'eventDB:hasDate', entry[1])
    writeProperty(prefix, 'eventDB:hasCode', entry[27])
    writeProperty(prefix, 'eventDB:hasGoldsteinScale', entry[31])
    writeProperty(prefix, 'eventDB:hasAvgTone', entry[35])
    writeProperty(prefix, 'eventDB:hasCountryFIPS', entry[51])
    writeTerminus(prefix, 'eventDB:hasName', eventName)

    # Write Actor1 class
    if entry[6] not in listOfActors:
        writeClass(prefix, entry[6], 'actor')
        writeProperty(prefix, 'eventDB:hasCountryCode', entry[7])
        writeProperty(prefix, 'eventDB:hasGroupCode', entry[8])
        writeProperty(prefix, 'eventDB:hasEthnicCode', entry[9])
        writeProperty(prefix, 'eventDB:hasReligion', entry[10])
        writeProperty(prefix, 'eventDB:hasReligion', entry[11])
        writeProperty(prefix, 'eventDB:hasTypeCode', entry[12])
        writeProperty(prefix, 'eventDB:hasTypeCode', entry[13])
        writeProperty(prefix, 'eventDB:hasTypeCode', entry[14])
        writeTerminus(prefix, 'rdfs:subClassOf', entry[5])
        listOfActors.append(entry[6])

    # Write Actor2 class
    if entry[16] not in listOfActors:
        writeClass(prefix, entry[16], 'actor')
        writeProperty(prefix, 'eventDB:hasCountryCode', entry[17])
        writeProperty(prefix, 'eventDB:hasGroupCode', entry[18])
        writeProperty(prefix, 'eventDB:hasEthnicCode', entry[19])
        writeProperty(prefix, 'eventDB:hasReligion', entry[20])
        writeProperty(prefix, 'eventDB:hasReligion', entry[21])
        writeProperty(prefix, 'eventDB:hasTypeCode', entry[22])
        writeProperty(prefix, 'eventDB:hasTypeCode', entry[23])
        writeProperty(prefix, 'eventDB:hasTypeCode', entry[24])
        writeTerminus(prefix, 'rdfs:subClassOf', entry[15])
        listOfActors.append(entry[16])

    # Write country class from Actor1
    if entry[7] not in listOfCountries:
        writeClass(prefix, entry[7], 'country')
        if entry[7] in listOfAfricanCountries:
            writeTerminus(prefix, 'rdfs:subClassOf', 'AfricanUnionCountry')
        elif entry[7] in listOfNATOCountries:
            writeTerminus(prefix, 'rdfs:subClassOf', 'NATOCountry')
        elif entry[7] in listOfRussianAlliedCountries:
            writeTerminus(prefix, 'rdfs:subClassOf', 'russianAlliedCountry')
        else:
            writeTerminus(prefix, 'rdfs:subClassOf', 'otherCountry')
        listOfCountries.append(entry[7])

    # Write country class from Actor2
    if entry[17] not in listOfCountries:
        writeClass(prefix, entry[17], 'country')
        if entry[17] in listOfAfricanCountries:
            writeTerminus(prefix, 'rdfs:subClassOf', 'africanUnionCountry')
        elif entry[17] in listOfNATOCountries:
            writeTerminus(prefix, 'rdfs:subClassOf', 'NATOCountry')
        elif entry[17] in listOfRussianAlliedCountries:
            writeTerminus(prefix, 'rdfs:subClassOf', 'russianAlliedCountry')
        else:
            writeTerminus(prefix, 'rdfs:subClassOf', 'otherCountry')
        listOfCountries.append(entry[17])

fw.close()

