import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import json

def extract_lat_long(shape_str):
    try:
        lat_long_dict = json.loads(shape_str.replace("'", '"'))
        lat = str(lat_long_dict.get('y', '0'))
        lon = str(lat_long_dict.get('x', '0'))
    except json.JSONDecodeError:
        lat, lon = '0', '0'
    return lat, lon

def get_icon_path(waypoint_type):
    icon_paths = {
        "Area Command": "",
        "CAP Unit Position update": "https://github.com/jpat-12/Incident-Icons/blob/main/CAP%20Asset%20Report.png?raw=true",
        "Clue Location": "https://github.com/jpat-12/Incident-Icons/blob/main/CLUE.png?raw=true",
        "ELT Signal": "https://github.com/jpat-12/Incident-Icons/blob/main/ELT.png?raw=true",
        "Flood/Water Level (HWM)": "https://github.com/jpat-12/Incident-Icons/blob/main/Flood.png?raw=true",
        "Hazard, Animal": "https://github.com/jpat-12/Incident-Icons/blob/main/Animal.png?raw=true",
        "Hazard, Electrical": "https://github.com/jpat-12/Incident-Icons/blob/main/Electrical.png?raw=true",
        "Hazard, Fire": "https://github.com/jpat-12/Incident-Icons/blob/main/Fire.png?raw=true",
        "Hazard, Haz Materials": "https://github.com/jpat-12/Incident-Icons/blob/main/Hazard,%20Haz%20Materials.png?raw=true",
        "Hazard, Other": "https://github.com/jpat-12/Incident-Icons/blob/main/Hazard,%20Other.png?raw=true",
        "Helicopter Landing Zone": "https://github.com/jpat-12/Incident-Icons/blob/main/LZHeli.png?raw=true",
        "Incident Command Post": "https://github.com/jpat-12/Incident-Icons/blob/main/Incident%20Command%20Post.png?raw=true",
        "Initial Planning Point": "https://github.com/jpat-12/Incident-Icons/blob/main/Initial%20Planning%20Point.png?raw=true",
        "Initial Planning Point (PLS, LKP)": "https://github.com/jpat-12/Incident-Icons/blob/main/Initial%20Planning%20Point.png?raw=true",
        "Medical Station": "https://github.com/jpat-12/Incident-Icons/blob/main/Medical.png?raw=true",
        "Placeholder Other": "https://github.com/jpat-12/Incident-Icons/blob/main/Placeholder%20Other.png?raw=true",
        "Plane Crash": "https://github.com/jpat-12/Incident-Icons/blob/main/PlaneCrash.png?raw=true",
        "PLT/PLB Signal": "https://github.com/jpat-12/Incident-Icons/blob/main/PLT.png?raw=true",
        "Staging": "https://github.com/jpat-12/Incident-Icons/blob/main/Staging.png?raw=true",
        "Structure, Damaged": "https://github.com/jpat-12/Incident-Icons/blob/main/Structure,%20Damaged.png?raw=true",
        "Structure, Destroyed": "https://github.com/jpat-12/Incident-Icons/blob/main/Destroyed.png?raw=true",
        "Structure, Failed": "https://github.com/jpat-12/Incident-Icons/blob/main/Structure,%20Failed.png?raw=true",
        "Structure, No Damage": "https://github.com/jpat-12/Incident-Icons/blob/main/NoDamage.png?raw=true",
        "Transportation, Route Block": "https://github.com/jpat-12/Incident-Icons/blob/main/Transportation,%20Route%20Block.png?raw=true"
    }
    return icon_paths.get(waypoint_type, "https://github.com/jpat-12/Incident-Icons/blob/main/Placeholder%20Other.png?raw=true")

def create_kml_placemark(data):
    placemark = ET.Element("Placemark")
    placemark.set("id", str(data['objectid']))

    name = ET.SubElement(placemark, "name")
    name.text = f"{data['team_callsign']} - {data['select_a_waypoint_of_what_you_a']}"

    styleUrl = ET.SubElement(placemark, "styleUrl")
    styleUrl.text = "#icon-style"

    extendedData = ET.SubElement(placemark, "ExtendedData")
    for key, value in data.items():
        if key == 'SHAPE':
            continue
        data_elem = ET.SubElement(extendedData, "Data")
        data_elem.set("name", key)
        value_elem = ET.SubElement(data_elem, "value")
        value_elem.text = str(value)

    point = ET.SubElement(placemark, "Point")
    lat, lon = extract_lat_long(data["SHAPE"])
    coordinates = ET.SubElement(point, "coordinates")
    coordinates.text = f"{lon},{lat},0.0"

    return placemark

def parse_csv_and_create_kml(csv_file_path, output_file_path):
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2", xmlns_gx="http://www.google.com/kml/ext/2.2")
    document = ET.SubElement(kml, "Document")
    document.set("id", "1")

    style = ET.SubElement(document, "Style")
    style.set("id", "icon-style")
    iconStyle = ET.SubElement(style, "IconStyle")
    iconStyle.set("id", "icon-style")
    colorMode = ET.SubElement(iconStyle, "colorMode")
    colorMode.text = "normal"
    scale = ET.SubElement(iconStyle, "scale")
    scale.text = "1"
    heading = ET.SubElement(iconStyle, "heading")
    heading.text = "0"
    icon = ET.SubElement(iconStyle, "Icon")
    icon.set("id", "icon")
    href = ET.SubElement(icon, "href")
    href.text = get_icon_path("Placeholder Other")  # Default icon path

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            placemark = create_kml_placemark(row)
            document.append(placemark)

    tree = ET.ElementTree(kml)
    tree.write(output_file_path, encoding='utf-8', xml_declaration=True)

# Pull CSV from 'survey.csv' and write to 'survey.kml'
parse_csv_and_create_kml('survey.csv', 'survey.kml')