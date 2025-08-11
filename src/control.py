from .model import Model
from .view import View

class Control(object):
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

        self.do_auto_detect()

        self.view.add_callbacks({
            "do_auto_detect": self.do_auto_detect,
            "change_path": self.change_path,
            "change_slide": self.change_slide,
            "do_export": self.do_export
        })
    
        self.view.bind_callbacks()
        
        self.view.run()
        
    def do_auto_detect(self):
        is_detected = self.model.auto_detect()
        if is_detected:
            self.view.set_path(self.model.path)
            self.view.set_slide(self.model.curr_slide)
            self.view.set_max(self.model.max_slide)        
        
    def change_path(self, path: str):
        try:
            self.model.get_pptx_info(path)
            
            self.view.set_path(self.model.path)
            self.view.set_max(str(self.model.max_slide))
            self.view.set_slide(str(self.model.curr_slide))
            
        except Exception as e:
            print(e)
            return
    
    def change_slide(self, value: str):
        try:
            # Validate the slide
            validate = ""
            for ch in value:
                if not ch.isnumeric():
                    continue
                validate += ch
            
            if validate == "":
                self.view.set_slide("")
                return
            
            slide = int(validate)
            if slide <= 0:
                slide = 1
            elif slide > self.model.max_slide:
                slide = self.model.max_slide
            
            self.model.set_slide(slide)
            self.view.set_slide(str(slide))
            
        except Exception as e:
            print(e)
    def do_export(self, path: str, format: str):
        try:
            self.model.export_slide(path, format)
        except Exception as e:
            print(e)