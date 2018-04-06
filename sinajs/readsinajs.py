import requests
import csv

def make_key(id):
    if not id:
        return ''
    if id.find('f_') == 0 and len(id) == 8:
        return id
    if len(id) > 6:
        return ''
    if len(id) < 6:
        id = '' * (6 - len(id)) + id
    return 'f_' + id

def make_url(ids):
    '''
    >>> make_url(['070001'])
    'http://hq.sinajs.cn/list=f_070001'
    >>> make_url(['070001', '', '373010'])
    'http://hq.sinajs.cn/list=f_070001,f_373010'
    >>> make_url([])
    ''
    >>> make_url(['070001', '373010'])
    'http://hq.sinajs.cn/list=f_070001,f_373010'
    '''
    url = ''
    if isinstance(ids, str):
        url = make_key(ids)
    else:
        for id in ids:
            key = make_key(id)
            if key:
                if url:
                    url = url + ','
                url = url + key
    if url:
        url = "http://hq.sinajs.cn/list=" + url
    return url

def get_data(url):
    r = requests.get(url)
    return r.text

def split_data(text):
    '''
    >>> v = split_data('var hq_str_f_070001="嘉实成长收益混合A,1.3554,4.5576,1.3628,2018-04-02,34.357";')
    >>> v['id']
    '070001'
    >>> v['name']
    '嘉实成长收益混合A'
    >>> v['rVal']
    1.3554
    >>> v['cVal']
    4.5576
    >>> v['pVal']
    1.3628
    >>> v['date']
    '2018-04-02'
    '''
    r = {}
    text = text.strip()

    # before =, ID
    vals = text.partition('=')
    if not vals[1]:
        raise ValueError
    val = vals[0]
    val = val.strip()
    val = val[-6:]
    r['id'] = val
    
    # after =, get text between "
    text = vals[2]
    pos = text.rfind(';')
    if pos != len(text) - 1:
        raise ValueError
    text = text[0:len(text) - 1]
    text = text.strip()
    pos = text.find('"')
    if pos != 0:
        raise ValueError
    pos = text.rfind('"')
    if pos != len(text) - 1:
        raise ValueError
    text = text[1: pos]

    vals = text.split(',')
    if len(vals) != 6:
        raise ValueError

    r['name'] = vals[0].strip()
    r['rVal'] = float(vals[1].strip())
    r['cVal'] = float(vals[2].strip())
    r['pVal'] = float(vals[3].strip())
    r['date'] = vals[4]

    return r

def read_ids(file):
    ids = []
    with open(file, encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            id = ''
            if len(row):
                id = row[0]
            ids.append(id)
    return ids

def save_file(file, data):
    with open(file, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

def update_file(file):
    ids = read_ids(file)
    data = []
    for id in ids:
        url = make_url(id)
        text = get_data(url)
        try:
            vals = split_data(text)
            #data.append([id, vals['name'], vals['rVal'], vals['cVal'], vals['pVal'], vals['date']])
            data.append([id, vals['name'], vals['rVal'], vals['cVal'], vals['pVal'], vals['date']])
        except:
            data.append([id])
    save_file(file, data)

if __name__ == '__main__':
    update_file('sinajs.csv')
