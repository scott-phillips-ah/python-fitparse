from lxml.etree import Element, SubElement, tostring


TCD_NAMESPACE = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
TCD = "{%s}" % TCD_NAMESPACE

XML_SCHEMA_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"
XML_SCHEMA = "{%s}" % XML_SCHEMA_NAMESPACE

SCHEMA_LOCATION = \
    "http://www.garmin.com/xmlschemas/ActivityExtension/v2 " + \
    "http://www.garmin.com/xmlschemas/ActivityExtensionv2.xsd " + \
    "http://www.garmin.com/xmlschemas/FatCalories/v1 " + \
    "http://www.garmin.com/xmlschemas/fatcalorieextensionv1.xsd " + \
    "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 " + \
    "http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"

NSMAP = {
    None: TCD_NAMESPACE,
    "xsi": XML_SCHEMA_NAMESPACE
}

# FIT to TCX values mapping

LAP_TRIGGER_MAP = {
    "manual": "Manual",
    "time": "Time",
    "distance": "Distance",
    "position_start": "Location",
    "position_lap": "Location",
    "position_waypoint": "Location",
    "position_marked": "Location",
    "session_end": "Manual",
    "fitness_equipment": "Manual"}

INTENSITY_MAP = {
    "active": "Active",
    "warmup": "Active",
    "cooldown": "Active",
    "rest": "Resting"}

SPORT_MAP = {
    "running": "Running",
    "cycling": "Biking"}


def create_element(tag, text=None, namespace=None):
    namespace = NSMAP[namespace]
    tag = "{%s}%s" % (namespace, tag)
    element = Element(tag, nsmap=NSMAP)

    if text is not None:
        element.text = text

    return element


def create_document() -> Element:
    document = Element("TrainingCenterDatabase", nsmap=NSMAP)
    # TODO - Set schema location
    document.set(XML_SCHEMA + "schemaLocation", SCHEMA_LOCATION)
    return document


def create_activity_section(tcx_doc: Element, records: list) -> None:
    activities_elem = SubElement(tcx_doc, "Activities")
    # Add the session
    activity_elem = SubElement(activities_elem, "Activity")
    sport_record = next(x for x in records if x.name == 'sport')
    sport_name = next(f.value for f in sport_record.fields if f.name == 'sport')
    activity_elem.attrib['Sport'] = SPORT_MAP[sport_name]
    # TODO - Add the sport and activity summary information
    # TODO - Iterate through all the lap data


def write_tcx(options, records) -> None:
    records = list(records)
    # Create the document
    tcx_doc = create_document()
    # Create the activities section
    create_activity_section(tcx_doc, records)
    # Write the file
    options.output.write(tostring(tcx_doc, xml_declaration=True, pretty_print=True,
                                  encoding='utf-8').decode('utf-8'))
    pass
