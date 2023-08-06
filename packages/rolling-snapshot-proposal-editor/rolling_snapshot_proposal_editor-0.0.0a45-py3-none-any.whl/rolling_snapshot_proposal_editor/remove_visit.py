def remove_visit(propread,visitnumber,verbal=True):
    ##### visitnumber = two-digit string satisfied proposal requirements
    ##### Note: last visit is assumed to be at the last section of the prop file.
    from rolling_snapshot_proposal_editor.list_visits import list_visits
    dictvisits = list_visits(propread,verbal=verbal)
    #####
    if verbal: print('Finding line indices for visit number {0}...\n'.format(visitnumber))
    line_start,line_stop = None,None
    stop_at_eof = False
    for ii,i in enumerate(dictvisits.keys()):
        if i==visitnumber:
            line_start = dictvisits[i]
            print('Line start {0}\n'.format(line_start))
            dictindex = ii
            continue
        if line_start and ii==dictindex+1:
            line_stop = dictvisits[i]
            print('Line stop {0}\n'.format(line_stop))
            continue
    if not line_stop:
        t0 = propread
        line_stop = len(t0)+1
        print('Line stop {0} at EOF\n'.format(line_stop))   
        stop_at_eof = True
    #####
    print('Removing {0} ...\n'.format(visitnumber))
    t0 = propread
    t1 = t0[:line_start-1]
    t3 = t0[line_stop:]
    t = t1
    t.append(t3)
    #####
    print('Finish.\n')
    return t
