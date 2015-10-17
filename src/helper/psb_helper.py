# coding:utf-8

import os
import itertools
import numpy as np
from theano import config
from src.util.config import path_res_3d_psb, path_res_3d_psb_classifier, \
    path_res_numpy_psb

__author__ = 'ren'


class PSB(object):
    @classmethod
    def load_class_infos(cls, train_name="train.cla", test_name="test.cla"):
        return cls.load_class_info(train_name), cls.load_class_info(test_name)

    @staticmethod
    def load_class_info(f_name, dir=path_res_3d_psb_classifier):

        classifier = {}

        with file(dir + "/" + f_name) as f:

            line = f.readline()

            if "PSB" not in line:
                raise IOError("PSB class file must be \"cls\" format file.")
            else:
                n_class, n_model = map(int, f.readline().split(" "))

            while line:

                line = f.readline()

                if line == "\n":
                    continue

                s_line = line.split(" ")

                if len(s_line) == 3:
                    main_name, sub_name, n_id = s_line
                    n_id = int(n_id)

                    if n_id > 0:
                        ids = [int(f.readline()) for i in range(n_id)]
                        prefix = "" if sub_name == "0" else sub_name + "/"
                        classifier.setdefault(prefix + main_name, ids)

        return classifier

    @classmethod
    def load_vertices_all(cls, dir=path_res_3d_psb):
        train_vertices = []
        test_vertices = []
        train_answers = []
        test_answers = []

        train_classes, test_classes = cls.load_class_infos()
        classes = dict(train_classes, **test_classes)

        train_members = list(itertools.chain(*train_classes.values()))
        test_members = list(itertools.chain(*test_classes.values()))

        for f in os.listdir(dir):

            if not os.path.isfile(dir + "/" + f):
                continue

            id = int(f.split(".")[0])

            if id in test_members:
                v_list = test_vertices
                a_list = test_answers
            elif id in train_members:
                v_list = train_vertices
                a_list = train_answers

            # データの格納
            v_list.append(cls.load_vertices(f, dir))

            # 正解ラベルの探索と格納
            keys = classes.keys()
            for key in keys:
                if id in classes.get(key):
                    a_list.append(keys.index(key))
                    break

        return train_vertices, test_vertices, train_answers, test_answers

    @staticmethod
    def load_vertices(f_name, dir=path_res_3d_psb, is_saved=True):

        # saved numpy array
        path_np = path_res_numpy_psb + "/" + f_name + ".npy"
        if os.path.exists(path_np):
            return np.load(path_np)

        with file(dir + "/" + f_name) as f:

            lines = f.readlines()

            # 一行目はファイルフォーマット名
            if "OFF" not in lines[0]:
                raise IOError("psb file must be \"off\" format file.")
            else:
                # 二行目は頂点数、面数、エッジ数
                n_ver, n_faces, n_edges = map(int, lines[1].split(" "))

            # 三行目以降の頂点座標情報のみ取得
            vertices = np.array(
                [map(float, line.split(" ")) for line in lines[2:n_ver]])

            if is_saved:
                np.save(path_np, vertices)

        return vertices

    @staticmethod
    def standard(points):
        mean = np.mean(points, axis=0)
        norm = np.max(points) - np.min(points)
        return np.array([(p - mean) / norm for p in points],
                        dtype=config.floatX)

    @classmethod
    def boxel(cls, points, n_div=100):
        # -0.5~0.5
        points = cls.standard(points)
        boxel = np.zeros(shape=(n_div, n_div, n_div), dtype=config.floatX)
        for p in points:
            x, y, z = p
            bz = int(z * n_div + n_div) / 2
            by = int(y * n_div + n_div) / 2
            bx = int(x * n_div + n_div) / 2
            boxel[bz][by][bx] = 1
        return boxel

    @classmethod
    def boxel_all(cls, points_list, n_div=100):
        return np.array([cls.boxel(points, n_div) for points in points_list],
                        dtype=config.floatX)
