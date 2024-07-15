import base64
from PIL import Image
from io import BytesIO
import os
import cv2
from flask import Flask, request
from werkzeug.utils import secure_filename
import shutil
import csv
import datetime
from flask_cors import CORS, cross_origin

uploads_dir = 'uploads'
attemps_dir = 'attempts'
output_json = {}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

term_plans = ['aditya_birla_digishield_plans','bajaj_alliance_life_etouch', 'hdfc_click2protect_super','icici_iprotect_smart', 'max_life_smart_secure_plus' ]

health_plans = ['aditya_birla_activ_health' , 'bajaj_alliance_health_guard', 'hdfc_ergo' , 'icici_lombard', 'tata_aig']

def base64_to_image(base64_string):
    # Remove the data URI prefix if present
    if "data:image" in base64_string:
        base64_string = base64_string.split(",")[1]

    # Decode the Base64 string into bytes
    image_bytes = base64.b64decode(base64_string)
    return image_bytes

def create_image_from_bytes(image_bytes):
    # Create a BytesIO object to handle the image data
    image_stream = BytesIO(image_bytes)

    # Open the image using Pillow (PIL)
    image = Image.open(image_stream)
    return image

def get_term_plans(plan):
    remaining_term_plans = []
    for i in term_plans:
        if i != plan:
            remaining_term_plans.append(i)
    return remaining_term_plans

def get_health_plans(plan):
    remaining_health_plans = []
    for i in health_plans:
        if i != plan:
            remaining_health_plans.append(i)
    return remaining_health_plans

@app.route('/insurance', methods = ['POST'])
@cross_origin()
def get_health():
    if os.path.exists('yolov5/runs/detect/insurance_plans/'):

        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y_%m_%d_%H_%M_%S")

        shutil.move('yolov5/runs/detect/insurance_plans/', attemps_dir)
        # renaming 
        current_dir_path = 'attempts/insurance_plans'
        new_dir_path = 'attempts/insurance_plans' + '_' + formatted_datetime
        os.rename(current_dir_path, new_dir_path)

    if request.method == 'POST':
        ## -------------------- for base64 as input
        # data = request.get_json()
        # base64_string = data['data']
        # image_bytes = base64_to_image(base64_string)
        # img = create_image_from_bytes(image_bytes)
        # print("1")

        # now = datetime.datetime.now()
        # formatted_datetime = now.strftime("%Y_%m_%d_%H_%M_%S")
        
        # filename_1 = 'image_' + formatted_datetime + ".png"
  
        # img.save(os.path.join(uploads_dir, filename_1))
        # file_path = os.path.join(uploads_dir, filename_1)

        ## --------------- for file as input
        file = request.files["file"]

        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y_%m_%d_%H_%M_%S")

        filename = secure_filename(file.filename)

        file_name = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1]
        
        filename = 'image_' + formatted_datetime + file_extension

        file.save(os.path.join(uploads_dir, filename))
        file_path = os.path.join(uploads_dir, filename)



        print(f'################ file path = {file_path}')
        
        result = os.system(f'python yolov5/detect.py --weights best.pt --img 416 --conf 0.1 --source {file_path} --save-csv --name insurance_plans')
        term_file_path = 'yolov5/runs/detect/insurance_plans/predictions.csv'
        try : 
            lines_list = []
            with open(term_file_path, mode ='r') as file:
                csvFile = csv.reader(file)

                for lines in csvFile:
                    lines_list.append(lines)
            print(lines_list[0][1])

            label = lines_list[0][1]
            health_plan_bool = 0
            term_plan_bool = 0
            if label in health_plans:
                health_plan_bool = 1
                remaining_plans = get_health_plans(label)
            elif label in term_plans:
              term_plan_bool = 1
              remaining_plans = get_term_plans(label)
            else:
                remaining_plans = ['aditya_birla_digishield_plans','bajaj_alliance_life_etouch', 'hdfc_click2protect_super','icici_iprotect_smart', 'max_life_smart_secure_plus', 'aditya_birla_activ_health' , 'bajaj_alliance_health_guard', 'hdfc_ergo' , 'icici_lombard', 'tata_aig']

            output_json['logo'] = label
            output_json['error'] = "NA"
            output_json['recommendations'] = remaining_plans
            output_json['health_plan_bool'] = health_plan_bool
            output_json['term_plan_bool'] = term_plan_bool
            
        except : 
            print("no detections were made")
            output_json['logo'] = "NA"
            output_json['error'] = "no detections were made."
            output_json['recommendations'] = ['aditya_birla_digishield_plans','bajaj_alliance_life_etouch', 'hdfc_click2protect_super','icici_iprotect_smart', 'max_life_smart_secure_plus', 'aditya_birla_activ_health' , 'bajaj_alliance_health_guard', 'hdfc_ergo' , 'icici_lombard', 'tata_aig']
            
            
        finally : 
            shutil.move('yolov5/runs/detect/insurance_plans/', attemps_dir)

            # renaming 
            current_dir_path = 'attempts/insurance_plans'
            new_dir_path = 'attempts/insurance_plans' + '_' + formatted_datetime
            os.rename(current_dir_path, new_dir_path)
    return output_json

if __name__ == "__main__":
    app.run(debug=True)

'''
sample response : 

{
    "error": "NA",
    "logo": "bajaj_alliance_life_etouch",
    "recommendations": [
        "aditya_birla_digishield_plans",
        "hdfc_click2protect_super",
        "icici_iprotect_smart",
        "max_life_smart_secure_plus"
    ]
}


'''

