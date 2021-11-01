# -*- coding: UTF-8 -*-

import push_down_list_copy

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
    r = push_down_list_copy.my_process(data)
    push_down_list_copy._print(r)
