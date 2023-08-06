def remove_visit(propread,visitnumber,verbal=True):
    ##### propfile = path to .prop file to be edited. This file will be open, but will not be changed; changes will be implemented and saved to a new file specified by outname.
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
        f = open(propfile,'r')
        t0 = f.readlines()
        f.close() 
        line_stop = len(t0)+1
        print('Line stop {0} at EOF\n'.format(line_stop))   
        stop_at_eof = True
    #####
    print('Grabbing the original file ...\n')
    f = open(propfile,'r')
    t0 = f.readlines()
    t1 = t0[:line_start-1]
    t3 = t0[line_stop:]
    f.close()
    #####
    print('Creating {0} ...\n'.format(outname))
    f = open(outname,'w')
    #####
    print('Removing {0} ...\n'.format(visitnumber))
    f.writelines(t1)
    if not stop_at_eof:
        f.writelines('\n')
        f.writelines(t3)
        f.writelines('\n')
    print('Finish.\n')
