import json
from xml.dom.minidom import parse
import os
path = 'F:/voice/train/train/box/'
xml_list = os.listdir(path)
cat_names = set()
classes = {"holothurian": 0, "echinus": 1, "scallop": 2, "starfish": 3}
classes = {"cube": 0, "ball": 1, "cylinder": 2, "human body": 3,
           "tyre": 4, "circle cage": 5, "square cage": 6,
           "metal bucket": 7}
classes_name = ["holothurian", "echinus", "scallop", "starfish"]
classes_name = ["cube", "ball", "cylinder", "human body",
                "tyre", "circle cage", "square cage", "metal bucket"]


def read_xml(xml_path):
    doc = parse(xml_path)
    x_min = doc.getElementsByTagName('xmin')
    y_min = doc.getElementsByTagName('ymin')
    x_max = doc.getElementsByTagName('xmax')
    y_max = doc.getElementsByTagName('ymax')
    name = doc.getElementsByTagName('name')
    width = int(doc.getElementsByTagName('width')[0].firstChild.data)
    height = int(doc.getElementsByTagName('height')[0].firstChild.data)
    boxes = list()
    for i in range(len(name)):
        x1 = int(x_min[i].firstChild.data)
        y1 = int(y_min[i].firstChild.data)
        x2 = int(x_max[i].firstChild.data)
        y2 = int(y_max[i].firstChild.data)
        cat_name = name[i].firstChild.data
        boxes.append([x1, y1, x2-x1, y2-y1, cat_name])
        cat_names.add(cat_name)
    return boxes, width, height


train_coco = dict()
val_coco = dict()
cat_num = dict()
train_coco['images'] = list()
train_coco['annotations'] = list()
train_coco['categories'] = list()
val_coco['images'] = list()
val_coco['annotations'] = list()
val_coco['categories'] = list()
for c in classes:
    cat = dict()
    cat['supercategory'] = c
    cat['name'] = c
    cat['id'] = classes[c]
    train_coco['categories'].append(cat)
    val_coco['categories'].append(cat)
cnt = 0
train_image_index = 1
val_image_index = 1
train_annotation_index = 1
val_annotation_index = 1
for xml in xml_list:
    image_boxes, image_width, image_height = read_xml(path + xml)
    image = dict()
    image['height'] = image_height
    image['width'] = image_width
    image['file_name'] = xml.replace('.xml', '.jpg')
    if cnt < int(len(xml_list)*0.8):
        image['id'] = train_image_index
        for box in image_boxes:
            # if box[-1] == 'holothurian':
            #     # print(classes)
            #     print('ok')
            if box[-1] not in classes_name:
                continue
            if cat_num.get(box[-1]):
                cat_num[box[-1]] += 1
            else:
                cat_num[box[-1]] = 1
            annotation = dict()
            annotation['id'] = train_annotation_index
            annotation['image_id'] = train_image_index
            annotation['segmentation'] = []
            annotation['category_id'] = classes[box[-1]]
            annotation['bbox'] = box[:4]
            annotation['iscrowd'] = 0
            annotation['area'] = box[2] * box[3]
            train_coco['annotations'].append(annotation)
            train_annotation_index += 1
        train_coco['images'].append(image)
        train_image_index += 1
    else:
        image['id'] = val_image_index
        for box in image_boxes:
            if box[-1] not in classes_name:
                continue
            if cat_num.get(box[-1]):
                cat_num[box[-1]] += 1
            else:
                cat_num[box[-1]] = 1
            annotation = dict()
            annotation['id'] = val_annotation_index
            annotation['image_id'] = val_image_index
            annotation['segmentation'] = []
            annotation['category_id'] = classes[box[-1]]
            annotation['bbox'] = box[:4]
            annotation['iscrowd'] = 0
            annotation['area'] = box[2] * box[3]
            val_coco['annotations'].append(annotation)
            val_annotation_index += 1
        val_coco['images'].append(image)
        val_image_index += 1
    cnt += 1
for key in cat_num:
    print(key, cat_num[key])
print(cat_names)
with open('under_water_voice_train.json', 'w') as f:
    json.dump(train_coco, f, indent='\t')
with open('under_water_voice_val.json', 'w') as f:
    json.dump(val_coco, f, indent='\t')
