import streamlit as st
from datetime import datetime
from fpdf import FPDF
import os
from PIL import Image
import torch
import cv2
import numpy as np

# Load YOLOv5 model (pre-trained for general object detection)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def generate_pdf(patient_name, surgical_plan, control_plan, prosthetic_plan, timeline):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Dental Treatment Plan for {patient_name}", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Surgical Phase:", ln=True)
    for item in surgical_plan:
        pdf.cell(200, 10, txt=f"- {item}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Control Phase:", ln=True)
    for item in control_plan:
        pdf.cell(200, 10, txt=f"- {item}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Prosthetic Phase:", ln=True)
    for item in prosthetic_plan:
        pdf.cell(200, 10, txt=f"- {item}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Estimated Timeline:", ln=True)
    for item in timeline:
        pdf.cell(200, 10, txt=f"- {item}", ln=True)

    file_path = f"treatment_plan_{patient_name.replace(' ', '_')}.pdf"
    pdf.output(file_path)
    return file_path

def analyze_image(image_data):
    img = Image.open(image_data)
    img_array = np.array(img)
    results = model(img_array)
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    img_height, img_width = img.size[1], img.size[0]
    new_img = np.array(img)
    count = {"caries": 0, "missing": 0, "lesion": 0}

    for label, cord in zip(labels, cords):
        x1, y1, x2, y2, conf = cord
        x1, y1, x2, y2 = int(x1 * img_width), int(y1 * img_height), int(x2 * img_width), int(y2 * img_height)

        # Simulate detection classes based on label id (random mapping for now)
        if int(label) % 3 == 0:
            color = (0, 255, 0)  # Green for caries
            text = "Caries"
            count["caries"] += 1
        elif int(label) % 3 == 1:
            color = (255, 0, 0)  # Blue for missing teeth
            text = "Missing"
            count["missing"] += 1
        else:
            color = (255, 165, 0)  # Orange for lesion
            text = "Lesion"
            count["lesion"] += 1

        cv2.rectangle(new_img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(new_img, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return new_img, count

def main():
    st.title("Dental Treatment Plan Recommendation Software 🦷")

    # Patient Info
    st.header("1. Patient Information")
    patient_name = st.text_input("Patient Name:")
    patient_age = st.number_input("Patient Age:", min_value=1, max_value=120)
    chief_complaint = st.text_area("Chief Complaint:")

    # Upload section
    st.header("2. Upload Patient Documentation")
    photos = st.file_uploader("Upload Intraoral/Extraoral Photographs", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    pano = st.file_uploader("Upload Panoramic Radiograph (Panorama)", type=['png', 'jpg', 'jpeg'])

    if patient_name and photos and pano:
        st.success("All necessary files uploaded!")

        # Image Analysis
        st.header("3. AI Analysis of Uploaded Images")
        if st.button("Analyze Radiographs"):
            st.subheader("Analysis Results:")
            for uploaded_file in photos + [pano]:
                annotated_img, count = analyze_image(uploaded_file)
                st.image(annotated_img, caption=f"Findings: {count}", use_column_width=True)

        # Treatment Plan Generation
        st.header("4. Proposed Treatment Plan")

        surgical_plan = [
            "Extraction of non-restorable teeth.",
            "Surgical removal of impacted teeth if any.",
            "Ridge preservation grafting if needed."
        ]

        control_plan = [
            "Full mouth scaling and root planing.",
            "Endodontic treatments for teeth with periapical lesions or deep caries.",
            "Temporary restorations where needed."
        ]

        prosthetic_plan = [
            "Definitive crowns for structurally compromised teeth.",
            "Implant planning for missing teeth sites.",
            "Removable partial denture if implants are not an option."
        ]

        timeline = [
            "Month 1-2: Initial therapy and extractions.",
            "Month 2-4: Healing and endodontic treatment.",
            "Month 4-6: Implant placement (if applicable).",
            "Month 7-9: Final prosthetic rehabilitation."
        ]

        st.subheader("Surgical Phase")
        for step in surgical_plan:
            st.write("-", step)

        st.subheader("Control Phase")
        for step in control_plan:
            st.write("-", step)

        st.subheader("Prosthetic Phase")
        for step in prosthetic_plan:
            st.write("-", step)

        st.subheader("Estimated Timeline")
        for step in timeline:
            st.write("-", step)

        if st.button("Download Treatment Plan PDF"):
            pdf_path = generate_pdf(patient_name, surgical_plan, control_plan, prosthetic_plan, timeline)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name=pdf_path)
            os.remove(pdf_path)

        # Approval
        st.header("5. Approval")
        approval = st.radio("Do you approve the proposed treatment plan?", ("Yes", "No"))

        if approval == "Yes":
            st.success("Thank you! Proceeding to schedule clinical appointments.")
        else:
            st.warning("Please consult the dentist for alternative options.")

if __name__ == "__main__":
    main()
