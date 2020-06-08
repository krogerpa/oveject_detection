import os

import numpy as np
from AIBallAnnotationParser import *
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow import keras

dimen = 32

dir_path = input('Enter images directory path : ')
output_path = input('Enter output directory path : ')

sub_dir_list = os.listdir(dir_path)
images = list()
labels = list()
for i, sub_dir_name in enumerate(sub_dir_list):
    label = i
    sub_dir_path = os.path.join(dir_path, sub_dir_name)

    if not os.path.isdir(sub_dir_path):
        continue

    parser = AIBallAnnotationParser(sub_dir_path)
    annotations = parser.read_ai_ball_file()
    print('subdir: "{}" label: "{}" found {} annotations: {}'.format(sub_dir_name, i, len(annotations), annotations))

    image_names = os.listdir(sub_dir_path)
    for image_path in image_names:
        path = os.path.join(sub_dir_path, image_path)

        if os.path.splitext(path)[1] == '.txt' or image_path == '.DS_Store':
            continue

        image = Image.open(path).convert('L')

        annotation = annotations[image_path]
        if len(annotation) == 1:
            print('skip image: {}', image_path)
            continue
        crop_area = (int(annotation['x1']), int(annotation['y1']), int(annotation['x2']), int(annotation['y2']))
        cropped_img = image.crop(crop_area)

        resize_image = cropped_img.resize((dimen, dimen))

        # image.show()
        # cropped_img.show()
        # resize_image.show()
        # exit(9)

        array = list()
        for x in range(dimen):
            sub_array = list()
            for y in range(dimen):
                sub_array.append(resize_image.load()[x, y])
            array.append(sub_array)
        image_data = np.array(array)
        image = np.array(np.reshape(image_data, (dimen, dimen, 1))) / 255
        images.append(image)
        labels.append(label)

x = np.array(images)
y = np.array(keras.utils.to_categorical(np.array(labels), num_classes=len(sub_dir_list)))

train_features, test_features, train_labels, test_labels = train_test_split(x, y, test_size=0.4)

np.save('{}x.npy'.format(output_path), train_features)
np.save('{}y.npy'.format(output_path), train_labels)
np.save('{}test_x.npy'.format(output_path), test_features)
np.save('{}test_y.npy'.format(output_path), test_labels)
