def flatten(dic):
    result = []
    for key in dic.keys():
        value = dic[key]
        if isinstance(value, dict):
            result.extend(flatten(value))
        elif isinstance(value, list):
            for elem in value:
                result.extend(flatten(elem))
        else:
            result.append(key)
    return result

a = {'x': [{'y': "ceshi"}, {'z': 2.6}], 'a': "shenmeyang", 'b': "zuihou"}
keys = flatten(a)

print(keys)
