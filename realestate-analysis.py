import json
import re
import pandas as pd
import numpy as np
import json

def digits(string, min, max):
    s = re.findall('\d+', str(string))
    if len(s) == 4:
        s = (int(s[0]+s[1]) + int(s[2]+s[3])) / 2
    elif len(s) == 3:
        s1 = int(s[0]+s[1]+s[2])
        if s1 > max:
            s1 = (int(s[0]+s[1]) + int(s[2])) / 2
            if s1 > max:
                s1 = (int(s[0]) + int(s[1]+s[2])) / 2
                if s1 > max:
                    s1 = int(s[0]+s[1])
        s = s1
    elif len(s) == 2:
        s1 = int(s[0]+s[1])
        if s1 > max:
            s = (int(s[0]) + int(s[1])) / 2
        elif 0 < s1 < min:
            s = re.findall('\d+.\d+', str(string))
            try:
                s = float(s[0]) * 1000000
            except Exception:
                s = 0
        else:
            s = s1
    elif len(s) == 1:
        s = int(s[0])
    else:
        s = 0
    if s < min or s > max:
        s = 0
    return s

state = 'vic'

filename = 'realestate.com-' + state
minprice = 10000
maxprice = 10000000
min_sample = 3

with open(filename + '.json', 'r') as fin:
    load = json.load(fin)

summary = {}
median_price = {}
samples = {}

for suburb, value in load.items():
    properties = value[1]

    postcode = []
    addresses = []
    prices = []
    baths = []
    beds = []
    cars = []
    for property in properties:
        print(property)
        addresses.append(property['address'])
        try:
            postcode.append(re.match('.*?([0-9]+)$', property['address']).group(1))
        except AttributeError:
            postcode.append('0000')
        prices.append(digits(property['price'], minprice, maxprice))
        beds.append(int(property['bed']))
        try:
            baths.append(int(property['bath']))
        except ValueError:
            baths.append(0)
        try:
            cars.append(int(property['car']))
        except ValueError:
            cars.append(0)
    data = {'Postcode': postcode, 'Addresses': addresses, 'Prices': prices, 'Baths': baths, 'Beds': beds, 'Cars': cars}

    df = pd.DataFrame(data = data, columns = ['Postcode', 'Prices', 'Beds', 'Baths', 'Cars'],
                        index = addresses)
    filtered_df = df.loc[(df['Prices'] != 0) & (df['Beds'] != 0)]

    summary[suburb] = filtered_df
    price_bed = filtered_df['Prices'] / filtered_df['Beds']
    samples[suburb] = len(price_bed)
    if len(price_bed) < min_sample:
        median_price[suburb] = np.NaN
    else:
        median_price[suburb] = price_bed.median()

with open('medianprices-' + state + '.json', 'w') as fout:
    json.dump([median_price, samples], fout)
