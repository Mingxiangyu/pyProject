# -*- codeing = utf-8 -*-
# @Time :2023/10/18 17:21
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  获取接箍异常值.py
import numpy as np
from scipy.signal import find_peaks

import Pandas as pd


def enhanced_peak_search(x: pd.Series, width_weight=1, height_weight=1, outlier_weight=1) -> np.ndarray:
    """

    :param x: 滑动窗口选择的数据
    :param width_weight: 数据宽权重
    :param height_weight: 数据高权重
    :param outlier_weight: 离群值权重
    :return:
    """
    gradient = np.gradient(x)
    peaks, _ = find_peaks(x)
    widths = []
    heights = []
    outlier_scores = []
    mean_val = np.mean(x)
    std_val = np.std(x)

    for peak in peaks:
        left_indices = np.where(gradient[:peak] < 0)[0]
        right_indices = np.where(gradient[peak:] < 0)[0]
        left_valley = left_indices[-1] if len(left_indices) > 0 else 0
        right_valley = peak + right_indices[0] if len(right_indices) > 0 else len(x) - 1

        width = right_valley - left_valley
        height = x[peak] - min(x[left_valley], x[right_valley])
        outlier_score = abs(x[peak] - mean_val) / std_val

        widths.append(width)
        heights.append(height)
        outlier_scores.append(outlier_score)

    # 使用z-score标准化处理
    widths = (widths - np.mean(widths)) / np.std(widths)
    heights = (heights - np.mean(heights)) / np.std(heights)
    outlier_scores = (outlier_scores - np.mean(outlier_scores)) / np.std(outlier_scores)

    # 计算综合分数
    scores = width_weight * widths + height_weight * heights + outlier_weight * outlier_scores

    # 返回分数最高的波峰
    highest_peak = peaks[np.argmax(scores)]

    return np.array([highest_peak])