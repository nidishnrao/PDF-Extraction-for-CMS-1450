import fitz  
import json

with open("cms1450_template.json", "r") as f:
    field_template = json.load(f)

def extract_fields(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_fields = []

    for page in doc:
        widgets = page.widgets()
        if not widgets:
            continue

        for widget in widgets:
            field_name = widget.field_name 
            field_value = widget.field_value 
            rect = widget.rect  

            field_info = {
                "name": field_name,
                "value": field_value or "NA",
                "bbox": {
                    "x0": rect.x0,
                    "y0": rect.y0,
                    "x1": rect.x1,
                    "y1": rect.y1
                }
            }

            extracted_fields.append(field_info)

    return extracted_fields

def extract_by_bbox_match(form_fields, template):
    extracted = {}

    for field_def in template:
        label = field_def["label"]
        tbbox = field_def["bbox"]

        for field in form_fields:
            fbbox = field["bbox"]

            if (abs(fbbox["x0"] - tbbox["x0"]) < 3 and abs(fbbox["y0"] - tbbox["y0"]) < 3 and abs(fbbox["x1"] - tbbox["x1"]) < 3 and abs(fbbox["y1"] - tbbox["y1"]) < 3):
                extracted[label] = field["value"]
                break

    return extracted

pdf_path = "CMS 1450 Forms/CMS Form 1450 SPC111.pdf"  
form_fields = extract_fields(pdf_path)
matched_fields = extract_by_bbox_match(form_fields, field_template)

with open("cms1450_extracted_fields.json", "w") as f:
    json.dump(matched_fields, f, indent=2)
