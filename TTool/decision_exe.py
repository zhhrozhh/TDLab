def market_decision_exe(p,s_diff):
    for scode in s_diff.index:
        n = s_diff.loc[scode]
        if n>0:
            p.market_buy(scode,int(n))
        elif n<0:
            p.market_sell(scode,int(-n))

def sell_first_decision_exe(p,s_diff):
    for scode in s_diff.index:
        n = s_diff.loc[scode]
        if n<0:
            p.market_sell(scode,int(-n))
    for scode in s_diff.index:
        n = s_diff.loc[scode]
        if n>0:
            p.market_buy(scode,int(-n))
            