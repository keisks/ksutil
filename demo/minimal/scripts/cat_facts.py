#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

# minimal backend that uses public WebAPI 
def get_cat_facts():
    r = requests.get("https://cat-fact.herokuapp.com" + "/facts/random?animal=cat&amount=1")
    data = json.loads(r.text)    
    return data

if __name__ == "__main__":
    print(get_cat_facts())

