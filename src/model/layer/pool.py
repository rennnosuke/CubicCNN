# coding:utf-8

import numpy as np
from theano import config, tensor as T, shared

from filterlayer import FilterLayer, CubicLayer
from src.util.sequence import pair, trio

__author__ = 'ren'

POOL_MAX = 0
POOL_AVERAGE = 1


class PoolLayer2d(FilterLayer):
    def __init__(self, img_size, in_channel, k_size, stride=None, W=None, pad=0,
                 dtype=config.floatX, activation=lambda x: x, is_dropout=False,
                 cover_all=False, pool_type=POOL_MAX):

        # フィルタサイズ
        kw, kh = pair(k_size)

        # 実行するプーリングの種類
        self.pool_type = pool_type

        if stride is None:
            stride = k_size

        # フィルタベクトル
        if W is None:
            W = np.ones((in_channel, in_channel, kh, kw), dtype=dtype)
        self.W = shared(W, name='W', borrow=True)

        super(PoolLayer2d, self).__init__(img_size, in_channel, in_channel,
                                          k_size, stride, None, True, W,
                                          dtype, activation, cover_all,
                                          is_dropout)

    def update(self, cost, learning_rate=0.001):
        return None

    def output(self, inputs_symbol):
        if self.pool_type == POOL_MAX:
            output = self.max_pooling(inputs_symbol)
        elif self.pool_type == POOL_AVERAGE:
            output = self.averate_pooling(inputs_symbol)
        else:
            raise RuntimeError("pool_type is invalid.")

        z = self.activation(output)

        if self.is_dropout:
            if self.is_train:
                z *= self.srnd.binomial(size=z.shape, p=0.5)
            else:
                z *= self.dropout_rate

        return z

    def max_pooling(self, inputs_symbol):

        # データ数
        n = inputs_symbol.shape[0]

        # 一時的に4次元テンソルの形に
        inputs_4d = T.reshape(inputs_symbol,
                              (n, self.in_channel, self.img_h, self.img_w))

        # 畳み込み対象となる画素のみを抽出したテンソル
        col = self.im2col(inputs_4d)

        reshape_col = T.reshape(col, (
            n, self.in_channel, self.kh * self.kw, self.out_h, self.out_w))

        max_col = T.flatten(T.max(reshape_col, axis=2), outdim=2)

        return max_col


class PoolLayer3d(CubicLayer):
    def __init__(self, box_size, in_channel, k_size, stride=None, W=None, pad=0,
                 dtype=config.floatX, activation=lambda x: x, is_dropout=False,
                 cover_all=False, pool_type=POOL_MAX):

        # フィルタサイズ
        kx, ky, kz = trio(k_size)

        # 実行するプーリングの種類
        self.pool_type = pool_type

        if stride is None:
            stride = k_size

        # フィルタベクトル
        if W is None:
            W = np.ones((in_channel, in_channel, kz, ky, kx), dtype=dtype)
        self.W = shared(W, name='W', borrow=True)

        super(PoolLayer3d, self).__init__(box_size, in_channel, in_channel,
                                          k_size, stride, None, True, W,
                                          dtype, activation, cover_all,
                                          is_dropout)

    def update(self, cost, learning_rate=0.001):
        return None

    def output(self, inputs_symbol):
        if self.pool_type == POOL_MAX:
            output = self.max_pooling(inputs_symbol)
        elif self.pool_type == POOL_AVERAGE:
            output = self.averate_pooling(inputs_symbol)
        else:
            raise RuntimeError("pool_type is invalid.")

        z = self.activation(output)

        if self.is_dropout:
            if self.is_train:
                z *= self.srnd.binomial(size=z.shape, p=0.5)
            else:
                z *= self.dropout_rate

        return z

    def max_pooling(self, inputs_symbol):

        # データ数
        n = inputs_symbol.shape[0]

        # 一時的に4次元テンソルの形に
        inputs_5d = T.reshape(inputs_symbol,
                              (n, self.in_channel, self.box_z, self.box_y,
                               self.box_x))

        # 畳み込み対象となる画素のみを抽出したテンソル
        col = self.box2col(inputs_5d)

        reshape_col = T.reshape(col, (
            n, self.in_channel, self.kz * self.ky * self.kx, self.out_z,
            self.out_y, self.out_x))

        max_col = T.flatten(T.max(reshape_col, axis=2), outdim=2)

        return max_col
