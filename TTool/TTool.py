import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
try:
    import quandl
except:
    pass
def t_cluster_max(data):
    d = data.copy()
    d.columns = range(len(d.columns))
    res = []
    mxi = len(data.columns)
    mx = len(data.columns)
    while len(d.corr()) > 1:
        cotd = -d.corr() + 2*np.identity(len(d.columns))
        scode1 = (cotd).min().idxmin()
        scode2 = (cotd)[scode1].idxmin()
        corr = d.corr()[scode1][scode2]
        d1 = d.pop(scode1)
        d2 = d.pop(scode2)
        
        s1 = d1.std(ddof = 0)
        s2 = d2.std(ddof = 0)
        w = min(max((2*s2**2 - 2*s1*s2*corr)/(2*s1**2+2*s2**2-4*s1*s2*corr),0),1)
        d[mx] = w*d1 + (1-w)*d2
        mx += 1
        m = 0
        if scode1 >= mxi:
            m+=res[scode1-mxi][3]
        else:
            m+=1
        if (scode2) >= mxi:
            m+=res[scode2-mxi][3]
        else:
            m+=1
        res.append([scode1,scode2,1/(corr+2),m])
    return np.array(res)

def t_cluster_min(data):
    d = data.copy()
    d.columns = range(len(d.columns))
    res = []
    mxi = len(data.columns)
    mx = len(data.columns)
    while len(d.corr()) > 1:
        scode1 = (d.corr()).min().idxmin()
        scode2 = (d.corr())[scode1].idxmin()
        corr = d.corr()[scode1][scode2]
        d1 = d.pop(scode1)
        d2 = d.pop(scode2)
        s1 = d1.std(ddof = 0)
        s2 = d2.std(ddof = 0)
        w = min(max((2*s2**2 - 2*s1*s2*corr)/(2*s1**2+2*s2**2-4*s1*s2*corr),0),1)
        d[mx] = w*d1 + (1-w)*d2
        mx += 1
        m = 0
        if scode1 > mxi:
            m+=res[scode1-mxi][3]
        else:
            m+=1
        if (scode2) > mxi:
            m+=res[scode2-mxi][3]
        else:
            m+=1
        res.append([scode1,scode2,corr+1,m])
    return np.array(res)

def t_corr_group(typ = 'max',data = None,gamount = 4):
    assert data is not None
    assert typ in ['max','min']
    assert gamount > 2
    res = []
    d = data.copy()
    while len(d.columns)>gamount:
        cols = list(d.columns)
        Z = None
        sp = []
        group = []
        if typ == 'max':
            Z = t_cluster_max(d)
        else:
            Z = t_cluster_min(d)
        for i in range(0,len(Z)):
            if Z[i][3] >= gamount:
                sp = [Z[i][0],Z[i][1]]
                while len(sp):
                    s = sp.pop()
                    if s >= len(cols):
                        sp.append(Z[int(s-len(cols))][0])
                        sp.append(Z[int(s-len(cols))][1])
                    else:
                        group.append(cols[int(s)])
                        d.pop(cols[int(s)])
                res.append(group)
                break
    if len(d.columns):
        res.append(list(d.columns))
    return res

def quandl_data_getter(scodes,attr = 'Close',quandl_apikey = None):
    quandl.ApiConfig.api_key = quandl_apikey
    res = pd.DataFrame()
    res_p = pd.DataFrame()
    assert attr in ['Close','Open','High','Low','Volume']
    for scode in scodes:
        dt = quandl.get("EOD/"+scode.replace(".","_"))
        s = dt[attr]
        split = dt['Split']
        sidx = split[split!=1].index
        for idx in sidx:
            s.loc[:idx] = s.loc[:idx]/split.loc[idx]
            s.loc[idx] = s.loc[idx]*split.loc[idx]
        res[scode] = (s-s.shift(1))/s.shift(1)
        res_p[scode] = s
    res = res.dropna()
    res_p = res_p.loc[res.index]
    quandl.ApiConfig.api_key = None
    return res,res_p

T_indices = ['UVXY','VCSH','SHV','IWM','RSX','VIIX','PSQ','UPRO','QLD','QID','QQQX','SPY','SSO','UCO','SDS','SH','SPXU','SQQQ','UDOW','DDM','VIXM',
'VXZ','VIXY','VXX','SPXL']
T_sectors = ['XLE','XLI','XLK','XLU','XLP','XLY','XLRE','XLB','XLF'] 

