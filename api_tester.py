import json
import requests
from PIL import Image, PngImagePlugin
from pathlib import Path
import base64
import io
#import torch
import pandas as pd


BASE_URL = "http://127.0.0.1:7860"
MAX_IMAGES = 1
OUTPUT_DIRECTORY = "outputs"

def load_payload():
    with open('payload.json') as f:
        payload = json.load(f)
    return payload

def generate_images(base_url, payload, image_number, output_directory, image_name_format):
    try:
        response = requests.post(f'{base_url}/sdapi/v1/txt2img', json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return
    r = response.json()

    print(r)  # Print the response JSON for debugging purposes

    # Check if the response structure is different than expected
    if 'images' not in r:
        print("Response structure is different. Check the response JSON.")
        return

    # Create the output directory if it doesn't exist
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    for i in r['images']:
        try:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(f'{base_url}/sdapi/v1/png-info', json=png_payload)
            response2.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            continue

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image_path = Path(output_directory) / image_name_format.format(image_number+1)
        image.save(image_path, pnginfo=pnginfo)
        #torch.cuda.empty_cache()

# Load the CSV file into a DataFrame
df = pd.read_csv('inputs.csv')

for index, row in df.iterrows():
    payload = load_payload()

    IMAGE_NAME_FORMAT = row['Test Name'] + ".png"
    input_text = row['prompt']
    input_negative_text = row['negative prompt']
    sampler = row['sampler']
    steps = row['steps']
    script_name = "x/y/z plot"
    checkpoints = [checkpoint.strip() for checkpoint in row['checkpoints'].split(',')]

    # Remove trailing single quotation mark from the last checkpoint string
    last_checkpoint = checkpoints[-1]
    if last_checkpoint.endswith("'"):
        checkpoints[-1] = last_checkpoint[:-1]

    x_type = 1
    x_values = row['seeds']
    x_values_dropdown = 0
    y_type = 10
    y_values = "'" + "','".join(checkpoints) + "'"
    y_values_dropdown = checkpoints
    z_type = 6
    z_values = row['cfg values']
    z_values_dropdown = 0
    draw_legend = True
    include_lone_images = False
    include_sub_grids = False
    no_fixed_seeds = False
    margin_size = 0

    script_args = [
        x_type,
        x_values,
        x_values_dropdown,
        y_type,
        y_values,
        y_values_dropdown,
        z_type,
        z_values,
        z_values_dropdown,
        draw_legend,
        include_lone_images,
        include_sub_grids,
        no_fixed_seeds,
        margin_size
    ]

    payload["prompt"] = input_text
    payload["negative_prompt"] = input_negative_text
    payload["sampler_index"] = sampler
    payload["steps"] = steps
    payload["script_name"] = script_name
    payload["script_args"] = script_args

    for j in range(MAX_IMAGES):
        generate_images(BASE_URL, payload, j, OUTPUT_DIRECTORY, IMAGE_NAME_FORMAT)