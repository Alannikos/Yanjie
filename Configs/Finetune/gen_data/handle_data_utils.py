import json
import random

def split_data(data):
    pass

def filter_data(data):
    new_data = []
    for record in data:
        if len(record['conversation']) != 0:
            new_data.append(record)

    return new_data

def sampling_data(data, num_sample):
    new_data = random.sample(data, k=num_sample)
    return new_data

if __name__ == "__main__":
    with open("/root/Yanjie/Components/Configs/Finetune/datasets/alpca_data_ft.json", 'r') as file:
        data = json.load(file)
        # new_data = filter_data(data)
        # with open("new_data.json", 'w', encoding='utf-8') as file:
        #     json.dump(new_data, file)
        new_data = sampling_data(data, 2000)
        with open("/root/Yanjie/Components/Configs/Finetune/datasets/ft_data_alpaca_1.json", 'w') as file1:
            json.dump(new_data, file1)
