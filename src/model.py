import os
import win32com.client
import pywintypes
import win32api

class Model(object):
    is_active: bool
    path: str
    curr_slide: int
    max_slide: int

    def __init__(self):
        object.__init__(self)
        self.reset_props()
    
    def reset_props(self):
        self.is_active = False
        self.path = ""
        self.curr_slide = 0
        self.max_slide = 0
        
    def auto_detect(self):
        app = self.get_active_pp()
        if app is None:
            # No powerpoint app is open
            self.reset_props()
            return False
            
        if len(app.Presentations) == 0:
            # No file opened
            self.reset_props()
            return False
        
        try:
            active_presentation = app.ActivePresentation
            if active_presentation.FullName == "":
                print("No active presentation")
                self.reset_props()
                return
            self.is_active = True
            self.path = active_presentation.FullName
            self.curr_slide = 1
            self.max_slide = len(active_presentation.Slides)            
            return True
        except:
            # No active presentation
            self.reset_props()
            return False
            
            
        
    def get_active_pp(self):
        try:
            active = win32com.client.GetActiveObject("PowerPoint.Application")
            return active
        except Exception as e:
            return None

    def get_pptx_info(self, path: str):
        if not os.path.exists(path):
            raise Exception("The path does not exist!")
        if not os.path.isfile(path):
            raise Exception("The path is not a file!")
        
        try:
            app = win32com.client.Dispatch("PowerPoint.Application")
            pptx = app.Presentations.Open(path, WithWindow=False)
            
            self.is_active = False
            self.path = path
            self.curr_slide = 1
            self.max_slide = len(pptx.Slides)
            
            pptx.Close()
            app.Quit()
        except Exception as e:
            raise Exception(f"Failed to open PowerPoint file: {e}")
        finally:
            try:
                app.Quit()
            except Exception as e:
                pass
    
    def set_slide(self, slide: int):
        self.curr_slide = slide

    def export_slide(self, export_path: str, format: str):                
        try:
            c_export_path = os.path.abspath(export_path)
            
            if self.is_active:
                app = self.get_active_pp()
                if app is None:
                    return
                pp = app.ActivePresentation
                pp.Slides[self.curr_slide-1].Export(
                    c_export_path,
                    format
                )
            else:
                app = win32com.client.Dispatch("PowerPoint.Application")
                pp = app.Presentations.Open(self.path, WithWindow=False)
                pp.Slides[self.curr_slide-1].Export(
                    c_export_path,
                    format
                )
            
                pp.Close()
                app.Quit()
        except pywintypes.com_error as e:
            info = e.excepinfo[5]
            errstring = win32api.FormatMessage(info)
            raise Exception(f"Failed to export the slide: {errstring}")
        except Exception as e:
            raise Exception(f"Failed to export the slide: {e}")
        finally:
            try:
                if not self.is_active:
                    app.Quit()
            except Exception as e:
                pass