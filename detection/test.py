def getCalculate(layer_type, label_label, a_jun, b_jun, c_jun, e_jun, n_jun, w, v, curve_value):
    """
    进行计算
    :param layer_type: 井构类型，1类，2类，3类等
    :param label_label:  管节标签，A，B，C
    :param a_jun:  a均值
    :param b_jun:
    :param c_jun:
    :param e_jun:
    :param n_jun:
    :param w: 计算参数1
    :param v: 计算参数2
    :param curve_value: 曲线中当前值
    :return:
    """
    calculate = None
    if layer_type == 1:
        if label_label == "N":
            calculate = w * (1 / w - 1 / 2 + curve_value / n_jun - (a_jun + e_jun) / 2) + v
        elif label_label == "E":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v
        elif label_label == "A":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v
    elif layer_type == 2:
        if label_label == "N":
            calculate = w * (1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + e_jun) / 2) + v
        elif label_label == "E":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v
        elif label_label == "B":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v
        elif label_label == "A":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v
    elif layer_type == 3:
        if label_label == "N":
            calculate = w * (1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + c_jun + e_jun) / 2) + v
        elif label_label == "E":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v
        elif label_label == "C":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (c_jun) / 2) + v
        elif label_label == "B":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v
        elif label_label == "A":
            calculate = w * (1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v
    return calculate


def getCalculate2(layer_type, label_label, a_jun, b_jun, c_jun, e_jun, n_jun, w, v, curve_value):
    settings = {
        1: {
            "N": {"formula": "w * (1 / w - 1 / 2 + curve_value / n_jun - (a_jun + e_jun) / 2) + v"},
            "E": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v"},
            "A": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v"}
        },
        2: {
            "N": {"formula": "w * (1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + e_jun) / 2) + v"},
            "E": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v"},
            "B": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v"},
            "A": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v"}
        },
        3: {
            "N": {"formula": "w * (1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + c_jun + e_jun) / 2) + v"},
            "E": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v"},
            "C": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (c_jun) / 2) + v"},
            "B": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v"},
            "A": {"formula": "w * (1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v"}
        }
    }
    formula = settings.get(layer_type, {}).get(label_label, {}).get("formula")
    if formula:
        return eval(formula)
    else:
        return None


def getCalculate1(layer_type, label_label, a_jun, b_jun, c_jun, e_jun, n_jun, w, v, curve_value):
    # 参数和计算公式的字典
    params = {
        1: {
            "N": {"params": [a_jun, e_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, e_jun, n_jun: w * (
                    1 / w - 1 / 2 + curve_value / n_jun - (a_jun + e_jun) / 2) + v},
            "E": {"params": [e_jun, n_jun], "formula": lambda w, v, curve_value, e_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v},
            "A": {"params": [a_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v}
        },
        2: {
            "N": {"params": [a_jun, b_jun, e_jun, n_jun],
                  "formula": lambda w, v, curve_value, a_jun, b_jun, e_jun, n_jun: w * (
                          1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + e_jun) / 2) + v},
            "E": {"params": [e_jun, n_jun], "formula": lambda w, v, curve_value, e_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v},
            "B": {"params": [b_jun, n_jun], "formula": lambda w, v, curve_value, b_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v},
            "A": {"params": [a_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v}
        },
        3: {
            "N": {"params": [a_jun, b_jun, c_jun, e_jun, n_jun],
                  "formula": lambda w, v, curve_value, a_jun, b_jun, c_jun, e_jun, n_jun: w * (
                          1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + c_jun + e_jun) / 2) + v},
            "E": {"params": [e_jun, n_jun], "formula": lambda w, v, curve_value, e_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v},
            "C": {"params": [c_jun, n_jun], "formula": lambda w, v, curve_value, c_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (c_jun) / 2) + v},
            "B": {"params": [b_jun, n_jun], "formula": lambda w, v, curve_value, b_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v},
            "A": {"params": [a_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v}
        }
    }
    # 获取对应的参数和计算公式
    params_dict = params.get(layer_type, {}).get(label_label, None)
    if params_dict is None:
        return None
    params_list = params_dict["params"]
    formula = params_dict["formula"]
    # 使用参数和计算公式计算结果
    calculate = formula(w, v, curve_value, *params_list)
    return calculate


calculate_ = getCalculate1(3, "N", 446.25790221642785, 311.6120251716253, 323.67046209386314, 332.984272282077,
                           316.0507548448953, 0.25, -0.009, 186.923)
print(calculate_)
calculate = getCalculate(3, "N", 446.25790221642785, 311.6120251716253, 323.67046209386314, 332.984272282077,
                         316.0507548448953, 0.25, -0.009, 186.923)
print(calculate)
