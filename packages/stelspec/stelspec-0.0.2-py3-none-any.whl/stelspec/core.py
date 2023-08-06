import numpy as np
import pandas as pd
import requests
from urllib.request import urlretrieve
from .columns import desc_el_ccf, desc_el_spec, desc_so_ccf, desc_so_spec

def _get_df(base, col_dc, int_cols, float_cols):
    url = base + str(list(col_dc.keys())).replace("'", "").replace(" ", "")[1:-1]
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

def elodie_ccf(obj):
    """
    Elodie Cross-Correlation Functions table
    """
    BASE = f'http://atlas.obs-hp.fr/elodie/fE.cgi?n=e501&o={obj}&ob=jdb&a=csv&&d='
    int_cols = ['datenuit']
    float_cols = ['jdb','exptim','sn','vfit','sigfit','ampfit','ctefit']
    url, df = _get_df(BASE, desc_el_ccf, int_cols, float_cols)
    print(url.replace('a=csv', 'a=htab'))
    return df

def elodie_spec(obj):
    """
    Elodie Spectra table
    """
    BASE = f'http://atlas.obs-hp.fr/elodie/fE.cgi?o={obj}&a=csv&d='
    int_cols = ['dataset']
    float_cols = ['exptime','sn','vfit','sigfit','ampfit']
    url, df = _get_df(BASE, desc_el_spec, int_cols, float_cols)
    print(url.replace('a=csv', 'a=htab'))
    return df

def sophie_ccf(obj):
    """
    Sophie Cross-Correlation Functions table
    """
    BASE = f'http://atlas.obs-hp.fr/sophie/sophie.cgi?n=sophiecc&ob=bjd&a=csv&o={obj}&d='
    int_cols = ['seq','sseq','slen','nexp','expno','ccf_offline','maxcpp','lines']
    float_cols = ['bjd','rv','err','dvrms','fwhm','span','contrast','sn26']
    url, df = _get_df(BASE, desc_so_ccf, int_cols, float_cols)
    print(url.replace('a=csv', 'a=htab'))
    return df

def sophie_spec(obj):
    """
    Sophie Spectra table
    """
    BASE = f'http://atlas.obs-hp.fr/sophie/sophie.cgi?n=sophie&a=csv&ob=bjd&c=o&o={obj}&d='
    int_cols = ['seq','sseq','slen','nexp','expno']
    float_cols = ['bjd','sn26','exptime']
    url, df = _get_df(BASE, desc_so_spec, int_cols, float_cols)
    print(url.replace('a=csv', 'a=htab'))
    return df
