from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urlparse


if __name__ == '__main__':
    directory = 'C:\Disk E\prescribing\prescribing'
    csv_file_path = f'C:\Disk E\drug interaction\drug_class.csv'
    df = pd.DataFrame(columns=['Drug', 'Class'])
    files = os.listdir(directory)
    for i in range(0, len(files)):
        try:
            file_path = os.path.join(directory, files[i])
            file_name = os.path.basename(file_path)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding="utf8") as HTMLFile:
                    index = HTMLFile.read()
                    S = BeautifulSoup(index, 'lxml')
                    results = S.findAll("div", {"class": "pronounce-title"})
                    if len(results) == 0:
                        results = S.findAll("div", {"class": "contentBox"})
                    drug_name = results[0].contents[1].contents[0]
                    drug_class = S.findAll("p", {"class": "drug-subtitle"})
                    if len(drug_class) != 0:
                        drug_classes = drug_class[0].contents
                        for j in range(0, len(drug_classes)):
                            if str(drug_classes[j]).lower().__contains__("class"):
                                if str(drug_classes[j+1]) != "" and str(drug_classes[j+1]) != "\n" and str(drug_classes[j+1]) != " ":
                                    d_class = str(drug_classes[j+1])
                                    df = df._append({'Drug': drug_name, 'Class': d_class}, ignore_index=True)
                                    break
                                else:
                                    d_class = drug_classes[j+2].contents[0]
                                    df = df._append({'Drug': drug_name, 'Class': d_class}, ignore_index=True)
                                    break
                    else:
                        results = S.findAll("div", {"class": "contentBox"})[0].contents
                        for j in range(0, len(results)):
                            if str(results[j]).lower().__contains__("pharmacologic category"):
                                if str(results[j+1]) != "" and str(results[j+1]) != '\n':
                                    d_class = results[j + 1]
                                    df = df._append({'Drug': drug_name, 'Class': d_class}, ignore_index=True)
                                    break
                                else:
                                    d_class = results[j + 2].contents[1].get_text()
                                    df = df._append({'Drug': drug_name, 'Class': d_class}, ignore_index=True)
                                    break
            if i % 50 == 0:
                print(i)
                print(file_name)

            if i % 1000 == 0:
                csv_file_path = f'C:\Disk E\prescribing\prescribing {i}.csv'
                df.to_csv(csv_file_path, index=False)
                df = pd.DataFrame(columns=['Drug', 'Class'])


        except Exception as e:
            print(e)
            print(file_name)
            HTMLFile.close()

    df.to_csv(csv_file_path+"_", index=False)



