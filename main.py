import kivy
kivy.require('2.2.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
#from kivy.core.image import Image
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy import platform
from kivy.logger import Logger

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    from android.permissions import request_permissions, Permission
    from android.storage import app_storage_path
    View = autoclass('android.view.View')

    settings_path = app_storage_path()

import numpy as np
import cv2 as cv
#from PIL import Image

class CameraWidget(Screen):
    
    #camera = ObjectProperty(None)
    
    #def cappic(self, dt):
        #filename = 'captured_image.png'
        #self.camera.export_to_png(filename)
        #self.camera.play = False
        
    def capture(self):
        #self.camera.play = True
        #Clock.schedule_once(self.cappic, 5)
        camera = self.ids['camera']
        #filename = settings_path + 'captured_image.png'
        camera.export_to_png(./captured_image.png')
        Logger.info('CamPr: Picture hopefully taken.')

        #texture = self.cameraObject.texture
        #size=texture.size
        #pixels = texture.pixels
        #pil_image=Image.frombytes(mode='RGBA', size=size,data=pixels)
        #numpypicture=numpy.array(pil_image)

class ContourImageWidget(Screen):
    
    image = ObjectProperty(None)
    sldr = ObjectProperty(None)
    
    def drawconts(self):
        imname = self.image.source
        print(imname[-7:])
        if imname[-7:] == '_ct.png':
            imname = imname[0:-7] + '.png'
            self.image.source = imname
        try:
            imc = cv.imread(cv.samples.findFile('captured_image.png'))
        except: 
            try:
                imc = cv.imread(cv.samples.findFile('./captured_image.png'))
                except:
                    Logger.info('CamPr: Epic Fail.')
            else:
                Logger.info('CamPr: Dot Slash')
                imname = './captured_image.png'
        else:
            Logger.info('CamPr: Default')
            imname = 'captured_image.png'
        print(imname)
        Logger.info('CamPr: This is a info message.')
        imc = cv.imread(cv.samples.findFile(imname))
        #cop = imc.copy()
        cop = cv.medianBlur(imc, 11)
        grsc = cv.cvtColor(cop, cv.COLOR_RGB2GRAY)
        ret, thresh = cv.threshold(grsc, self.sldr.value, 255, cv.THRESH_BINARY_INV)
        #if (thresh.item(10, 10) == 255):
        #    thresh = 255 - thresh
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(thresh, contours, -1, (255, 255, 255), 6)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        imc_copy = imc.copy()
        cv.drawContours(imc_copy, contours, -1, (0, 255, 0), 2)
        
        filename = imname[0:-4] + '_ct.png'
        print(filename)
        cv.imwrite(filename, imc_copy)
        self.image.source = filename

class HelloApp(App):

    def build(self):
        request_permissions([
            Permission.CAMERA,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
        #request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        #Window.size = (480, 800)
        sm = ScreenManager()
        sm.add_widget(CameraWidget(name='cam'))
        sm.add_widget(ContourImageWidget(name='cont'))
        
        return sm

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True
        else:           
            return False

    def on_pause(self):
        return True



if __name__ == '__main__':
    HelloApp().run()
