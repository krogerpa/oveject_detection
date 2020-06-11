import os
from shutil import copyfile
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array

ORIGINAL_DATASET_PATH = 'Humanoide Roboter/images/original images/robot_ball_dataset-original'
DATASET_OUTPUT_PATH = 'Humanoide Roboter/images/current_dataset'
TEST_SPLIT = 0.2

train_datagen = ImageDataGenerator(
    validation_split = TEST_SPLIT
)

print("train dataset:")
train_generator = train_datagen.flow_from_directory(
    ORIGINAL_DATASET_PATH,
    class_mode = 'binary',
    subset = 'training'
)

print("validation dataset:")
test_generator = train_datagen.flow_from_directory(
    ORIGINAL_DATASET_PATH,
    class_mode = 'binary',
    subset = 'validation'
)

train_dataset_path = os.path.join(DATASET_OUTPUT_PATH, 'robot_ball_dataset')
test_dataset_path = os.path.join(DATASET_OUTPUT_PATH, 'test_dataset')

os.mkdir(train_dataset_path)
os.mkdir(os.path.join(train_dataset_path, 'ball'))
os.mkdir(os.path.join(train_dataset_path, 'robot'))
os.mkdir(test_dataset_path)
os.mkdir(os.path.join(test_dataset_path, 'ball'))
os.mkdir(os.path.join(test_dataset_path, 'robot'))

for image_filename in train_generator.filenames:
    src_path = os.path.join(ORIGINAL_DATASET_PATH, image_filename)
    tar_path = os.path.join(train_dataset_path, image_filename)
    copyfile(src_path, tar_path)

for image_filename in test_generator.filenames:
    src_path = os.path.join(ORIGINAL_DATASET_PATH, image_filename)
    tar_path = os.path.join(test_dataset_path, image_filename)
    copyfile(src_path, tar_path)