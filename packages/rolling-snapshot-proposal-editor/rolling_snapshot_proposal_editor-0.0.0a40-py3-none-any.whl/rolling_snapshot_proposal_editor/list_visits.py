def list_visits(propread,verbal=True):
    ##### internally used
    dictvisits = {}
    t0 = propread
    #####
    if verbal: print('Listing visits ...\n')
    for ii,i in enumerate(t0):
        try:
            if i.split()[0]=='Visit_Number:':
                dictvisits[i.split()[-1]] = ii # 0-indexing
        except:
            pass
    #####
    if verbal: print('Finish ...\n')
    return dictvisits
