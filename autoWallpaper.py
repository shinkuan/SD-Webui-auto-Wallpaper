import io
import os
import json
import time
import ctypes
import base64
import requests
import subprocess
from PIL import Image, PngImagePlugin

# Run SD
directory = os.getcwd()
os.chdir("S:\\stable-diffusion-webui-1.4.0")
p = subprocess.Popen("webui-user.bat")
time.sleep(15)
os.chdir(directory)

# SD API
url = "http://127.0.0.1:7860"
payload = {
    "enable_hr": True,
    "denoising_strength": 0.55,
    "firstphase_width": 1280,
    "firstphase_height": 720,
    "hr_scale": 2,
    "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
    "hr_second_pass_steps": 12,
    "hr_resize_x": 2560,
    "hr_resize_y": 1440,
    "hr_sampler_name": "",
    "hr_prompt": "",
    "hr_negative_prompt": "",
    "prompt": "(4k wallpaper, absurdres, fantastic scenery, detailed background, 1girl), __tt-all__",
    "styles": [],
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 40,
    "cfg_scale": 6,
    "width": 1280,
    "height": 720,
    "restore_faces": False,
    "tiling": False,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "negative_prompt": "((worst quality, low quality:1.4), lowres, (monochrome:1.1), blurry, jpeg artifacts, pubic hair, muscular, hairy, (fat:1.0), (cross-section:1.1), (multiple views:1.2):0.8), easynegative, verybadimagenegative_v1.3, ng_deepnegative_v1_75t, nsfw, nude, topless",
    "eta": 0,
    "s_min_uncond": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 1,
    "override_settings": {"CLIP_stop_at_last_layers": 2, "eta_noise_seed_delta": 31337},
    "override_settings_restore_afterwards": True,
    "script_args": [],
    "sampler_index": "DPM++ 2M Karras",
    "script_name": "",
    "send_images": True,
    "save_images": False,
    "alwayson_scripts": {},
}

# Make sure SD is opened
while requests.get(url=f"{url}/user/").status_code != 200:
	time.sleep(1)
	pass

# Inference
response = requests.post(url=f"{url}/sdapi/v1/txt2img", json=payload)
r = response.json()

# Terminate SD
requests.post(url=f"{url}/_stop/")
p.terminate()

# Load Image to wallpaper
for i in r["images"]:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

    png_payload = {"image": "data:image/png;base64," + i}
    response2 = requests.post(url=f"{url}/sdapi/v1/png-info", json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save("output.png", pnginfo=pnginfo)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, directory+"\\output.png", 0)
