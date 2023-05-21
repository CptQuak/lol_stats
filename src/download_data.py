import gdown

def main(data_path):
    '''
    Source of competetive data: https://oracleselixir.com/tools/downloads
    https://drive.google.com/drive/u/1/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH
    '''
    print('Downloading data')
    id = "1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH"
    gdown.download_folder(id=id, output=data_path, quiet=True, use_cookies=True)
    print('Downloading finished')

if __name__ == '__main__':
    data_path = '../data'
    main(data_path)
