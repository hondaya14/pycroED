import re
import numpy as np
import subprocess
from .util import *


# pick up Fcalc at Fobs index; h, k, l
# Fobs(h,k,l)
#   ↓
# h,k,l   ->   Fcalc(h,k,l)
def pick_up_hkl(fobs_file_name, fcalc_file_name):
    if file_exist(fcalc_file_name + '_all.hkl') and file_exist(fcalc_file_name + '_gt.hkl'): return
    print('pick up hkl...')
    fobs_file = fobs_file_name
    fcalc_file = fcalc_file_name + '.ampascii'

    result = subprocess.run(['mrcInfo', '-i', fcalc_file_name + '.mrc'], stdout=subprocess.PIPE).stdout.decode()
    lines = result.split('\n')
    mrc_size_list = list(map(int, (re.sub(r"[(N:) ]", "", lines[0])).split(',')))
    mrc_unit_length_list = list(map(float, (re.sub(r"[(Length:) ]", "", lines[4])).split(',')))

    # mrc size
    mrc_size_x, mrc_size_y, mrc_size_z = mrc_size_list[0], mrc_size_list[1], mrc_size_list[2]

    # voxel length
    mrc_unit_length = mrc_unit_length_list[0]

    center = [int(mrc_size_x / 2), int(mrc_size_y / 2), int(mrc_size_z / 2)]

    # read voxel data
    voxel_data = [[[0] * mrc_size_z for i in range(mrc_size_y)] for j in range(mrc_size_x)]

    with open(fcalc_file, mode='r') as vf:
        vl = vf.readlines()
        for line in vl:
            try:
                x, y, z, v = map(float, line.split())
                # x, y, z を ボクセルの整数座標に変換
                x = round(x / mrc_unit_length)
                y = round(y / mrc_unit_length)
                z = round(z / mrc_unit_length)

                # 逆空間(Å^-1)に変換
                # x = (x - cutoff_mrc_size_x / 2) / (cutoff_mrc_size_x * mrc_unit_length)
                # y = (y - cutoff_mrc_size_y / 2) / (cutoff_mrc_size_y * mrc_unit_length)
                # z = (z - cutoff_mrc_size_z / 2) / (cutoff_mrc_size_z * mrc_unit_length)
                # # print('\t{0}\t{1}\t{2}\t{3}'.format(x, y, z, v))
                # voxel_data.append([x, y, z, v])
                try:
                    voxel_data[x][y][z] = v
                except IndexError:
                    continue

            except EOFError:
                break

    # フーリエボクセル1個の幅
    voxel_unit_length_x = 1 / (mrc_size_x * mrc_unit_length)
    voxel_unit_length_y = 1 / (mrc_size_y * mrc_unit_length)
    voxel_unit_length_z = 1 / (mrc_size_z * mrc_unit_length)

    # unit cell parameters
    unit_cell_tv_x = [7.1178, 0, 0]
    unit_cell_tv_y = [0, 9.6265, 0]
    unit_cell_tv_z = [-1.39567, 0, 11.81314]

    unit_cell_tv = np.array([
        unit_cell_tv_x,
        unit_cell_tv_y,
        unit_cell_tv_z
    ])

    # unit cell volume
    unit_cell_volume = np.dot(np.cross(unit_cell_tv_x, unit_cell_tv_y), unit_cell_tv_z)

    reciprocal_lattice_vector_a = np.cross(unit_cell_tv_y, unit_cell_tv_z) / unit_cell_volume
    reciprocal_lattice_vector_b = np.cross(unit_cell_tv_z, unit_cell_tv_x) / unit_cell_volume
    reciprocal_lattice_vector_c = np.cross(unit_cell_tv_x, unit_cell_tv_y) / unit_cell_volume

    # reciprocal_lattice_vector = np.array([
    #     reciprocal_lattice_vector_a,
    #     reciprocal_lattice_vector_b,
    #     reciprocal_lattice_vector_c
    # ])

    # hkl.insert(0, [0, 0, 0])
    with open(fcalc_file_name+'_all.hkl', mode='w') as fc_all_f, open(fcalc_file_name+'_gt.hkl', mode='w') as fc_gt_f, open(fobs_file, mode='r') as hrf:
        hl = hrf.readlines()
        for lines in hl:
            h, k, l, fc_squared, fo_squared, f_sigma_squared, *value = lines.split()
            h, k, l, fc_squared, fo_squared, f_sigma_squared = \
                int(h), int(k), int(l), float(fc_squared), float(fo_squared), float(f_sigma_squared)

            # referenceで読み込んだh,k,lに対応するフーリエ空間の座標
            fourier_coord = h * reciprocal_lattice_vector_a + \
                            k * reciprocal_lattice_vector_b + \
                            l * reciprocal_lattice_vector_c

            # フーリエ空間での中心からの距離
            r = np.sqrt(np.power(fourier_coord[0], 2)+np.power(fourier_coord[1], 2)+np.power(fourier_coord[2], 2))

            # 特定のhklの点が対応するボクセルの座標()
            target_voxel_x = round(fourier_coord[0] / voxel_unit_length_x) + center[0]
            target_voxel_y = round(fourier_coord[1] / voxel_unit_length_y) + center[1]
            target_voxel_z = round(fourier_coord[2] / voxel_unit_length_z) + center[2]

            # 特定のhklの点が対応するボクセルの座標(Å-1)
            # target_voxel_x = round(fourier_coord[0] / voxel_unit_length_x) * voxel_unit_length_x
            # target_voxel_y = round(fourier_coord[1] / voxel_unit_length_y) * voxel_unit_length_y
            # target_voxel_z = round(fourier_coord[2] / voxel_unit_length_z) * voxel_unit_length_z

            try:
                # L-R 出力
                # target_voxel_x_coord = round(fourier_coord[0] / voxel_unit_length_x) * voxel_unit_length_x
                # target_voxel_y_coord = round(fourier_coord[1] / voxel_unit_length_y) * voxel_unit_length_y
                # target_voxel_z_coord = round(fourier_coord[2] / voxel_unit_length_z) * voxel_unit_length_z
                # 逆格子点とボクセ点の距離
                # distance = np.sqrt(np.power(target_voxel_x_coord - fourier_coord[0], 2) +
                #                    np.power(target_voxel_y_coord - fourier_coord[1], 2) +
                #                    np.power(target_voxel_z_coord - fourier_coord[2], 2))

                # distance 有り
                # fcf.write('\t{0}\t{1}\t{2}\t{3:.6f}\t{4:.6f\n'.format(
                #   h, k, l, distance, voxel_data[target_voxel_x][target_voxel_y][target_voxel_z]), flush=True
                # )

                # gt
                f_obs_value = float(0 if fo_squared < 0 else np.sqrt(fo_squared))
                if fo_squared > 2 * f_sigma_squared:
                    fc_gt_f.write('\t{0}\t{1}\t{2}\t{3:.4}\t{4:.4}\t{5:.6f}\n'.format(
                        h, k, l, r, f_obs_value, voxel_data[target_voxel_x][target_voxel_y][target_voxel_z])
                    )

                fc_all_f.write('\t{0}\t{1}\t{2}\t{3:.4}\t{4:.4}\t{5:.6f}\n'.format(
                    h, k, l, r, f_obs_value, voxel_data[target_voxel_x][target_voxel_y][target_voxel_z])
                )

            except IndexError:
                print('\t{0}\t{1}\t{2}\t{3}'.format(h, k, l, "out of range"), flush=True)
    print('picked up\n')


def calculate_r_factor(fobs_file_name, fcalc_file_name):
    if file_exist('result_' + fcalc_file_name + '.txt'): return
    print('calculating R factor...')
    # calculation phase
    with open('result_' + fcalc_file_name + '.txt', mode='w') as rf, \
            open(fobs_file_name, mode='r') as fof, \
            open(fcalc_file_name+'_all.hkl', mode='r') as fcf:

        obs_lines, calc_lines = fof.readlines(), fcf.readlines()

        hkl_all_list = []
        hkl_gt_list = []
        # R variable
        sum_f_obs_all, sum_f_calc_all, sum_fo_fc_diff_all = 0, 0, 0
        sum_f_obs_gt, sum_f_calc_gt, sum_fo_fc_diff_gt = 0, 0, 0
        sum_f_obs_x_f_calc_all, sum_f_obs_x_f_calc_gt = 0, 0
        sum_f_calc_power_all, sum_f_calc_power_gt = 0, 0
        all_cnt, gt_cnt = 0, 0

        # read
        for obs_line, calc_line in zip(obs_lines, calc_lines):
            obs_line_list, calc_line_list = obs_line.split(), calc_line.split()

            h, k, l = obs_line_list[0], obs_line_list[1], obs_line_list[2]
            f_calc_clisalis_value_squared, f_obs_value_squared, f_sigma_squared \
                = float(obs_line_list[3]), float(obs_line_list[4]), float(obs_line_list[5])

            f_calc_value = float(calc_line_list[5])
            f_obs_value = 0 if f_obs_value_squared < 0 else np.sqrt(f_obs_value_squared)

            # test
            # f_calc_clisalis_value = np.sqrt(f_calc_clisalis_value_squared)
            # f_calc_value = f_calc_clisalis_value

            # all
            hkl_all_list.append([h, k, l, f_obs_value, f_calc_value])
            sum_f_obs_all += abs(f_obs_value)
            sum_f_calc_all += abs(f_calc_value)
            sum_f_obs_x_f_calc_all += abs(f_obs_value) * abs(f_calc_value)
            sum_f_calc_power_all += f_calc_value * f_calc_value
            all_cnt += 1
            # gt
            if f_obs_value_squared > 2 * f_sigma_squared:
                hkl_gt_list.append([h, k, l, f_obs_value, f_calc_value])
                sum_f_obs_gt += abs(f_obs_value)
                sum_f_calc_gt += abs(f_calc_value)
                sum_f_obs_x_f_calc_gt += abs(f_obs_value) * abs(f_calc_value)
                sum_f_calc_power_gt += f_calc_value * f_calc_value
                gt_cnt += 1

        # scaling　ー G
        # s_all = sum_f_obs_x_f_calc_all / sum_f_calc_power_all
        # s_gt = sum_f_obs_x_f_calc_gt / sum_f_calc_power_gt

        s_all, s_gt = 0.001, 0.001
        min_r_all, min_r_gt = 1, 1
        s = 0
        for i in range(10001):
            sum_fo_fc_diff_all, sum_fo_fc_diff_gt = 0, 0
            for hal in hkl_all_list:
                h, k, l, fobs, fcalc = hal[0], hal[1], hal[2], hal[3], hal[4]
                sum_fo_fc_diff_all += abs(fobs - s * fcalc)
            r_factor_all = sum_fo_fc_diff_all / sum_f_obs_all
            min_r_all = min(r_factor_all, min_r_all)
            if min_r_all == r_factor_all:
                s_all = s
            for hgl in hkl_gt_list:
                h, k, l, fobs, fcalc = hgl[0], hgl[1], hgl[2], hgl[3], hgl[4]
                sum_fo_fc_diff_gt += abs(fobs - s * fcalc)
            r_factor_gt = sum_fo_fc_diff_gt / sum_f_obs_gt
            min_r_gt = min(r_factor_gt, min_r_gt)
            if min_r_gt == r_factor_gt:
                s_gt = s
            s += 0.001

        rf.write('project               : ' + fcalc_file_name + '\n\n')
        rf.write('gt                    : I > 2sigma(I)\n')
        rf.write('num_of_lat_point_all  : ' + str(all_cnt) + '\n')
        rf.write('num_of_lat_point_gt   : ' + str(gt_cnt) + '\n')
        rf.write('r_factor_all          : ' + '{:.4f}'.format(min_r_all) + '\n')
        rf.write('r_factor_gt           : ' + '{:.4f}'.format(min_r_gt) + '\n')
        rf.write('scale_all             : ' + '{:.3f}'.format(s_all) + '\n')
        rf.write('scale_gt              : ' + '{:.3f}'.format(s_gt) + '\n')
    print('wrote result -> result_' + fcalc_file_name + '.txt\n')
