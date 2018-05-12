## download pdf from latest link
import requests
import os
import pandas as pd
from time_util import get_last_created


def download_pdfs(spreadsheet_folder='../weekly_pulls/',
                  destination_folder='../downloaded_pulls/'):
    latest_file, date = get_last_created(spreadsheet_folder, '.csv')
    df = pd.read_csv(latest_file)
    ids, links = df["ID"].tolist(), df['PDF_LINK'].tolist()
    folder_name = "_".join([str(s) for s in [date.year, date.month, date.day]])
    new_folder_path = destination_folder + folder_name + '/'
    if not os.path.isdir(new_folder_path):
        os.makedirs(new_folder_path)
    num_to_download = len(links)
    for k, (i, l) in enumerate(zip(ids, links)):
        print("{} / {}...".format(k + 1, num_to_download))
        response = requests.get(l)
        with open(new_folder_path + i + '.pdf', 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    download_pdfs()