from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import scipy.cluster
import glob
import os

'''
change text and font_path
'''

text = "sampletext"
font_path = "font/hoge.ttf"


def kmeans_process(img, n_cluster=3):
    sm_img = img.resize((100, 100))
    color_arr = np.array(sm_img)
    w_size, h_size, n_color = color_arr.shape
    color_arr = color_arr.reshape(w_size * h_size, n_color)
    color_arr = color_arr.astype(np.float)
    codebook, distortion = scipy.cluster.vq.kmeans(color_arr, n_cluster)
    code, _ = scipy.cluster.vq.vq(color_arr, codebook)
    n_data = []
    for n in range(n_cluster):
        n_data.append(len([x for x in code if x == n]))
    desc_order = np.argsort(n_data)[::-1]
    return ["#{:02x}{:02x}{:02x}".format(*(codebook[elem].astype(int))) for elem in desc_order]

def draw_im_color(img, n_cluster=3):
    colors = kmeans_process(img)
    im_color_width = 400
    im_color_height = 20
    im_color = Image.new('RGB', (im_color_width, im_color_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im_color)
    single_width = im_color_width / n_cluster
    for i, color in enumerate(sorted(colors, reverse=True)):
        p1 = (single_width * i, 0)
        p2 = (single_width * (i + 1), im_color_height)
        pos = [p1, p2]
        draw.rectangle(pos, fill=color)
    return im_color

def draw_im_font(im_target, text, font_path=None):
    font_size = 60
    font_color = (255, 255, 255)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(im_target)
    draw.text((490, 800), text, font_color, font=font) # adjust the position of the text
    return im_target


files = glob.glob("input/*")
for input_filename in files:
    im_source = Image.open(input_filename)
    if im_source.width < im_source.height:
        im_source = im_source.rotate(90, expand=True)
    im_source = im_source.resize((960, 640), Image.LANCZOS)
    output_filename = "output/" + kmeans_process(im_source, n_cluster=1)[0][1:] + ".png"

    im_target = Image.new('RGB', (1080, 1080), (255, 255, 255, 255))
    im_target.paste(im_source, (60, 220))
    im_color = draw_im_color(im_source)
    im_target.paste(im_color, (340, 920))
    im_target = draw_im_font(im_target, text, font_path)

    im_target.save(output_filename)
    os.remove(input_filename)


