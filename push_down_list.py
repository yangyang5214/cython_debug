# -*- coding: UTF-8 -*-


def my_process(data: list):
    r = []
    for _ in data:
        d = {
            'name': _.get('name'),
        }
        info = [_['company'] for _ in _.get('info', [])]
        d['info'] = info
        d['age'] = _.get('age'),
        r.append(d)
    return r


def _print(data):
    for item in data:
        print(item)


if __name__ == '__main__':
    data = [
        {
            "name": "beer",
            "age": "18",
            "info": [
                {"date": "2013", "company": "微软"},
                {"date": "2017", "company": "阿里巴巴"},
                {"date": "2019", "company": "京东"},
            ]
        },
        {
            "name": "beef",
            "age": "20",
            "info": [
                {"date": "2013", "company": "拼刀刀"},
                {"date": "2017", "company": "字节"},
            ]
        },
    ]
    r = my_process(data)
    _print(r)
