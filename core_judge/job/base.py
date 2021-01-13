



class JobBase(object):
    
    def __init__(self,**kwargs):
        for item in kwargs.keys():
            self.item = kwargs[item]
    

    def run(self):
        raise Exception('IMPLEMENT')

    def prepare_file(self):
        raise Exception("implement")

    def update_status(self,log):
        raise Exception("implement")

    def eval_status(self):
        self.sandbox.cleanup()