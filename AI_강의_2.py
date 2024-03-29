# -*- coding: utf-8 -*-
"""AI_강의.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19KgXjv0ofOgMlZ19hkKybRN6bd9RfqbW
"""

#@title 구글 드라이브 연동

from google.colab import drive

drive.mount("/content/gdrive")

#@title 구글드라이브 파일 코랩에 가져오기

!gdown https://drive.google.com/uc?id=174pitX1IkwFkG3Hwek3o_-iOS2WY1g-4

#@title 가져온 파일 압축 풀기

!unzip dogs-vs-cats.zip

#@title 라이브러리 다운로드

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dropout, MaxPooling2D, Flatten, Dense
import os
import shutil
from keras import regularizers
from keras import optimizers
!pip install pydot
!brew install graphviz
from keras.utils import plot_model
import datetime
from tensorflow.keras.callbacks import TensorBoard

# 원본 데이터셋을 압축 해제한 디렉터리 경로
original_dataset_dir = '/content/train'

# 소규모 데이터셋을 저장할 디렉터리
base_dir = '/content/cats_and_dogs_small'
if os.path.exists(base_dir):  # 반복적인 실행을 위해 디렉토리를 삭제합니다.
    shutil.rmtree(base_dir)   # 이 코드는 책에 포함되어 있지 않습니다.
os.mkdir(base_dir)

# 원본 데이터셋을 압축 해제한 디렉터리 경로
original_dataset_dir = '/content/train'

# 소규모 데이터셋을 저장할 디렉터리
base_dir = '/content/cats_and_dogs_small'
if os.path.exists(base_dir):  # 반복적인 실행을 위해 디렉토리를 삭제합니다.
    shutil.rmtree(base_dir)   # 이 코드는 책에 포함되어 있지 않습니다.
os.mkdir(base_dir)

# 훈련, 검증, 테스트 분할을 위한 디렉터리
train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)
validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)
test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

# 훈련용 고양이 사진 디렉터리
train_cats_dir = os.path.join(train_dir, 'cats')
os.mkdir(train_cats_dir)

# 훈련용 강아지 사진 디렉터리
train_dogs_dir = os.path.join(train_dir, 'dogs')
os.mkdir(train_dogs_dir)

# 검증용 고양이 사진 디렉터리
validation_cats_dir = os.path.join(validation_dir, 'cats')
os.mkdir(validation_cats_dir)

# 검증용 강아지 사진 디렉터리
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
os.mkdir(validation_dogs_dir)

# 테스트용 고양이 사진 디렉터리
test_cats_dir = os.path.join(test_dir, 'cats')
os.mkdir(test_cats_dir)

# 테스트용 강아지 사진 디렉터리
test_dogs_dir = os.path.join(test_dir, 'dogs')
os.mkdir(test_dogs_dir)

# 처음 1,000개의 고양이 이미지를 train_cats_dir에 복사합니다
fnames = ['cat.{}.jpg'.format(i) for i in range(3000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_cats_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 고양이 이미지를 validation_cats_dir에 복사합니다
fnames = ['cat.{}.jpg'.format(i) for i in range(3001, 4501)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_cats_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 고양이 이미지를 test_cats_dir에 복사합니다
fnames = ['cat.{}.jpg'.format(i) for i in range(4502, 6002)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_cats_dir, fname)
    shutil.copyfile(src, dst)

# 처음 1,000개의 강아지 이미지를 train_dogs_dir에 복사합니다
fnames = ['dog.{}.jpg'.format(i) for i in range(3000)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(train_dogs_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 강아지 이미지를 validation_dogs_dir에 복사합니다
fnames = ['dog.{}.jpg'.format(i) for i in range(3001, 4501)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(validation_dogs_dir, fname)
    shutil.copyfile(src, dst)

# 다음 500개 강아지 이미지를 test_dogs_dir에 복사합니다
fnames = ['dog.{}.jpg'.format(i) for i in range(4502, 6002)]
for fname in fnames:
    src = os.path.join(original_dataset_dir, fname)
    dst = os.path.join(test_dogs_dir, fname)
    shutil.copyfile(src, dst)

base_dir = '/content/cats_and_dogs_small'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')

train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')
validation_cats_dir = os.path.join(validation_dir, 'cats')
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
test_cats_dir = os.path.join(test_dir, 'cats')
test_dogs_dir = os.path.join(test_dir, 'dogs')

print('훈련용 고양이 이미지 전체 개수:', len(os.listdir(train_cats_dir)))
print('훈련용 강아지 이미지 전체 개수:', len(os.listdir(train_dogs_dir)))
print('검증용 고양이 이미지 전체 개수: ', len(os.listdir(validation_cats_dir)))
print('검증용 강아지 이미지 전체 개수: ', len(os.listdir(validation_dogs_dir)))
print('테스트용 고양이 이미지 전체 개수: ', len(os.listdir(test_cats_dir)))
print('테스트용 강아지 이미지 전체 개수: ', len(os.listdir(test_dogs_dir)))

"""# 1차시 마지막."""

from PIL import Image

# 새로운 폴더 생성
new_directory = '/content/newcats_and_newdogs_small/test/new_cats'
os.makedirs(new_directory, exist_ok=True)
new_directory = '/content/newcats_and_newdogs_small/test/new_dogs'
os.makedirs(new_directory, exist_ok=True)
new_directory = '/content/newcats_and_newdogs_small/train/new_cats'
os.makedirs(new_directory, exist_ok=True)
new_directory = '/content/newcats_and_newdogs_small/train/new_dogs'
os.makedirs(new_directory, exist_ok=True)
new_directory = '/content/newcats_and_newdogs_small/validation/new_cats'
os.makedirs(new_directory, exist_ok=True)
new_directory = '/content/newcats_and_newdogs_small/validation/new_dogs'
os.makedirs(new_directory, exist_ok=True)

# 이미지가 있는 디렉토리 경로
directory = '/content/cats_and_dogs_small/test/dogs'

new_directory = '/content/newcats_and_newdogs_small/test/new_dogs'
os.makedirs(new_directory, exist_ok=True)

# 디렉토리 안의 모든 파일에 대해 반복
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # 이미지 파일 불러오기
        image_path = os.path.join(directory, filename)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_image(image, channels=3)  # 이미지 포맷에 따라 decode_image() 사용

        # 이미지 크기 조정
        resized_image = tf.image.resize(image, [244, 244])  # 새로운 높이와 너비 설정

        # 조정된 이미지를 파일로 저장
        resized_image_array = tf.cast(resized_image, tf.uint8)  # 이미지를 바이트 형식으로 변환
        resized_image_pil = Image.fromarray(resized_image_array.numpy())  # PIL 이미지로 변환

        # 새로운 파일 경로 설정
        new_filename = 'resized_' + filename
        new_image_path = os.path.join(new_directory, new_filename)

        # 조정된 이미지를 새로운 폴더에 저장
        resized_image_pil.save(new_image_path)

print("이미지 크기 조정 및 저장 완료")

# 이미지가 있는 디렉토리 경로
directory = '/content/cats_and_dogs_small/test/cats'

new_directory = '/content/newcats_and_newdogs_small/test/new_cats'
os.makedirs(new_directory, exist_ok=True)

# 디렉토리 안의 모든 파일에 대해 반복
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # 이미지 파일 불러오기
        image_path = os.path.join(directory, filename)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_image(image, channels=3)  # 이미지 포맷에 따라 decode_image() 사용

        # 이미지 크기 조정
        resized_image = tf.image.resize(image, [244, 244])  # 새로운 높이와 너비 설정

        # 조정된 이미지를 파일로 저장
        resized_image_array = tf.cast(resized_image, tf.uint8)  # 이미지를 바이트 형식으로 변환
        resized_image_pil = Image.fromarray(resized_image_array.numpy())  # PIL 이미지로 변환

        # 새로운 파일 경로 설정
        new_filename = 'resized_' + filename
        new_image_path = os.path.join(new_directory, new_filename)

        # 조정된 이미지를 새로운 폴더에 저장
        resized_image_pil.save(new_image_path)

print("이미지 크기 조정 및 저장 완료")

# 이미지가 있는 디렉토리 경로
directory = '/content/cats_and_dogs_small/train/dogs'

new_directory = '/content/newcats_and_newdogs_small/train/new_dogs'
os.makedirs(new_directory, exist_ok=True)

# 디렉토리 안의 모든 파일에 대해 반복
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # 이미지 파일 불러오기
        image_path = os.path.join(directory, filename)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_image(image, channels=3)  # 이미지 포맷에 따라 decode_image() 사용

        # 이미지 크기 조정
        resized_image = tf.image.resize(image, [244, 244])  # 새로운 높이와 너비 설정

        # 조정된 이미지를 파일로 저장
        resized_image_array = tf.cast(resized_image, tf.uint8)  # 이미지를 바이트 형식으로 변환
        resized_image_pil = Image.fromarray(resized_image_array.numpy())  # PIL 이미지로 변환

        # 새로운 파일 경로 설정
        new_filename = 'resized_' + filename
        new_image_path = os.path.join(new_directory, new_filename)

        # 조정된 이미지를 새로운 폴더에 저장
        resized_image_pil.save(new_image_path)

print("이미지 크기 조정 및 저장 완료")

# 이미지가 있는 디렉토리 경로
directory = '/content/cats_and_dogs_small/train/cats'

new_directory = '/content/newcats_and_newdogs_small/train/new_cats'
os.makedirs(new_directory, exist_ok=True)

# 디렉토리 안의 모든 파일에 대해 반복
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # 이미지 파일 불러오기
        image_path = os.path.join(directory, filename)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_image(image, channels=3)  # 이미지 포맷에 따라 decode_image() 사용

        # 이미지 크기 조정
        resized_image = tf.image.resize(image, [244, 244])  # 새로운 높이와 너비 설정

        # 조정된 이미지를 파일로 저장
        resized_image_array = tf.cast(resized_image, tf.uint8)  # 이미지를 바이트 형식으로 변환
        resized_image_pil = Image.fromarray(resized_image_array.numpy())  # PIL 이미지로 변환

        # 새로운 파일 경로 설정
        new_filename = 'resized_' + filename
        new_image_path = os.path.join(new_directory, new_filename)

        # 조정된 이미지를 새로운 폴더에 저장
        resized_image_pil.save(new_image_path)

print("이미지 크기 조정 및 저장 완료")

# 이미지가 있는 디렉토리 경로
directory = '/content/cats_and_dogs_small/validation/cats'

new_directory = '/content/newcats_and_newdogs_small/validation/new_cats'
os.makedirs(new_directory, exist_ok=True)

# 디렉토리 안의 모든 파일에 대해 반복
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # 이미지 파일 불러오기
        image_path = os.path.join(directory, filename)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_image(image, channels=3)  # 이미지 포맷에 따라 decode_image() 사용

        # 이미지 크기 조정
        resized_image = tf.image.resize(image, [244, 244])  # 새로운 높이와 너비 설정

        # 조정된 이미지를 파일로 저장
        resized_image_array = tf.cast(resized_image, tf.uint8)  # 이미지를 바이트 형식으로 변환
        resized_image_pil = Image.fromarray(resized_image_array.numpy())  # PIL 이미지로 변환

        # 새로운 파일 경로 설정
        new_filename = 'resized_' + filename
        new_image_path = os.path.join(new_directory, new_filename)

        # 조정된 이미지를 새로운 폴더에 저장
        resized_image_pil.save(new_image_path)

print("이미지 크기 조정 및 저장 완료")

# 이미지가 있는 디렉토리 경로
directory = '/content/cats_and_dogs_small/validation/dogs'

new_directory = '/content/newcats_and_newdogs_small/validation/new_dogs'
os.makedirs(new_directory, exist_ok=True)

# 디렉토리 안의 모든 파일에 대해 반복
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # 이미지 파일 불러오기
        image_path = os.path.join(directory, filename)
        image = tf.io.read_file(image_path)
        image = tf.image.decode_image(image, channels=3)  # 이미지 포맷에 따라 decode_image() 사용

        # 이미지 크기 조정
        resized_image = tf.image.resize(image, [244, 244])  # 새로운 높이와 너비 설정

        # 조정된 이미지를 파일로 저장
        resized_image_array = tf.cast(resized_image, tf.uint8)  # 이미지를 바이트 형식으로 변환
        resized_image_pil = Image.fromarray(resized_image_array.numpy())  # PIL 이미지로 변환

        # 새로운 파일 경로 설정
        new_filename = 'resized_' + filename
        new_image_path = os.path.join(new_directory, new_filename)

        # 조정된 이미지를 새로운 폴더에 저장
        resized_image_pil.save(new_image_path)

print("이미지 크기 조정 및 저장 완료")

#@title 이미지 파일 경로 설정

train_dir = '/content/newcats_and_newdogs_small/train'
validation_dir = '/content/newcats_and_newdogs_small/validation'
test_dir = '/content/newcats_and_newdogs_small/test'

from PIL import Image

# 이미지 파일 경로
image_path = "/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg"

# 이미지 열기
image = Image.open(image_path)

# 이미지 크기 확인
width, height = image.size
print("이미지의 너비:", width)
print("이미지의 높이:", height)

#@title 이미지 파일 전처리 옵션 설정
#흑백 장점 컴퓨터의 학습 속도 증가, 불필요 정보 제거.일반화 성능 향상
#흑백 단점 컬러 정보 손실, 시각적 정보 제한, 다양성 감소


train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=20,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest'
                                   )

test_datagen = ImageDataGenerator(rescale=1./255)

validation_datagen = ImageDataGenerator(rescale=1./255)

#@title 이미지 파일 불러오기

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(150, 150),
                                                    batch_size=32,
                                                    class_mode='binary')

test_generator = test_datagen.flow_from_directory(test_dir,
                                                  target_size=(150, 150),
                                                  batch_size=32,
                                                  class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                              target_size=(150, 150),
                                                              batch_size=32,
                                                              class_mode='binary')

import tensorflow as tf

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = tf.io.read_file(image_path)
image = tf.image.decode_image(image, channels=3)  # 이미지를 RGB로 디코딩

# 이미지 색상 변경
# 예를 들어, 그레이스케일로 변환
grayscale_image = tf.image.rgb_to_grayscale(image)

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 이미지의 색상을 그레이스케일로 변환한 후에 저장하는 예제입니다.
output_image_path = 'output_image.jpg'
tf.io.write_file(output_image_path, tf.image.encode_jpeg(grayscale_image))

import tensorflow as tf

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = tf.io.read_file(image_path)
image = tf.image.decode_image(image, channels=1)  # 이미지를 그레이스케일로 디코딩

# 임계값(threshold) 설정
threshold = 127  # 임계값은 일반적으로 0과 255 사이의 값으로 설정됩니다.

# 이미지 이진화
binary_image = tf.cast(tf.where(image < threshold, 0, 255), tf.uint8)  # uint8로 변환

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 이미지를 이진화한 후에 저장하는 예제입니다.
output_image_path = 'binary_image.jpg'
tf.io.write_file(output_image_path, tf.image.encode_jpeg(binary_image))

import tensorflow as tf

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = tf.io.read_file(image_path)
image = tf.image.decode_image(image, channels=3)  # 이미지를 RGB로 디코딩

# 세피아 톤 행렬
sepia_matrix = tf.constant([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])

# 이미지 색상 변경 - 세피아 효과
def apply_sepia_tone(image):
    # 이미지를 float32로 변환
    image_float = tf.cast(image, tf.float32)
    # 세피아 효과 적용
    sepia_image = tf.matmul(image_float, sepia_matrix)
    # 픽셀 값을 0과 255 사이로 클리핑
    sepia_image = tf.clip_by_value(sepia_image, 0, 255)
    # float32를 uint8로 변환
    sepia_image = tf.cast(sepia_image, tf.uint8)
    return sepia_image

# 세피아 효과 적용
sepia_image = apply_sepia_tone(image)

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 이미지에 세피아 효과를 적용한 후에 저장하는 예제입니다.
output_image_path = 'sepia_image.jpg'
tf.io.write_file(output_image_path, tf.image.encode_jpeg(sepia_image))

import cv2

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 이미지를 흑백으로 로드합니다.

# 컬러 맵 적용
color_map = cv2.applyColorMap(image, cv2.COLORMAP_JET)  # 적용할 컬러 맵을 선택합니다.

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 컬러 맵을 적용한 후에 저장하는 예제입니다.
output_image_path = 'color_image.jpg'
cv2.imwrite(output_image_path, color_map)

import cv2
import numpy as np

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = cv2.imread(image_path)

# 이미지를 HSV 색상 공간으로 변환
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 노란색 범위 설정 (HSV 색상 공간에서)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# 노란색 마스크 생성
yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# 이미지에서 노란색 부분 강조
highlighted_image = cv2.bitwise_and(image, image, mask=yellow_mask)

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 노란색을 강조한 이미지를 저장하는 예제입니다.
output_image_path = 'highlighted_image.jpg'
cv2.imwrite(output_image_path, highlighted_image)

import cv2

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = cv2.imread(image_path)

# 이미지의 채널 스왑 (RGB -> BGR)
swapped_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 채널 스왑된 이미지를 저장하는 예제입니다.
output_image_path = 'swapped_image.jpg'
cv2.imwrite(output_image_path, swapped_image)

import cv2
import numpy as np

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = cv2.imread(image_path)

# 채도 조정
s = 50  # 채도 조정 계수 (1보다 크면 높아지고, 1보다 작으면 낮아집니다.)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 이미지를 HSV 색상 공간으로 변환
hsv[:, :, 1] = np.clip(hsv[:, :, 1] * s, 0, 255)  # 채도 조정
saturated_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)  # 다시 BGR 색상 공간으로 변환

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 채도가 조정된 이미지를 저장하는 예제입니다.
output_image_path = 'saturated_image.jpg'
cv2.imwrite(output_image_path, saturated_image)

import cv2

# 이미지 로드
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = cv2.imread(image_path)

# 이미지 크기에 따라 가우시안 블러의 커널 크기 계산
height, width, _ = image.shape
kernel_size = max(244, 244) // 20  # 이미지의 크기에 따라 조절할 수 있습니다.
kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1  # 커널 크기를 홀수로 만듭니다.

# 가우시안 블러 적용
blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

# 변경된 이미지를 저장하거나 화면에 표시하는 등의 후속 작업을 수행할 수 있습니다.
# 이 코드는 노이즈가 제거된 이미지를 저장하는 예제입니다.
output_image_path = 'denoised_image.jpg'
cv2.imwrite(output_image_path, blurred_image)

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# 이미지 불러오기
image_path = '/content/newcats_and_newdogs_small/train/new_cats/resized_cat.0.jpg'
image = cv2.imread(image_path)

# 이미지를 그레이스케일로 변환
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이진화를 사용하여 누끼를 분리
ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 누끼의 외곽선 찾기
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 누끼 그리기
mask = np.zeros_like(image)
cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

# 원본 이미지에서 누끼 제거
result = cv2.bitwise_and(image, mask)

# 결과 이미지 출력
cv2_imshow(result)

#@title 전처리된 사진 보기

img, label = next(train_generator)
plt.figure(figsize=(20, 20))

for i in range(8):
    plt.subplot(3, 3, i+1)
    plt.imshow(img[i])
    plt.title(label[i])
    plt.axis('off')

plt.show()

"""2차시 끝"""

#@title 모델 구성

model = models.Sequential()

Conv2D(1, (2, 2), padding='same', input_shape=(150, 150, 3))
model.add(layers.Conv2D(512, (2, 2), activation='sigmoid')) #512 = 레이어의 수 12,12= 가져올 이미지의 범위


model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2))) #2,2 뽑아갈 이미지의 범위 max 폴링 이미지 픽셀의 최댓값을 가져감
model.add(layers.Conv2D(256, (4, 4), activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(256, (4, 4), activation='relu' ))


model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (6, 6), activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.Conv2D(64, (2, 2), activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.Flatten())


model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.3)) #0.3 노드를 삭제할 비율
model.add(layers.Dense(512, activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.3))



model.add(layers.Dense(1, activation='sigmoid'))



#@title 생성 모델 시각화 하기

model = models.Sequential()


model.add(layers.BatchNormalization(input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(512, (2, 2), activation='sigmoid')) #512 = 레이어의 수 12,12= 가져올 이미지의 범위


model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2))) #2,2 뽑아갈 이미지의 범위 max 폴링 이미지 픽셀의 최댓값을 가져감
model.add(layers.Conv2D(256, (4, 4), activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(256, (4, 4), activation='relu' ))


model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (6, 6), activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.Conv2D(64, (2, 2), activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.Flatten())


model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.3)) #0.3 노드를 삭제할 비율
model.add(layers.Dense(512, activation='relu'))


model.add(layers.BatchNormalization())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.3))



model.add(layers.Dense(1, activation='sigmoid'))

plot_model(model, to_file='model.png')
plot_model(model, to_file='model_shapes.png', show_shapes=True)

#@title 모델 컴파일


model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])

# 로그 디렉토리 설정
log_dir = "/content/AImodel"

# TensorBoard 콜백 설정
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

#@title 모델 학습
#loss 손실: 오차 낮을수록 좋음
#acc 정확도: 높을 수록 좋음

history = model.fit_generator(
      train_generator,
      steps_per_epoch=100,
      epochs=200,
      validation_data=validation_generator,
      validation_steps=50,
      callbacks=[tensorboard_callback]
      )

#@title 평가 데이터를 사용해 실제 정확도 측정

test_loss, test_acc = model.evaluate(test_generator, steps=100)
print('test acc:', test_acc)

#@title 만들어진 모델 저장

tf.saved_model.save(model, "/content/AImodel")

#@title 저장된 모델 불러오기

model = tf.saved_model.load('/content/AImodel')

log_dir = "/content/AImodel" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir {log_dir}

!mkdir models

