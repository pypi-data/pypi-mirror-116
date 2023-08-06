def find_targetname_in_targetlist(propread,verbal=True):
    ##### return a list of tuples. Each tuple = (x,y,z) where x = line index (0-indexing), y = target number, and z = target name
    from rolling_snapshot_proposal_editor.editpropfile import EditPropFile
    if verbal: print('Getting a list of target numbers ...\n')
    target_number_list = EditPropFile(propfile=None,read_propfile=False).profiling(keyword='Target_Number:',prop=propread,this_verbal=verbal)
    #####
    if verbal: print('Matching with target name ...\n')
    target_name_list = []
    t0 = propread
    for i in target_number_list:
        ti = i[0]
        t1 = t0[ti:]
        for jj,j in enumerate(t1):
            try:
                tk = j.split()[0]
            except:
                continue
            if j.split()[0] == 'Target_Name:':
                target_name_list.append(j.split()[-1]) 
                break
    #####
    if verbal: print('Preparing output ...\n')
    output = []
    for ii,i in enumerate(target_number_list):
        t1 = target_number_list[ii][0]
        t2 = target_number_list[ii][1].split()[-1]
        t3 = target_name_list[ii]
        output.append((t1,t2,t3))
    #####
    if verbal: print('Finish.')
    return output
