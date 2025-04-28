
# 🦷 Dental AI Treatment Planner

Welcome to the future of digital dentistry!  
This AI-powered Streamlit app analyzes patient clinical photos and panoramic radiographs to recommend a complete dental treatment plan — instantly.

## 🚀 Features
- Upload intraoral/extraoral photographs and panoramic X-rays.
- Automatic detection of:
  - Dental caries
  - Missing teeth
  - Periapical lesions
- Generate a full treatment plan:
  - Surgical Phase
  - Control Phase
  - Prosthetic Phase
- Download a PDF treatment summary.
- Patient approval workflow integrated.
- Powered by YOLOv5 deep learning models and Streamlit.



## 🛠 How to Run Locally
```bash
pip install -r requirements.txt
streamlit run treatment_plan_app.py
```

## 🌐 Deploy Your Own App
Deploy your app for free at [Streamlit Cloud](https://streamlit.io/cloud).

## 📜 License
This project is licensed under the MIT License.

---

## 📖 Citation
If you use this tool, please cite:
> Dental AI Treatment Planner, version 1.0.  
> DOI: [To be generated via Zenodo]

---
```

---

# 📜 **requirements.txt**

```plaintext
streamlit
torch
torchvision
yolov5
opencv-python
pillow
fpdf
```

---
