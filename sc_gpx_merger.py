#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://www.topografix.com/GPX/1/1")
ET.register_namespace("gpxtpx", "http://www.garmin.com/xmlschemas/TrackPointExtension/v2")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

NS = {
    "gpx": "http://www.topografix.com/GPX/1/1",
    "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v2"
}

def clean_trkpt(trkpt):
    ext = trkpt.find("gpx:extensions", NS)
    if ext is None:
        return

    # Remove <distance>
    dist_elem = ext.find("gpx:distance", NS)
    if dist_elem is not None:
        ext.remove(dist_elem)

    # Remove <gpxtpx:course>
    tpx = ext.find("gpxtpx:TrackPointExtension", NS)
    if tpx is not None:
        course_elem = tpx.find("gpxtpx:course", NS)
        if course_elem is not None:
            tpx.remove(course_elem)

        # Optional: remove empty TrackPointExtension
        if len(tpx) == 0:
            ext.remove(tpx)

    # Optional: remove empty <extensions>
    if len(ext) == 0:
        trkpt.remove(ext)

def clean_trkseg(trkseg):
    for trkpt in trkseg.findall("gpx:trkpt", NS):
        clean_trkpt(trkpt)

def clean_track(trk):
    for trkseg in trk.findall("gpx:trkseg", NS):
        clean_trkseg(trkseg)

def merge_gpx(output_file, input_files):
    if not input_files:
        raise ValueError("No input files provided")

    # Base file
    base_tree = ET.parse(input_files[0])
    base_root = base_tree.getroot()
    base_trk = base_root.find("gpx:trk", NS)

    if base_trk is None:
        raise ValueError(f"{input_files[0]} has no <trk>")

    clean_track(base_trk)

    # Merge others
    for file in input_files[1:]:
        tree = ET.parse(file)
        root = tree.getroot()
        trk = root.find("gpx:trk", NS)

        if trk is None:
            print(f"Warning: {file} has no <trk>, skipping")
            continue

        for trkseg in trk.findall("gpx:trkseg", NS):
            clean_trkseg(trkseg)
            base_trk.append(trkseg)

    ET.indent(base_tree, space="  ")
    base_tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_gpx.py output.gpx input1.gpx input2.gpx ...")
        sys.exit(1)

    output = sys.argv[1]
    inputs = sys.argv[2:]

    merge_gpx(output, inputs)