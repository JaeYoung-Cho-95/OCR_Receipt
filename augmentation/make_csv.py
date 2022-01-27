import pandas as pd
import json
import glob
from tqdm import tqdm

def make_csv(images_path : str, json_path : str) -> pd.DataFrame:
    """
        이 함수는 이미지들의 경로, json 파일들의 경로를 입력값으로 받아 
        Image_name, Json_name, Label, XMin,YMin,XMax,YMax 형태의 csv를 만들어주는 함수입니다.
    
    Args:
        images_path (str): 이미지파일들의 경로
                           ex) 'C/User/Desktop/data/images/'
        json_path (str): json 파일들의 경로
                         ex) 'C/User/Desktop/data/json/'

    Returns:
        pd.DataFrame: Image_name, Json_name, Label, XMin,YMin,XMax,YMax 형태의 dataframe

        또한 images, json 파일들의 존재하는 상위 경로에 csv 파일을 저장한다.
    """    

    # images_path = '.././data/aug_img/'
    # json_path = '.././data/aug_json/'

    print('csv file 을 만드는 중 입니다.')

    images_list = glob.glob(images_path + '*.jpg')
    json_list = glob.glob(json_path + '*.json')


    # mac = split 안에 '/'
    # windows = split 안에 '\\' 넣기
    images_list = [x.split('\\')[-1] for x in images_list]
    json_list = [x.split('\\')[-1] for x in json_list]


    images_list = sorted(images_list, key = lambda x : int(x.split('.')[0]))
    json_list = sorted(json_list, key = lambda x : int(x.split('.')[0]))

    ground_truth = []
    for json_idx in tqdm(range(len(json_list))):
        with open("{}{}".format(json_path,json_list[json_idx]), "r") as file_json:
            file_json = json.load(file_json)
            for i,v in file_json.items():
                if i == 'type':
                    continue
                for j in v:
                    ground_truth.append([images_list[json_idx]])
                    ground_truth[-1].append(json_list[json_idx])
                    for key,value in j.items():
                        if type(value) == list:
                            for i in value:
                                ground_truth[-1].append(i) 
                        else: 
                            ground_truth[-1].append(value)

    df = pd.DataFrame(ground_truth, columns =['Image_Name','Json_Name', 'Label','Xmin','Ymin','XMax','YMax']) 
    df.to_csv('.././data/df.csv',sep=',',na_rep='NaN',encoding='utf-8')

    return df