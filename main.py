#!/usr/bin/env python
# coding: utf-8

# In[1]:


def api_kec_medan():
    import requests
    from bs4 import BeautifulSoup
    import numpy as np
    
    URL_kabupaten = "https://covid19.pemkomedan.go.id/index.php?page=stat_medan"
    r_kabupaten = requests.get(URL_kabupaten) 
    soup_kabupaten = BeautifulSoup(r_kabupaten.content, 'html5lib')
    tglUpdate = soup_kabupaten.find('section').div.text.split('\n')[6].split(',')[1].strip()
    
    URL_kecamatan = "http://covid19.pemkomedan.go.id/index.php?page=stat_kec"
    r_kecamatan = requests.get(URL_kecamatan)
    soup_kecamatan = BeautifulSoup(r_kecamatan.content, 'html5lib')
    
    resp = '{"data":['
    resp += '{"judul":"Data Covid-19 per kecamatan di Kota Medan",'
    resp += '"sumber":"http://covid19.pemkomedan.go.id/index.php?page=stat_kec",'
    resp += '"tanggal_update":"'+tglUpdate+'",'
    resp += '"kec":['
    
    panjang = len(soup_kecamatan.find('table').tbody.findAll('tr'))

    for kode in range(panjang):
        kecamatan = soup_kecamatan.find('table').tbody.findAll('tr')[kode].findAll('td')[1].text.title()
        pdp_dirawat = soup_kecamatan.find('table').tbody.findAll('tr')[kode].findAll('td')[10].text
        pdp_meninggal = soup_kecamatan.find('table').tbody.findAll('tr')[kode].findAll('td')[9].text
        positif_dirawat = soup_kecamatan.find('table').tbody.findAll('tr')[kode].findAll('td')[13].text
        positif_sembuh = soup_kecamatan.find('table').tbody.findAll('tr')[kode].findAll('td')[11].text
        positif_meninggal = soup_kecamatan.find('table').tbody.findAll('tr')[kode].findAll('td')[12].text
        
        resp += '{'
        resp += '"no":"'+str(kode+1)+'",'
        resp += '"nama_kecamatan":"'+kecamatan+'",'
        resp += '"pdp_dirawat":"'+pdp_dirawat+'",'
        resp += '"pdp_meninggal":"'+pdp_meninggal+'",'
        resp += '"positif_dirawat":"'+positif_dirawat+'",'
        resp += '"positif_sembuh":"'+positif_sembuh+'",'
        resp += '"positif_meninggal":"'+positif_meninggal+'"'
        resp += '}'
        
        
        if kode<panjang-1:
            resp += ','
        
    resp += ']}'
    resp += ']}'
        
    return resp


# In[ ]:





# In[ ]:





# In[2]:


import requests
import os
import sys
import urllib.parse

from flask import Flask, request, abort, send_from_directory, Response


# In[3]:


app = Flask(__name__)

app = Flask(__name__, static_url_path='')


# In[4]:


@app.route('/medan')
def medan():
    return Response(api_kec_medan(), mimetype='application/json')


# In[ ]:


if __name__ == "__main__":
    app.run()

