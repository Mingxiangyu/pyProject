import json


def clean_json(json_data):
    cleaned_data = []
    for item in json_data:
        cleaned_item = {}
        cleaned_item["LayerNomThkin"] = item.get("LayerNomThkin")
        cleaned_item["LayerODin"] = item.get("LayerODin")
        cleaned_item["LayerWtLbFt"] = item.get("LayerWtLbFt")
        cleaned_item["channel_data"] = []

        for layer_item in item.get("layer_item", []):
            cleaned_item["channel_data"].extend(layer_item.get("channel_data", []))

        cleaned_data.append(cleaned_item)

    return cleaned_data


json_str = '''[
    {
        "layer_end": 897,
        "layer_item": [
            {
                "LayerNomThkin": 0.395,
                "LayerODin": 9.625,
                "LayerWtLbFt": 40,
                "V": -0.009,
                "W": 0.25,
                "channel_data": [
                    {
                        "label_end": 4.0667,
                        "label_start": 0
                    },
                    {
                        "label_end": 64.834,
                        "label_start": 55.0667
                    }
                ],
                "channel_name": "AD[15]",
                "layer": 3
            },
            {
                "LayerNomThkin": 0.514,
                "LayerODin": 13.375,
                "LayerWtLbFt": 72,
                "V": -0.006,
                "W": 0.25,
                "channel_data": [
                    {
                        "label_end": 4.0667,
                        "label_start": 0
                    },
                    {
                        "label_end": 89.0667,
                        "label_start": 55.0667
                    }
                ],
                "channel_name": "AD[38]",
                "layer": 3
            },
            {
                "LayerNomThkin": 0.594,
                "LayerODin": 18.625,
                "LayerWtLbFt": 115,
                "V": -0.009,
                "W": 0.25,
                "channel_data": [
                    {
                        "label_end": 4.0667,
                        "label_start": 0
                    },
                    {
                        "label_end": 65.0667,
                        "label_start": 55.0667
                    }
                ],
                "channel_name": "AD[54]",
                "layer": 3
            }
        ],
        "layer_start": 4.0667,
        "layer_type": 3
    },
    {
        "layer_end": 4652.4,
        "layer_item": [
            {
                "LayerNomThkin": 0.395,
                "LayerODin": 9.625,
                "LayerWtLbFt": 40,
                "V": -0.009,
                "W": 0.25,
                "channel_data": [
                    {
                        "label_end": 928.909,
                        "label_start": 897
                    },
                    {
                        "label_end": 969.471,
                        "label_start": 930.709
                    },
                    {
                        "label_end": 1009.058,
                        "label_start": 971.271
                    }
                ],
                "channel_name": "AD[15]",
                "layer": 2
            },
            {
                "LayerNomThkin": 0.514,
                "LayerODin": 13.375,
                "LayerWtLbFt": 72,
                "V": -0.001,
                "W": 0.42,
                "channel_data": [
                    {
                        "label_end": 933.424,
                        "label_start": 897
                    },
                    {
                        "label_end": 972.385,
                        "label_start": 935.224
                    },
                    {
                        "label_end": 1011.549,
                        "label_start": 974.185
                    }
                ],
                "channel_name": "AD[38]",
                "layer": 2
            },
            {
                "LayerNomThkin": null,
                "LayerODin": null,
                "LayerWtLbFt": null,
                "V": 0,
                "W": 1,
                "channel_name": null,
                "layer": 2
            }
        ],
        "layer_start": 897,
        "layer_type": 2
    },
    {
        "layer_end": 5149.667,
        "layer_item": [
            {
                "LayerNomThkin": 0.395,
                "LayerODin": 9.625,
                "LayerWtLbFt": 40,
                "V": -0.007,
                "W": 0.25,
                "channel_data": [
                    {
                        "label_end": 4656.149,
                        "label_start": 4652.4
                    }
                ],
                "channel_name": "AD[25]",
                "layer": 1
            },
            {
                "LayerNomThkin": null,
                "LayerODin": null,
                "LayerWtLbFt": null,
                "V": 0,
                "W": 1,
                "channel_name": null,
                "layer": 1
            }
        ],
        "layer_start": 4652.4,
        "layer_type": 1
    }
]'''

json_data = json.loads(json_str)
cleaned_data = clean_json(json_data)
cleaned_json = json.dumps(cleaned_data, indent=4)
print(cleaned_json)
