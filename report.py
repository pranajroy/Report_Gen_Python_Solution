import requests
import pandas as pd
import os
from glob import glob
import re
import datetime
from bs4 import BeautifulSoup as bs
import time

''' Get the url from the argument to pass it as parser'''
def get_soup(url):
    return bs(open(url,encoding = "iso-8859-1"), "html.parser")

''' Get the table data'''
def get_table(soup):
    return soup.find_all("table")

'''Get the table data row wise and append it in the list named cell and finally append it in rows'''
def get_table_rows(table,date):
    rows = []
    for tr in table.find_all("tr"):
        cells = []
        tds = tr.find_all("td")
        flag = True
        for td in tds:
                if len(td.text.strip()) == 0:
                    flag = flag and False
                cells.append(td.text.strip())
        if flag:
            cells[0] = cells[0]+" "+str(date.strftime("%H:%M:%S"))
            rows.append(cells)
    return rows

''' Convert the rows into pandas dataframe and then to csv format'''
def save_as_csv(file, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{file}.csv", index=False)
    
'''This function calls the sub functions and provides the final output'''
def runner(base_path,report):
    all_rows = []
    headers = ['Production', 'Total Yield QTY', 'UoM', 'Total Reject Qty', 'UoM', 'Date', 'Finish Time', 'SAP Component number', 'Total Material A-grade (pcs)', 'Reject Material Reject Bin\n  (pcs)', 'SAP Description', 'Qty consumed', 'UoM','Timestamp']
    result = [y for x in os.walk(base_path) for y in glob(os.path.join(x[0], 'sheet006.html'))]
    for filename in result:
                    match = re.search('\d{4} \d{2} \d{2} \d{2} \d{2} \d{2}', filename)
                    date = datetime.datetime.strptime(match.group(), '%Y %m %d %H %M %S')
                    soup = get_soup(filename)
                    tables = get_table(soup)
                    for table in tables:
                            rows = get_table_rows(table,date)
                            all_rows.extend(rows[1:])
    save_as_csv(report, headers, all_rows)


if __name__ == "__main__":
    import sys
    try:
        base = sys.argv[1]
        report = sys.argv[2]
    except IndexError:
        print("Provide the base path and report location")
        exit(1)
    runner(base,report)
    print("Generated report ", report)
