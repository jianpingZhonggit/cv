import json
import matplotlib.pyplot as plt
import math
import numpy as np
# train = json.load(open('./under_water_voice_train_all.json'))
train = json.load(open('./under_water_train_all.json'))
# 分析每张图片中大、中、小目标分布
image_annotation = dict()
for image in train['images']:
    image_annotation[image['id']] = []
for annotation in train['annotations']:
    image_annotation[annotation['image_id']].append(annotation['bbox'])
image_small = 0
image_medium = 0
image_large = 0
small = 0
medium = 0
large = 0
objects_per_image = dict()
for image in image_annotation:
    boxes = image_annotation[image]
    small_flag = False
    medium_flag = False
    large_flag = False
    if objects_per_image.get(len(boxes)):
        objects_per_image[len(boxes)] += 1
    else:
        objects_per_image[len(boxes)] = 1
    for box in boxes:
        if box[2] * box[3] < 32 * 32:
            small += 1
            small_flag = True
        elif 32 * 32 < box[2] * box[3] < 96 * 96:
            medium += 1
            medium_flag = True
        else:
            large += 1
            large_flag = True
    if small_flag:
        image_small += 1
    if medium_flag:
        image_medium += 1
    if large_flag:
        image_large += 1
print(objects_per_image.keys())
count = []
for key in objects_per_image:
    count.append(key)
plt.bar(range(len(objects_per_image)), objects_per_image.values(), tick_label=count)
plt.show()
plt.pie([small, medium, large], labels=['small', 'medium', 'large'], autopct='%1.1f%%')
plt.show()
plt.pie([image_small, image_medium, image_large],  labels=['small', 'medium', 'large'], autopct='%1.1f%%')
plt.show()
exit(0)
w, h, area = [], [], []
cnt = 0
cat = dict()
classes = ["holothurian", "echinus", "scallop", "starfish"]
# classes_name = ["cube", "ball", "cylinder", "human body",
#                 "tyre", "circle cage", "square cage", "metal bucket"]
image_width = list()
image_height = list()
w_h = dict()
for image in train['images']:
    if w_h.get(image['width']):
        continue
    else:
        w_h[image['width']] = image['height']
print('width \t height')
# for key in w_h:
#     print(key, w_h[key], 1333/(key/w_h[key]))
# # print(image_width)
# # print(image_height)
# exit(0)
small = 0
medium = 0
large = 0
for annotation in train['annotations']:
    w.append(annotation['bbox'][2])
    h.append(annotation['bbox'][3])
    # print(annotation['bbox'])
    if w[cnt] * h[cnt] < 32 * 32:
        small += 1
    elif 32 * 32 < w[cnt] * h[cnt] < 96 * 96:
        medium += 1
    else:
        large += 1
    if cat.get(annotation['category_id']):
        cat[annotation['category_id']] += 1
    else:
        cat[annotation['category_id']] = 1
    area.append(math.sqrt(np.abs(w[cnt]*h[cnt])))
    cnt += 1
area = sorted(area)
print(f'area min:{area[0]}')
print(f'area max:{area[-1]}')
print(f'area mean:{np.mean(np.array(area))}')
print(f'area std:{np.std(np.array(area))}')
# plt.plot(range(len(area)), area)
# plt.show()
height = []
for key in cat:
    height.append(cat[key])
print(height)
classes = ("holothurian", "echinus", "scallop", "starfish", 'samll', 'miedum', 'large')
# classes = ("cube", "ball", "cylinder", "human body",
#            "tyre", "circle cage", "square cage", "metal bucket")
plt.bar(range(len(classes)), height+[small, medium, large], tick_label=classes)
plt.show()

