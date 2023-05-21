import gdown
import argparse
import pathlib

def download_2023_data(data_path):
    id = r'1XXk2LO0CsNADBB1LRGOV5rUpyZdEZ8s2'
    gdown.download(id=id, output=data_path + '/lol.csv')

def download_entire_data(data_path):
    id = "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH"
    gdown.download_folder(id=id, output=data_path)


def main(args):
    '''
    Source of competetive data: https://oracleselixir.com/tools/downloads
    https://drive.google.com/drive/u/1/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH
    '''
    print('Downloading data')
    pathlib.Path(args.data_path).mkdir(parents=True, exist_ok=True) 
    if args.latest == 1: download_2023_data(args.data_path)
    elif args.latest == 0: download_entire_data(args.data_path)
    else: raise Exception('Invalid value for latest')
    print('Downloading finished')

if __name__ == '__main__':
    data_path = '../data'
    parser = argparse.ArgumentParser(description='Download lol data from google drive')
    parser.add_argument('-p', '--data_path', action='store', dest='data_path', default='../data')
    parser.add_argument('-l', '--latest', action='store', dest='latest', type=int, default=1) 
    args = parser.parse_args()
    main(args)
