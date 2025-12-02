import xml.dom.minidom as minidom
from xml.etree.ElementTree import Element, SubElement, tostring
import pandas as pd
import os
import pathlib

# Generates ABox ontology instances from the courses dataset

def generate_abox(csv_path, output_path="abox.owl"):
    df = pd.read_csv(csv_path)

    rdf = Element(
        "rdf:RDF",
        {
            "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "xmlns:rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xmlns:owl": "http://www.w3.org/2002/07/owl#",
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema#",
            "xml:base": "http://example.org/course_ontology",
        },
    )

    # ABox: Instances for each dataset row
    for idx, row in df.iterrows():
        # Course individual
        cid = row["course_title"].replace(" ", "_")
        course = SubElement(rdf, "owl:NamedIndividual", {"rdf:about": f"#{cid}"})
        SubElement(course, "rdf:type", {"rdf:resource": "#Course"})
        SubElement(course, "courseTitle", {"rdf:datatype": "xsd:string"}).text = str(row["course_title"])

        # Description object
        desc_id = f"Desc_{cid}"
        desc = SubElement(rdf, "owl:NamedIndividual", {"rdf:about": f"#{desc_id}"})
        SubElement(desc, "rdf:type", {"rdf:resource": "#DescriptionText"})
        SubElement(desc, "descriptionText", {"rdf:datatype": "xsd:string"}).text = str(row["Description"])
        SubElement(desc, "originalDescription", {"rdf:datatype": "xsd:string"}).text = str(row["original_description"])
        SubElement(desc, "combinedDescription", {"rdf:datatype": "xsd:string"}).text = str(row["combined_description"])

        # Link description to course
        SubElement(course, "hasDescription", {"rdf:resource": f"#{desc_id}"})

        # Skills
        if pd.notna(row["extracted_skills"]):
            skills = [s.strip() for s in row["extracted_skills"].split(',')]
            for s in skills:
                sid = s.replace(" ", "_")
                skill = SubElement(rdf, "owl:NamedIndividual", {"rdf:about": f"#{sid}"})
                SubElement(skill, "rdf:type", {"rdf:resource": "#Skill"})
                SubElement(skill, "skillName", {"rdf:datatype": "xsd:string"}).text = s
                SubElement(course, "hasSkill", {"rdf:resource": f"#{sid}"})

    xml_str = minidom.parseString(tostring(rdf)).toprettyxml(indent=" ")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"ABox ontology saved to {output_path}")

if __name__ == "__main__":
    actual_output_path = os.path.abspath(pathlib.Path("abox.owl"))
    dataset_csv_path = os.path.abspath(pathlib.Path("courses_dataset.csv"))
    generate_abox(dataset_csv_path, actual_output_path)