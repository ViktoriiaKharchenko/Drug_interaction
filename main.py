from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urlparse


if __name__ == '__main__':

    directory = 'C:\Disk E\interactionInfo'
    df = pd.DataFrame(columns=['Drug1', 'Drug2', 'Interaction'])
    log_file = open("C:\Disk E\drug interaction\log.txt", 'w')
    files = os.listdir(directory)
    for i in range(0, len(files)):
        try:
            file_path = os.path.join(directory, files[i])
            file_name = os.path.basename(file_path)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as HTMLFile:
                    try:
                        index = HTMLFile.read()
                        S = BeautifulSoup(index, 'lxml')
                        results = S.findAll("div", {"class": "contentBox"})
                        list = results[0].findAll("b", class_=None)
                        drug1 = list[0].contents[0]
                        drug2 = list[1].contents[0]
                        container = S.findAll("div", {"class": "interactions-reference-header"})
                        int_level = container[0].findAll("span")[0].contents[0]
                        if df['Drug1'].isin([drug2]).any() and df['Drug2'].isin([drug1]).any():
                            pass
                        else:
                            df = df._append({'Drug1': drug1, 'Drug2': drug2, 'Interaction': int_level}, ignore_index=True)

                    except Exception as e:
                        if len(results) == 0:
                            results = S.findAll("body")[0]
                            s = str(results.contents[1].contents[0])
                            if s in "Access Denied":
                                message = results.contents[2]
                                url_start = message.find('http://')
                            if url_start != -1:
                                url_end = message.find(' ', url_start)
                                if url_end == -1:
                                    url_end = len(message)
                                link = message[url_start:url_end]
                                parsed_link = urlparse(link)
                                log_file.write(file_name + "\n")
                                log_file.write(str(parsed_link) + "\n")

                    if i % 1000 == 0:
                        print(i)
                        print(file_name)

                    if i % 3000 == 0:
                        csv_file_path = f'C:\Disk E\drug interaction\interaction {i}.csv'
                        df.to_csv(csv_file_path, index=False)
                        df = pd.DataFrame(columns=['Drug1', 'Drug2', 'Interaction'])

                    S.decompose()
                    HTMLFile.close()

        except Exception as e:
            print(e)
            print(file_name)
            HTMLFile.close()

    df.to_csv(csv_file_path, index=False)


