from lxml.etree import Element, SubElement, tostring

from fitparse import FitFile

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
    # Set schema location
    document.set(XML_SCHEMA + "schemaLocation", SCHEMA_LOCATION)
    return document


def create_lap(activity, lap_data):
    pass


def create_activity_section(activities, file):
    # Add the session
    file_id = next(file.get_messages(name='file_id'))
    session = next(file.get_messages(name='sport'))
    activity = SubElement(activities, "Activity")
    # Add the sport and activity summary information
    activity.attrib['Sport'] = SPORT_MAP.get(session.get_value("sport"), "Other")
    id_elem = SubElement(activity, "Id")
    id_elem.text = file_id.get_value('time_created').isoformat() + 'Z'

    # TODO - Iterate through all the lap data


def write_tcx(options) -> None:
    file = FitFile(
        options.infile,
        check_crc=not options.ignore_crc
    )
    file.parse()
    # Create the document
    tcx_doc = create_document()
    activities = SubElement(tcx_doc, "Activities")
    # Create the activities section
    create_activity_section(activities, file)
    # Write the file
    options.output.write(tostring(tcx_doc, xml_declaration=True, pretty_print=True,
                                  encoding='utf-8').decode('utf-8'))
    pass
