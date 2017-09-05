#!/usr/bin/python

import json
import os.path as osp
import glob as gb
import PIL.Image

from labelme import utils


def our_labelme_shapes_to_label(img_shape, shapes):
    label_name_to_val = {'background': 0}
    lbl = np.zeros(img_shape[:2], dtype=np.int32)
    for shape in sorted(shapes, key=lambda x: x['label']):
        polygons = shape['points']
        label_name = shape['label']
        if label_name in label_name_to_val:
            label_value = label_name_to_val[label_name]
        else:
            label_value = int(label_name)
            label_name_to_val[label_name] = label_value
            # label_value = len(label_name_to_val)
            # label_name_to_val[label_name] = label_value
        mask = utils.polygons_to_mask(img_shape[:2], polygons)
        lbl[mask] = label_value

    lbl_names = [None] * (max(label_name_to_val.values()) + 1)
    for label_name, label_value in label_name_to_val.items():
        lbl_names[label_value] = label_name

    return lbl, lbl_names


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('src_path')
    parser.add_argument('target_path')
    args = parser.parser_args()
    pattern = '\*.json'

    for jpath in gb.glob(src_path + pattern):
        json_name = jpath.split('\\')[-1].split('.')[0]
        data = json.load(open(json))
        
        img = utils.img_b64_to_array(data['imageData'])
        lbl, lbl_names = our_labelme_shapes_to_label(img.shape, data['shapes'])

        PIL.Image.fromarray(lbl).save(osp.join(out_dir, json_name+'_label.png'))
        print('wrote  %s' % json_name)

    print('done...')



if __name__ == '__main__':
    main()
