from src.util.shape import *
from src.helper.data3d import psb_binvox, psb_binvoxs
from src.helper.visualize import plot_voxel

__author__ = 'ren'


def test_rotate_voxel():
    boxel = psb_binvox(0)
    r_x = (45, 0, 0)
    r_y = (0, 45, 0)
    r_z = (0, 0, 45)
    plot_voxel(rotate_voxel(boxel, r_x))
    plot_voxel(rotate_voxel(boxel, r_y))
    plot_voxel(rotate_voxel(boxel, r_z))

def test_trans_voxel():
    boxel = psb_binvox(0)
    t_x = (10, 0, 0)
    t_y = (0, 40, 0)
    t_z = (0, 0, 70)
    plot_voxel(trans_voxel(boxel, t_x))
    plot_voxel(trans_voxel(boxel, t_y))
    plot_voxel(trans_voxel(boxel, t_z))

def test_centerize_voxels():
    ids = [0, 1, 2, 3]
    x_train, x_test, y_train, y_test = psb_binvoxs(ids)
    c_binvoxs = centerize_voxels(np.array(x_test), center=(50, 50, 50))
    for b in c_binvoxs:
        plot_voxel(b)
