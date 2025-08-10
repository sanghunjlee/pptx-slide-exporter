from .view import View

class Control(object):
    def __init__(self, model, view: View):
        self.model = model
        self.view = view

        self.view.add_callbacks({
            "change_slide": self.change_slide
        })
    
    def change_slide(self, value: str):
        try:
            # Validate the slide
            validate = ""
            for ch in value:
                if not ch.isnumeric():
                    continue
                validate += ch
            if validate == "":
                
                return
            int_value = int(value)

        except Exception as e:
            print(e)