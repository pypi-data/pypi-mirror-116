def remove_fixed_target(propread,target_number,do_remove_visits=True,verbal=True):
    ##### target_number = string of 'Target_Number:' to be removed.
    ########## This assumes 'Target_Number:' starting each fixed target section.
    ##### json_template = e.g., fixed_target.json to read the string format, to count for the number lines to be removed.
    ##### outname = path to write the updated .prop file.
    ##### do_remove_visits = bool. If True, all visits associating with the target will be removed.
    from rolling_snapshot_proposal_editor.templatehandler import TemplateHandler
    from rolling_snapshot_proposal_editor.find_targetname_in_targetlist import find_targetname_in_targetlist
    from rolling_snapshot_proposal_editor.find_targetname_in_visits import find_targetname_in_visits
    template_dict = TemplateHandler().read('fixed_target')
    keys = list(template_dict.keys())
    N = len(keys)
    #####
    if verbal: print('read target name ... \n')
    target_name_list = find_targetname_in_targetlist(propread,verbal=verbal)
    for ii,i in enumerate(target_name_list):
        if target_name_list[ii][1] == target_number:
            target_name = target_name_list[ii][2]
            break
    #####
    if verbal: print('find line number ...\n')
    linenum = None
    for ii,i in enumerate(propread):
        tt = i.split()
        try:
            if tt[0]=='{0}:'.format(keys[0]):
                if tt[1]==target_number: # 1-indexing
                    linenum = ii
                    break
        except:
            pass
    print(linenum)
    #####
    if verbal: print('remove ...\n')
    t1 = propread[:linenum-1]
    t2 = propread[linenum+N:]
    t0 = t1
    t0.append(t2)
    return t0
    #####
    if do_remove_visits:
        from rolling_snapshot_proposal_editor.remove_visit import remove_visit
        if verbal: print('Removing visits associating with target number {0}, target name {1} ...\n'.format(target_number,target_name))
        visit_targetname_list = find_targetname_in_visits(propread)
        for ii,i in enumerate(visit_targetname_list):
            _,visitnumber,visittargetname = visit_targetname_list[ii]
            if visittargetname == target_name:
                t0 = remove_visit(t0,visitnumber,verbal=verbal)
    #####
    if verbal: print('Finish ...\n')
    return t0
