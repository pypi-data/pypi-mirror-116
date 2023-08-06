"""
Module core
===========
This module retrieves data from ELODIE/SOPHIE archive. It has two classes,
Elodie and Sophie, both could be constructed by passing an object name.

Help on Elodie FITS files:
http://atlas.obs-hp.fr/elodie/500/download.html

Help on Sophie FITS files:
http://atlas.obs-hp.fr/sophie/spec_help.html
"""

import numpy as np
import pandas as pd
import requests
from urllib.request import urlretrieve
from .columns import desc_el_ccf, desc_el_spec, desc_so_ccf, desc_so_spec

def _get_df(url_, col_dc, int_cols, float_cols):
    url = url_ + str(list(col_dc.keys())).replace("'", "").replace(" ", "")[1:-1]
    req = requests.request('GET', url)
    r = req.content.decode('utf-8')
    lines = r.splitlines()
    valid_lines = [i for i in lines if i[0]!='#']
    cols = valid_lines[0].split(' ')
    data_lines = [i.split('\t') for i in valid_lines[1:]]
    df = pd.DataFrame(data_lines, columns=cols)
    for i in df.columns:
        df.loc[df[i]=='', i] = np.nan
    df[float_cols] = df[float_cols].astype(float)
    df[int_cols] = df[int_cols].astype(int)
    return url, df


class Elodie:
    def __init__(self, obj):
        """
        Elodie class

        Parameters
        ----------
        obj (str) : object name

        Methods
        -------
        ccf : return Cross-Correlation Functions table
        spect : Spectra table
        """
        self.obj = obj
        self.BASE = 'http://atlas.obs-hp.fr/elodie/fE.cgi?'

    def ccf(self):
        """
        Elodie Cross-Correlation Functions table
        """
        url_ = self.BASE + f'n=e501&o={self.obj}&ob=jdb&a=csv&&d='
        int_cols = ['datenuit']
        float_cols = ['jdb','exptim','sn','vfit','sigfit','ampfit','ctefit']
        url, df = _get_df(url_, desc_el_ccf, int_cols, float_cols)
        print(url.replace('a=csv', 'a=htab'))
        return df

    def spec(self):
        """
        Elodie Spectra table
        """
        url_ = self.BASE + f'o={self.obj}&a=csv&d='
        int_cols = ['dataset']
        float_cols = ['exptime','sn','vfit','sigfit','ampfit']
        url, df = _get_df(url_, desc_el_spec, int_cols, float_cols)
        print(url.replace('a=csv', 'a=htab'))
        return df

    def get_spec(self, dataset, imanum, path=None, s1d=True):
        BASE = 'http://atlas.obs-hp.fr/elodie/E.cgi?'
        s1 = '&z=s1d' if s1d else ''
        PAR1 = f'&c=i&o=elodie:{dataset}/{imanum}'
        PAR2 = s1 + '&a=mime:application/x-fits'
        url = BASE + PAR1+ PAR2
        sp_typ = 's1d_' if s1d else 's2d_'
        filename = sp_typ + f'elodie_{dataset}_{imanum}.fits'
        path = '' if path is None else path
        urlretrieve(url, path+filename)

class Sophie:
    def __init__(self, obj):
        """
        Sophie class

        Parameters
        ----------
        obj (str) : object name

        Methods
        -------
        ccf : return Cross-Correlation Functions table
        spect : Spectra table
        """
        self.obj = obj
        self.BASE = 'http://atlas.obs-hp.fr/sophie/sophie.cgi?'

    def ccf(self):
        """
        Sophie Cross-Correlation Functions table
        """
        url_ = self.BASE + f'n=sophiecc&ob=bjd&a=csv&o={self.obj}&d='
        int_cols = ['seq','sseq','slen','nexp','expno','ccf_offline','maxcpp','lines']
        float_cols = ['bjd','rv','err','dvrms','fwhm','span','contrast','sn26']
        url, df = _get_df(url_, desc_so_ccf, int_cols, float_cols)
        print(url.replace('a=csv', 'a=htab'))
        return df

    def spec(self):
        """
        Sophie Spectra table
        """
        url_ = self.BASE + f'n=sophie&a=csv&ob=bjd&c=o&o={self.obj}&d='
        int_cols = ['seq','sseq','slen','nexp','expno']
        float_cols = ['bjd','sn26','exptime']
        url, df = _get_df(url_, desc_so_spec, int_cols, float_cols)
        print(url.replace('a=csv', 'a=htab'))
        return df

    def get_spec(self, seq, path=None, s1d=True):
        s1d = 's1d' if s1d==True else 'e2ds'
        url = self.BASE + f'c=i&a=mime:application/fits&o=sophie:[{s1d},{seq}]'
        filename = f'sophie_[{s1d},{seq}].fits'
        path = '' if path is None else path
        urlretrieve(url, path+filename)
