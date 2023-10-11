import obspython as obs
import os
from PIL import Image, ImageDraw, ImageFont
 
fainted = 0 


def script_description():
    return "Define you nuzlocke runs fainted pokemon."

def script_update(settings):
 
    global level_cap 
    level_cap = obs.obs_data_get_int(settings, "fainted")
 



def create_image(section : str,  text: str):
    img = Image.new('RGBA', (280, 100), (0, 0, 0, 0))

    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("font/impact.ttf", 50)
    except IOError:
        font = ImageFont.load_default()

    d.text((10,10), text, fill="white", stroke_width=2, stroke_fill="black", font=font)

    path = f'C:/nuzlocke-recordings'

    if not os.path.exists(path):
        obs.script_log(obs.LOG_INFO, "Creating a directory")
        os.makedirs(path)

    file = f'{path}/{section}.png'
    img.save(file, 'PNG')
    return file


def fainted_image(props, prop):

    obs.script_log(obs.LOG_INFO, f'Generate an image level cap of {str(level_cap)}')
    file = create_image("fainted_image",  f"FAINTED : {str(level_cap)}")
    
    if file != '':
        current_scene_source = obs.obs_frontend_get_current_scene()
        current_scene = obs.obs_scene_from_source(current_scene_source)

        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "file", file)

        image_source = obs.obs_source_create("image_source", 'fainted', settings, None)

        obs.obs_scene_add(current_scene, image_source)
        obs.obs_source_release(image_source)
        obs.obs_data_release(settings)
        obs.obs_source_release(current_scene_source)  



 
def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "fainted", "Cap", 0, 100, 1)
    obs.obs_properties_add_button(props, "btn_fainted", "Specify", fainted_image)
    return props


 


