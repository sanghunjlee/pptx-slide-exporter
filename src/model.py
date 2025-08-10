import os

class Model(object):
    path: str
    curr_slide: int
    max_slide: int

    def __init__(self):
        object.__init__(self)

        path = ""
        curr_slide = 0
        max_slide = 0

    def get_pptx_info(self, path: str):
        if not os.path.exists(path):
            raise Exception("The path does not exist!")
        if not os.path.isfile(path):
            raise Exception("The path is not a file!")
        
        self.path = path
        