class EditPropFile:
    """
    This class handles editing prop file.
    #####
    Usage:
    1: Initialization -- t = EditPropFile(propfile)
    2: Profiling -- t = EditPropFile(propfile); t.profiling(keyword='Visit_Number:',prop=t.prop)
    3: Remove -- t = EditPropFile(propfile); t.remove(section,info)
    4: Add -- ???
    5: Save -- ???
    """
    def __init__(self,propfile,verbal=True,read_propfile=True):
        import copy
        self.propfile = propfile
        self.verbal = verbal
        if read_propfile: 
            self.prop = self._read_propfile()
            self.newprop = copy.deepcopy(self.prop)
            if self.verbal: print('Access by self.prop. \n')
    def _read_propfile(self):
        if self.verbal: print('Read propfile.\n')
        f = open(self.propfile,'r')
        t = f.readlines()
        f.close()
        return t
    ####################
    ####################
    ####################
    def profiling(self,keyword,prop,this_verbal=True):
        ##### keyword = str e.g., 'Target_Number:'. Note that most keywords in propfile will have a comma ':' at the end.
        ##### This function returns line index (0-indexing) and content of the line in propfile given the keyword
        from rolling_snapshot_proposal_editor.templatehandler import TemplateHandler
        if this_verbal: print("""Search keyword: '{0}'\n""".format(keyword))
        output = []
        for ii,i in enumerate(prop):
            if keyword in i.split():
                output.append((ii,i))
        if this_verbal: print('Return profile ...\n')
        return output
    ####################
    ####################
    ####################
    def add(self):
        pass
    ####################
    ####################
    ####################
    def remove(self,section,info,this_verbal=True):
        ##### [section,info] = ['fixed_target','target_number'], ['visit','visit_number']
        if section=='fixed_target':
            from rolling_snapshot_proposal_editor.remove_fixed_target import remove_fixed_target
            prop = self.newprop
            try:
                target_number = info['target_number']
                do_remove_visits = info['do_remove_visits']
            except:
                print("""Error: for section='fixed_target', info = {'target_number':str,'do_remove_visits':bool}\n""")  
            self.newprop = remove_fixed_target(prop,target_number,do_remove_visits,verbal=this_verbal)
            if this_verbal: print('Access by self.newprop.\n')
    ####################
    ####################
    ####################
    def save(self,outpath):
        print('Creating {0} ...\n'.format(outname))
        f = open(outpath,'w')
        f.writelines(self.newprop)
        f.close()   
####################
####################
####################
    