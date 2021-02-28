# %%
import requests
import pandas as pd
import time
import datetime as dt
from tqdm import tqdm
# %%
SKILLS = "skillIds=1052%2C1732%2C2223%2C2225%2C2243%2C2368%2C2741%2C2750%2C3359%2C4457%2C4662%2C4668%2C5134%2C5277%2C5437%2C5440%2C7293%2C7329%2C7330%2C7333%2C7354%2C7576%2C7718%2C8601%2C9218%2C100109%2C100130%2C100288%2C100379%2C101885%2C102573%2C261%2C2080%2C2961%2C5624%2C7137%2C305%2C515%2C517%2C581%2C1128%2C1928%2C3057%2C3363%2C3376%2C3377%2C3442%2C4053%2C4666%2C5628%2C6866%2C6953%2C7192%2C8694%2C9463%2C102072%2C1545%2C3384%2C3868%2C4539%2C5284%2C8523%2C8970%2C9486%2C100205%2C100262%2C100707%2C105157%2C4667%2C5386%2C9464%2C2266%2C276%2C5834%2C102462%2C807%2C3534%2C3060%2C66%2C2881%2C5319%2C5644%2C7001%2C7414%2C109562%2C316%2C2231%2C3537%2C7154%2C7328%2C8692%2C9221%2C100165%2C100422%2C101138%2C102118%2C104294"


def search(phrase):
    page = 0
    url = f"https://api.mycareersfuture.gov.sg/v2/jobs?search={phrase}&{SKILLS}&limit=100&page={page}&sortBy=new_posting_date&omitCountWithSchemes=true"
    r = requests.get(url)
    res = r.json()
    if len(res['_links']['last']['href'].split('page=')) <= 1:
        last_page = 0
    else:
        last_page = int(res['_links']['last']
                        ['href'].split('page=')[1].split('&')[0])
    data = []
    for page in tqdm(range(last_page+1), desc=phrase.upper()):
        url = url = f"https://api.mycareersfuture.gov.sg/v2/jobs?search={phrase}&{SKILLS}&limit=100&page={page}&sortBy=new_posting_date&omitCountWithSchemes=true"
        r = requests.get(url)
        res = r.json()
        res = res['results']
        for x in res:
            employmentTypes = [et['employmentType']
                               for et in x['employmentTypes']]
            data.append({
                'uuid': x['uuid'],
                'title': x['title'],
                'postedCompanyName': x['postedCompany']['name'],
                'minimumYearsExperience': x['minimumYearsExperience'],
                'Full Time': 'Full Time' in employmentTypes,
                'Part Time': 'Part Time' in employmentTypes,
                'Internship/Traineeship': 'Internship/Traineeship' in employmentTypes,
                'Permanent': 'Permanent' in employmentTypes,
                'Temporary': 'Temporary' in employmentTypes,
                'Flexi-work': 'Flexi-work' in employmentTypes,
                'Contract': 'Contract' in employmentTypes,
                'salaryMin': x['salary']['minimum'],
                'salaryMax': x['salary']['maximum'],
                'salaryMid': (int(x['salary']['maximum']) + int(x['salary']['maximum']))/2,
                'salaryType': x['salary']['type']['salaryType'],
                'expiryDate': x['metadata']['expiryDate'],
                'totalNumberJobApplication': x['metadata']['totalNumberJobApplication'],
                'totalNumberOfView': x['metadata']['totalNumberOfView'],
                'originalPostingDate': x['metadata']['originalPostingDate'],
                'newPostingDate': x['metadata']['newPostingDate'],
                'link': x['metadata']['jobDetailsUrl'],
            })
        time.sleep(1)

    df = pd.DataFrame(data)
    df.to_csv(
        f"results_{phrase}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    return df

# %%


search('data analyst')
