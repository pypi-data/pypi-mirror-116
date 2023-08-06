def remove_visit(propread,visitnumber,verbal=True):
    ##### propfile = path to .prop file to be edited. This file will be open, but will not be changed; changes will be implemented and saved to a new file specified by outname.
    ##### outname = path to write the updated .prop file.
    ##### visitnumber = two-digit string satisfied proposal requirements
    ##### Note: last visit is assumed to be at the last section of the prop file.
    from rolling_snapshot_proposal_editor.list_visits import list_visits
    dictvisits = list_visits(propread,verbal=verbal)
    print('here')
    return dictvisits
    print('not here')
    #####
    if verbal: print('Finding line indices for visit number {0}...\n'.format(visitnumber))
    line_start,line_stop = None,None
    stop_at_eof = False
    for ii,i in enumerate(dictvisits.keys()):
        print(i,visitnumber)
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
        line_stop = len(propread)+1
        print('Line stop {0} at EOF\n'.format(line_stop))   
        stop_at_eof = True
    #####
    t1 = propread[:line_start-1]
    t3 = propread[line_stop:]
    #####
    print('Removing {0} ...\n'.format(visitnumber))
    propout = t1
    propout.append(t3)
    print('Finish.\n')
    return propout
