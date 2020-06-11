import os

from AIBallAnnotationParser import *
from PIL import Image

dir_path = 'Humanoide Roboter/images/original images/bit-bots/'

sub_dir_list = os.listdir(dir_path)

for i, sub_dir_name in enumerate(sub_dir_list):
    sub_dir_path = os.path.join(dir_path, sub_dir_name)

    if not os.path.isdir(sub_dir_path):
        continue

    parser = AIBallAnnotationParser(sub_dir_path)
    annotations = parser.read_ai_ball_file()
    print('subdir: "{}" label: "{}" found {} annotations: {}'.format(sub_dir_name, i, len(annotations), annotations))

    cropped_folder_name = '{}_cropped'.format(sub_dir_name)
    cropped_folder_path = os.path.join(dir_path, cropped_folder_name)

    if not os.path.exists(cropped_folder_path):
        os.mkdir(cropped_folder_path)

    image_names = os.listdir(sub_dir_path)

    for image_path in image_names:
        path = os.path.join(sub_dir_path, image_path)

        if os.path.splitext(path)[1] == '.txt' or image_path == '.DS_Store':
            continue

        image = Image.open(path).convert('L')

        try:
            annotation = annotations[image_path]
        except:
            print('{} - no entry found in annotation file for: {}'.format(sub_dir_name, image_path))
            continue
        if len(annotation) == 1:
            print('skip image: {}', image_path)
            continue

        crop_area = (int(annotation['x1']), int(annotation['y1']), int(annotation['x2']), int(annotation['y2']))
        cropped_img = image.crop(crop_area)

        img_name_splitted = os.path.splitext(image_path)
        cropped_img_name = '{}_{}_cropped.{}'.format(sub_dir_name, img_name_splitted[0], img_name_splitted[1])
        cropped_img_path = os.path.join(cropped_folder_path, cropped_img_name)
        cropped_img.save(cropped_img_path)
