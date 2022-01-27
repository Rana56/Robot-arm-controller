from kivy.app import App                                                            #imports
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition            #Or, CardTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

import time, os, serial, serial.tools.list_ports, sys
import numpy as np

#App windows - Represents screens
class MainMenu(Screen):                                                             #Main Menu Screen
    def __init__(self):
        super(MainMenu, self).__init__(name='main')

        with self.canvas.before:                                                    #This code the background colour
            Color(.953125,.6328125,.37890625)                                       #This sets the colour
            self.rect = Rectangle(size = self.size, pos = self.pos)                 #A rectangle is created covering the whole window
        self.bind(size= self.rect_update, pos = self.rect_update)

        box_lay = BoxLayout(orientation='vertical')                                 #creates a Boxlayout
        self.add_widget(box_lay)

        slider_button = Button(                                                     #creates a button object, with all its properties
            text='Slider Mode',                                                     #Slider Button
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.35},
            on_release=self.go_slider,
        )
        code_button = Button(
            text='Code Mode',                                                       #parameters of button - name, position, size
            size_hint=(0.3, 0.3),                                                   #Code Button
            pos_hint={'x': 0.35},
            on_release=self.go_code,
        )
        settings_button = Button(
            text='Settings',                                                        #Settings Button
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.35},
            on_release=self.go_setting,
        )

        box_lay.add_widget(slider_button)                                           #Adds the button obejects to the boxlayout through composition
        box_lay.add_widget(code_button)
        box_lay.add_widget(settings_button)

        float_lay = FloatLayout()
        self.add_widget(float_lay)
                                                                                    #Label for title, the label will always be the size of the layout minus the pos_hint percentages on each side
        title = Label(text='Main Menu', bold=True, color=(.2,.5,.65,1),  font_size='30sp', pos_hint={'x':-0.39,'y':0.46})
        float_lay.add_widget(title)

        main_menu_info_1 = Label(text='Welcome to the main menu\nClick on a button!', bold=True, color=(.2,.5,.65,1),  font_size='15sp', pos_hint={'x':-0.37,'y':0.39})
        float_lay.add_widget(main_menu_info_1)

        main_menu_info_2 = Label(text='Clicking on one of these buttons\nwill direct you a different screen!', bold=True, color=(.2,.5,.65,1),  font_size='15sp', pos_hint={'x':0.34,'y':-0.44})
        float_lay.add_widget(main_menu_info_2)

    #Methods
    def rect_update(self, instance, value):                                         #Method to update the shape of rectangle relative to the shape of window
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_slider(self, *args):                                                     #Method to complete action after button is pressed
        App.get_running_app().root.current = 'slider_m'                             #This line changes the screen to 'slider_m'
        # or
        # self.manager.current = 'slider_m'                                         #A different way to change screens

    def go_code(self, *args):
        App.get_running_app().root.current = 'code_m'
        # or
        # self.manager.current = 'code_m'

    def go_setting(self, *args):
        self.manager.current = 'setting_m'

class SliderMode(Screen):                                                            #SliderMode Screen
    def __init__(self):
        super(SliderMode, self).__init__(name='slider_m')

        with self.canvas.before:
            Color(.953125,.6328125,.37890625)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size= self.rect_update, pos = self.rect_update)

        main_grid_lay = GridLayout(cols=2, cols_minimum={0:20, 1:500})
        self.add_widget(main_grid_lay)

        btn_box_lay = BoxLayout(orientation='vertical')                             #Creates a box layout
        main_grid_lay.add_widget(btn_box_lay)

        menu_btn = Button(                                                          #Button for Menu
            text='Menu',
            size_hint=(1, 1),
            on_release=self.go_main,
        )
        btn_box_lay.add_widget(menu_btn)                                            #adds the button to the box layout

        robot_info_btn = Button(                                                    #Button for Robot picture
            text='Robot Info',
            size_hint=(1, 1),
            on_release=self.rbt_info,
        )
        btn_box_lay.add_widget(robot_info_btn)

        reset_btn = Button(                                                         #Button for reset
            text='Reset',
            size_hint=(1, 1),
            on_release=self.reset_values,
        )
        btn_box_lay.add_widget(reset_btn)

        slider_grid_lay = GridLayout(cols=3)                                        #Creates a GridLayout thorugh composition and has 3 colums
        main_grid_lay.add_widget(slider_grid_lay)

        self.grip_l = Label(text='Gripper')                                         #Creates a label object with its text
        self.grip_value = Label(text='90°')                                         #Creates a label to show slider value
        self.grip_slide = Slider(                                                   #Creates a slider object with its parameters
            min=0,                                                                  #Slider for Gripper
            max=180,
            value=90,
        )
        slider_grid_lay.add_widget(self.grip_l)                                     #adds the label and slider to the gridlayout
        slider_grid_lay.add_widget(self.grip_slide)
        slider_grid_lay.add_widget(self.grip_value)


        self.elbow_l = Label(text='Elbow')
        self.elbow_value = Label(text='90°')
        self.elbow_slide = Slider(                                                  #Slider for Elbow
            min=0,
            max=180,
            value=90,
        )
        slider_grid_lay.add_widget(self.elbow_l)
        slider_grid_lay.add_widget(self.elbow_slide)
        slider_grid_lay.add_widget(self.elbow_value)


        self.shldr_l = Label(text='Shoulder')
        self.shldr_value = Label(text='90°')
        self.shldr_slide = Slider(                                                  #Slider for Shoulder
            min=0,
            max=180,
            value=90,
        )
        slider_grid_lay.add_widget(self.shldr_l)
        slider_grid_lay.add_widget(self.shldr_slide)
        slider_grid_lay.add_widget(self.shldr_value)
        #

        self.base_l = Label(text='Base')
        self.base_value = Label(text='90°')
        self.base_slide = Slider(                                                   #Slider for Base
            min=0,
            max=180,
            value=90,
        )
        slider_grid_lay.add_widget(self.base_l)
        slider_grid_lay.add_widget(self.base_slide)
        slider_grid_lay.add_widget(self.base_value)

        self.grip_slide.bind(value=self.grip_s_value, on_touch_move=self.robot_move, on_touch_down=self.robot_move)                               #Gets the value of the sliders
        self.elbow_slide.bind(value=self.elbow_s_value, on_touch_move=self.robot_move, on_touch_down=self.robot_move)                            #Sends value to update_ function
        self.shldr_slide.bind(value=self.shldr_s_value, on_touch_move=self.robot_move,on_touch_down=self.robot_move)
        self.base_slide.bind(value=self.base_s_value, on_touch_move=self.robot_move, on_touch_down=self.robot_move)

        port = arduino()
        self.ser = serial.Serial(port, 115200)

    #Methods
    def robot_move(self,*args):
        try:
            time.sleep(.1)                                                                                 #Time delay
            self.ser.write(b"A%dB%dC%dD%d" % (self.base_slide.value, self.shldr_slide.value, self.elbow_slide.value, self.grip_slide.value))             #Sends value to arduino
        except:
            print('Not Connected')


    def rect_update(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_main(self, *args):
        self.manager.current = 'main'

    def rbt_info(self, *args):                                                      #Displays a labled robot arm picture
        try:
            self.robotpic = Image(source= 'robot_arm.png')#, allow_strech =True)
            self.robotpic_popup = Popup(title='Labeled Robot', content=self.robotpic, size_hint=(0.43, 0.4))
            self.robotpic_popup.open()
        except:
            print('Image Not Found')

    def reset_values(self, instance):                                               #Resets the slider to it's original position
        self.grip_slide.value = 90
        self.elbow_slide.value = 90
        self.shldr_slide.value = 90
        self.base_slide.value = 90

    def grip_s_value(self, instance, value):                                        #Rounds the value of the sliders and displays the degrees
        self.grip_value.text = str(int(value)) + '°'

    def elbow_s_value(self, instance, value):
        self.elbow_value.text = str(int(value)) + '°'

    def shldr_s_value(self, instance, value):
        self.shldr_value.text = str(int(value)) + '°'

    def base_s_value(self, instance, value):
        self.base_value.text = str(int(value)) + '°'


class CodeMode(Screen):                                                              #Code Mode Screen
    def __init__(self):
        super(CodeMode, self).__init__(name='code_m')

        with self.canvas.before:
            Color(.953125,.6328125,.37890625)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size= self.rect_update, pos = self.rect_update)

        self.list_deg_arm = None                                                    #attribute for loaded data list

        float_lay = FloatLayout()
        self.add_widget(float_lay)

        load_button = Button(                                                        #Button to load
            text='Load Code',
            size_hint=(0.35,0.4),
            pos_hint={'x':0.1,'y':0.30},
            on_release= self.go_load,
            font_size=15
        )
        float_lay.add_widget(load_button)

        code_button = Button(                                                        #Button to create code
            text='Create Code',
            size_hint=(0.35,0.4),
            pos_hint={'x':0.55,'y':0.30},
            on_release= self.go_code_screen,
            font_size=15
        )
        float_lay.add_widget(code_button)

        menu_button = Button(                                                        #Button to go to menu
            text='Menu',
            size_hint=(0.18, 0.18),
            pos_hint={'x': 0.0, 'y': 0.0},
            on_release=self.go_main,
        )
        float_lay.add_widget(menu_button)

        title = Label(text='Code Mode', bold=True, color=(.2,.5,.65,1),  font_size='30sp', pos_hint={'x':-0.39,'y':0.46})                       #label for title
        float_lay.add_widget(title)

        main_menu_info = Label(text="Click on the 'Load code' to load previous code\nor 'Create Code' to create new code", bold=True, color=(.2,.5,.65,1),  font_size='15sp', pos_hint={'x':-0.295,'y':0.39})               #label for information
        float_lay.add_widget(main_menu_info)

        self.load_list = []

    #Methods
    def rect_update(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_main(self, *args):
        App.get_running_app().root.current = 'main'

    def go_code_screen(self, *args):
        App.get_running_app().root.current = 'code_screen'

    def go_load(self,*args):                                                        #opens load popup
        grid_lay = GridLayout(cols=1)
        self.file_lbl = Label(text='Enter a File name to load the code')
        grid_lay.add_widget(self.file_lbl)
        self.file_input = TextInput(multiline=False)
        grid_lay.add_widget(self.file_input)

        grid_lay2 = GridLayout(cols=2)
        grid_lay.add_widget(grid_lay2)

        open_btn = Button(text='Open',
                          on_release = self.open
        )
        grid_lay2.add_widget(open_btn)
        cancel_btn = Button(text='Cancel')
        grid_lay2.add_widget(cancel_btn)

        self.load_popup = Popup(title="Open file", content=grid_lay, size_hint=(0.5, 0.5))
        self.load_popup.open()
        cancel_btn.bind(on_release=self.load_popup.dismiss)                         #closes popup

    def open(self, *args):
        try:                                                                         #Opens the file
                self.list_deg_arm = np.loadtxt(self.file_input.text+'.txt', dtype=np.object)        #loads data to varible from text file
                self.list_deg_arm = self.list_deg_arm.tolist()                      #changes returned data to a list
                print(self.list_deg_arm)
                self.load_popup.dismiss()

                App.get_running_app().root.current = 'code_screen'
                CodeScreen().set_multi_list(self.list_deg_arm)
                print('test - CodeMode')
        except:
            self.file_lbl.text = 'File name not found. Please try again'            #Error message if file not found

    def get_list(self):                                                             #getter for list
        data_list = self.list_deg_arm                                               #TODO clear lists when changing screens
        print('getter')
        return data_list


class CodeScreen(Screen):                                                            #Screen to start coding the robot
    def __init__(self):
        super(CodeScreen, self).__init__(name='code_screen')

        with self.canvas.before:
            Color(.953125,.6328125,.37890625)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size= self.rect_update, pos = self.rect_update)

        main_grid_lay = GridLayout(cols=1)                                           #Creates a main grid layout with one coloum
        self.add_widget(main_grid_lay)                                               #adds the gridlayout to the screen

        second_grid_lay = GridLayout(cols=2, cols_minimum={0:640, 1:175})            #Create a second gridlayout
        main_grid_lay.add_widget(second_grid_lay)                                    #Adds the second gridlayout to the main grid

        #Code ouput display
        self.display_code = TextInput(readonly = True)                               #This displays the inputs of the user
        second_grid_lay.add_widget(self.display_code)                                #Adds a textinput box to the second gridlayout

        self.arm_code_queue = Queue()                                                # Queue for arm name
        self.degree_code_queue = Queue()                                             #Queue for degree code

        self.display_list = []                                                       #List Displayed to the user
        print('list below')
        self.list_deg_arm = []                                                       #List used to store instructions
        self.loaded_code = None
        self.load_count = 0

        #self.data_list = CodeMode().get_list()
        #print(self.data_list)

        #Options Buttons
        box_lay = BoxLayout(orientation='vertical')                                  #Creates and adds a boxlayout to the second gridlayout
        second_grid_lay.add_widget(box_lay)

        delete_button = Button(                                                      #Delete button
            text='Delete',
            size_hint_x= None,
            width=160,
            on_release= self.printl#self.input_delete
        )
        box_lay.add_widget(delete_button)

        run_button = Button(                                                         #Run button
            text='Run',
            size_hint_x= None,
            width=160,
            on_release= self.multi_list
        )
        box_lay.add_widget(run_button)

        save_button = Button(                                                        #Save button
            text='Save',
            size_hint_x= None,
            width=160,
            on_release= self.save_popup
        )
        box_lay.add_widget(save_button)

        menu_button = Button(                                                        #Menu button
            text='Menu',
            size_hint_x= None,
            width=160,
            on_release= self.alert_exit,
        )
        box_lay.add_widget(menu_button)


        #Control Buttons
        ctrl_grid_lay = GridLayout(cols=5)                                           #Creates a control grid layout and adds it to the main grid layout
        main_grid_lay.add_widget(ctrl_grid_lay)

        self.base_turn = Button(                                                     #TODO Save data onto text files and display
            text='Base Turn',                                                        #Base Turn Button
            on_release= self.degree_popup,
        )
        ctrl_grid_lay.add_widget(self.base_turn)
        self.base_turn.bind(on_release=self.base_clicked)                            #Binds the method to the button press

        self.shldr_turn = Button(
            text='Shoulder Turn',                                                    #Shoulder Turn button
            on_release=self.degree_popup,
        )
        ctrl_grid_lay.add_widget(self.shldr_turn)
        self.shldr_turn.bind(on_release=self.shldr_clicked)

        self.elbow_turn = Button(
            text='Elbow Turn',                                                       #Elbow Turn button
            on_release= self.degree_popup,
        )
        ctrl_grid_lay.add_widget(self.elbow_turn)
        self.elbow_turn.bind(on_release=self.elbow_clicked)

        self.grip_open = Button(
            text='Gripper Open/Close',                                               #Gripper button
            on_release=self.degree_popup,
        )
        ctrl_grid_lay.add_widget(self.grip_open)
        self.grip_open.bind(on_release=self.gripper_clicked)

        reset = Button(                                                               #Reset button
            text='Reset',
            on_release = self.reset_clicked
        )
        ctrl_grid_lay.add_widget(reset)

        robot_info = Button(                                                          #Button displays picture
            text ='Robot Info',
            on_release= self.rbt_info
        )
        ctrl_grid_lay.add_widget(robot_info)


    #Methods
    def rect_update(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_main(self, *args):
        App.get_running_app().root.current = 'main'

    def rbt_info(self, *args):                                                       #Robot arm picture popup
        try:
            self.robotpic = Image(source= 'robot_arm.png')
            self.robotpic_popup = Popup(title='Labeled Robot', content=self.robotpic, size_hint=(0.43, 0.4))
            self.robotpic_popup.open()
        except:
            print('Image Not Found')

    def base_clicked(self, instance):                                                  #Displays the user inputs
        self.arm_code_queue.enqueue('Base')
        self.display_list.append('Base: ')
        self.arm_code_queue.print()

    def shldr_clicked(self, instance):                                                 #Adds the string to the textbox
        self.arm_code_queue.enqueue('Shoulder')
        self.display_list.append('Shoulder: ')
        self.arm_code_queue.print()

    def elbow_clicked(self, instance):
        self.arm_code_queue.enqueue('Elbow')
        self.display_list.append('Elbow: ')
        self.arm_code_queue.print()

    def gripper_clicked(self, instance):
        self.arm_code_queue.enqueue('Gripper')
        self.display_list.append('Gripper: ')
        self.arm_code_queue.print()

    def reset_clicked(self, instance):
        self.arm_code_queue.enqueue('Reset')
        self.display_list.append('Reset')
        self.arm_code_queue.print()
        self.display_code.text = str(self.display_list)

    def dismiss_popup(self, obj):
        self.exitWindow.dismiss()

    def degree_popup(self, *args):                                                   #The Pop up input the angle
        grid_lay = GridLayout(cols=1)
        self.d_input = TextInput(text='Please enter the angle of degree you want to turn (0°-180°)')
        self.d_input.bind(focus=self.on_focus_delete)                                #binds on_focus method

        self.ok_btn = Button(
            text='Ok',
            on_release = self.degree_check
        )
        grid_lay.add_widget(self.d_input)
        grid_lay.add_widget(self.ok_btn)
        self.degreeWindow = Popup(title='Enter an Angle (0°-180°):', content= grid_lay, size_hint=(None, None), size=(300, 250), auto_dismiss = False)
        self.degreeWindow.open()

    def degree_check(self, instance):                                               #method that checks the inputted value
        try:                                                                        #exception handling
            degree_int = int(self.d_input.text)
            degree_str = self.d_input.text
            if degree_int <= 180 and degree_int >= 0:
                self.degree_code_queue.enqueue(degree_int)                          #queues the value
                self.degree_code_queue.print()                                      #prints the queue
                self.degree_add(degree_str)
                self.degreeWindow.dismiss()                                         #closes popup
            else:
                self.d_input.text = 'Please Enter a valid angle (0°-180°)'

        except:
            self.d_input.text = ''                                                  #Clears the input box
            self.d_input.text = 'Please Enter a valid angle (0°-180°)'              #Outputs this message if wrong value inputted

    def degree_add(self, degree):                                                   #Adds the degree and ouputs
        pop_value = self.display_list.pop(-1)                                       #Pops last value, adds the degree and appends it back
        add_deg = pop_value+degree+'°'
        self.display_list.append(add_deg)
        self.display_code.text = str(self.display_list)

    def on_focus_delete(self, instance, value):                                     #Method to clear the text box when pressed
        if value == True:
            self.d_input.text = ''                                                  #Clears box
        else:
            pass

    def set_multi_list(self, load):                                                 #sets value to list when file loaded
        self.loaded_code = load
        print(self.loaded_code)
        print('Setter Check')
        #self.check_load(self.loaded_code)
        #self.list_process(load)
        print(self.loaded_code[0][0])

    def check_load(self, load):
        if self.load_count == 0:                                                                     #Checks if code has been loaded more than once
            print('Check Load')
            if load == None:                                                                  #TODO Set load count to zero when exiting
                self.load_count += 1
                print('Nothing Loaded')

            else:#if load != None:
                self.list_process(load)
                self.load_count += 1
                print('Values Loaded')
        else:
            pass

    def list_process(self, load):

        for i in range(len(load)):
            print(i)
            for values in range(load[i]):
                print(values)
                self.arm_code_queue.enqueue(load[i][values])
                self.arm_code_queue.print()
                # if i == 0:
                #     self.arm_code_queue.enqueue(load[i][values])
                #     self.degree_code_queue.enqueue(load[i+1][values])
                #     self.arm_code_queue.print()
                #     self.degree_code_queue.print()
                # else:
                #     pass

        #TODO process list - for loops

    def printl(self, *args):
        #print(self.loaded_code)
        self.arm_code_queue.print()
        self.degree_code_queue.print()

    def multi_list(self, *args):                                                                #Multidimensional list

        self.list_deg_arm = [self.arm_code_queue.queue, self.degree_code_queue.queue]           # Queue for code
        print(self.list_deg_arm)                                                                # Stored in a 2d list

        base_ang = 90                                                                          #Initial angle of the servo
        shldr_ang = 90                                                                          #TODO have value asociated with reset so there isn't an empty space
        elbw_ang = 90
        grip_ang = 90

        port = arduino()
        ser = serial.Serial(port, 115200)                                                    #Creates a serial connection 'COM8'

        try:
            for i in range(len(self.list_deg_arm)):                                                #Goes through the list and executes the code
                for arm in range(len(self.list_deg_arm[i])):
                    if self.list_deg_arm[i][arm] == 'Base':
                        base_ang = self.list_deg_arm[i+1][arm]                                     #Gets the angle associated to the arm
                        print('base_ang', base_ang)
                        time.sleep(2)                                                              #Time delay
                        ser.write(b"A%dB%dC%dD%d" %(base_ang, shldr_ang, elbw_ang, grip_ang))                                #Sends the signal to the arduino

                    elif self.list_deg_arm[i][arm] == 'Shoulder':
                        shldr_ang = self.list_deg_arm[i+1][arm]
                        print('shldr_ang',shldr_ang)
                        time.sleep(2)
                        ser.write(b"A%dB%dC%dD%d" % (base_ang, shldr_ang, elbw_ang, grip_ang))

                    elif self.list_deg_arm[i][arm] == 'Elbow':
                        elbw_ang = self.list_deg_arm[i + 1][arm]
                        time.sleep(2)
                        ser.write(b"A%dB%dC%dD%d" % (base_ang, shldr_ang, elbw_ang, grip_ang))

                    elif self.list_deg_arm[i][arm] == 'Gripper':
                        grip_ang = self.list_deg_arm[i+1][arm]
                        time.sleep(2)
                        ser.write(b"A%dB%dC%dD%d" % (base_ang, shldr_ang, elbw_ang, grip_ang))

                    elif self.list_deg_arm[i][arm] == 'Reset':
                        base_ang = 90
                        shldr_ang = 90
                        elbw_ang = 90
                        grip_ang = 90
                        time.sleep(2)
                        ser.write(b"A%dB%dC%dD%d" % (base_ang, shldr_ang, elbw_ang, grip_ang))

                    else:
                        pass
        except:
          print('Not connected')

    def input_delete(self, *args):                                                  #Removes the last entered input from the queue
        try:                                                                            #exception handling in case index out of range
            if self.display_list[-1] == 'Reset':                                        #Check if last input is reset
                self.arm_code_queue.dequeue()
                del self.display_list[-1]
                self.display_code.text = str(self.display_list)
                self.arm_code_queue.print()
                self.degree_code_queue.print()
            else:
                self.degree_code_queue.dequeue()
                self.arm_code_queue.dequeue()
                del self.display_list[-1]                                                   #Deletes last values of the list
                self.display_code.text = str(self.display_list)                             #Displays the queue

                self.arm_code_queue.print()
                self.degree_code_queue.print()
        except:
            pass

    def alert_exit(self, *args):                                                    #Popup to alert user before exiting the screen
        grid_lay = GridLayout(cols=1)                                               #The buttons and labels will be added to this gridlayout
        content_lbl = Label(
            text='Want to save your changes? Exiting without saving will result in loss of work!',
        )
        grid_lay.add_widget(content_lbl)

        btn_gridlay = GridLayout(cols=3)
        grid_lay.add_widget(btn_gridlay)

        self.save_btn = Button(                                                     #Save Button
            text='Save',
            on_release= self.save_popup
        )
        btn_gridlay.add_widget(self.save_btn)
        self.save_btn.bind(on_release=self.dismiss_popup)
        self.no_save_btn = Button(                                                  #Doesn't save and goes to the menu
            text="Don't save",
            on_release= self.go_main
        )
        btn_gridlay.add_widget(self.no_save_btn)
        self.cancel_btn = Button(                                                   #Dismisses the pop up
            text="Cancel",
            on_release=self.dismiss_popup
        )
        btn_gridlay.add_widget(self.cancel_btn)

        self.exitWindow = Popup(title='Save', content=(grid_lay), size_hint=(0.7, 0.4), auto_dismiss = False)
        self.exitWindow.open()                                                      #opens the popup

        self.no_save_btn.bind(on_press=self.exitWindow.dismiss)                     #Binds a button press to a dissmiss method
        self.no_save_btn.bind(on_release=self.dont_save)                            #Doesn't save the data

    def dont_save(self, *args):                                                     #Clears the input box and the queues
        self.display_code.text = ''
        self.degree_code_queue.clear()
        self.arm_code_queue.clear()
        self.display_list = []

    #Save function
    def save_popup(self, *args):                                                   #Popup to save
        grid_lay = GridLayout(cols=1)
        self.file_lbl = Label(text='Enter a File name to save the code')
        grid_lay.add_widget(self.file_lbl)
        self.file_input = TextInput(multiline=False)
        grid_lay.add_widget(self.file_input)

        grid_lay2 = GridLayout(cols=2)
        grid_lay.add_widget(grid_lay2)

        self.save_btn = Button(text='Save', on_release = self.save)
        grid_lay2.add_widget(self.save_btn)
        self.cancel_btn = Button(text='Cancel')
        grid_lay2.add_widget(self.cancel_btn)

        self.save_pu = Popup(title="Save file", content=grid_lay, size_hint=(0.5, 0.5))
        self.save_pu.open()
        self.cancel_btn.bind(on_release = self.save_pu.dismiss)

    def save(self, *args):                                                          #writes the user's data onto a text file
        if self.file_input.text == '':
            self.file_lbl.text = 'Please enter a valid file name'                   #Check if the input is empty

        elif self.file_input.text != '':
            self.list_deg_arm = [self.arm_code_queue.queue, self.degree_code_queue.queue]

            np.savetxt(self.file_input.text+'.txt', self.list_deg_arm, fmt='%s')   #save list to text file

            self.file_input.text = ''                                               # Clears the input box
            self.save_pu.dismiss()


class SettingMode(Screen):                                                          #Settings Screen
    def __init__(self):
        super(SettingMode, self).__init__(name='setting_m')

        with self.canvas.before:
            Color(.953125,.6328125,.37890625)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size= self.rect_update, pos = self.rect_update)

        box_lay = BoxLayout(orientation='vertical')                                 #Creates a box layout
        self.add_widget(box_lay)

        info_button = Button(                                                       #Button for info
            text='Information',
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.35},
            on_release=self.info_btn,
        )
        box_lay.add_widget(info_button)

        review_button = Button(                                                     #Button to rate
            text='Rate!',
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.35},
            on_release=self.rate,
        )
        box_lay.add_widget(review_button)

        exit_button = Button(                                                       #Button to exit
            text='Exit',
            size_hint=(0.3, 0.3),
            pos_hint={'x': 0.35},
            on_release=self.exit_app,
        )
        box_lay.add_widget(exit_button)

        float_lay = FloatLayout()
        self.add_widget(float_lay)
        menu_button = Button(                                                       #Button to go to menu
            text='Menu',
            size_hint=(0.15, 0.15),
            pos_hint={'x': 0.0, 'y': 0.0},
            on_release=self.go_main,
        )
        float_lay.add_widget(menu_button)
                                                                                    #Label for title
        title = Label(text='Settings', bold=True, color=(.2, .5, .65, 1), font_size='30sp', pos_hint={'x': -0.415, 'y': 0.46})
        float_lay.add_widget(title)

        setting_info = Label(text="Click on info button to find out more, \nrate to write a review, \nor exit to close the program", bold=True, color=(.2,.5,.65,1),  font_size='15sp', pos_hint={'x':-0.3285,'y':0.37})               #label for information
        float_lay.add_widget(setting_info)

        self.arduino_info = Label(text="Connect Arduino", bold=True, color=(.2,.5,.65,1),  font_size='15sp', pos_hint={'x':0.3285,'y':-0.4})               #label for information
        float_lay.add_widget(self.arduino_info)                                                                 #TODO have label display if arduino is connected

    #Methods
    def rect_update(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_main(self, *args):
        App.get_running_app().root.current = 'main'

    def rate(self, *args):
        grid_lay = GridLayout(cols=1)
        self.rate_value = Label(
            text='0',
            size_hint=(0.1, 0.4),
        )
        grid_lay.add_widget(self.rate_value)

        self.rate_slider = Slider(
            min=0,
            max=5,
            value=0,
        )
        grid_lay.add_widget(self.rate_slider)
        self.rate_slider.bind(value=self.rate_value_display)

        self.user_review = TextInput(
            text='Tell us what you think!',
            size_hint=(0.8, 0.9),
            #pos_hint={'x': 0.1, 'y': 0.1},
        )
        grid_lay.add_widget(self.user_review)
        self.user_review.bind(focus=self.on_focus_delete)                           #Deletes text when input box is clicked

        self.submit_btn = Button(
            text='Submit',
            size_hint=(0.5, 0.5),
            on_release= self.rate_save
        )
        grid_lay.add_widget(self.submit_btn)

        self.rate_popup = Popup(title='Rate the Program!', content=(grid_lay), size_hint=(None, None), size=(400, 300))
        self.rate_popup.open()

    def rate_value_display(self, instance, value):                                   #Displays the slider's value
        self.rate_value.text = str(int(value))

    def rate_save(self, *args):                                                      #Saves the user's input
        date_time_name =  time.strftime("%d/%m/%Y-%H:%M:%S")                         #Gets the date and time
        print(date_time_name)

        review_file = open('AppReviews.txt', 'a')                                    #Appends the user's data onto a text file
        review = ('%s\nRating: %d \nReview: %s\n\n' % (date_time_name,self.rate_slider.value, self.user_review.text))
        print(review)
        review_file.write(review)
        review_file.close()

        self.rate_popup.dismiss()

    def on_focus_delete(self, instance, value):                                     #Method to clear the text box when pressed
        if value == True:
            self.user_review.text = ''
        else:
            pass

    def info_btn(self, *args):                                                      #Popup for information
        content_lbl = TextInput(readonly = True,
                                text="This is an application that controls a robot."
                                     "\nIn general, the program sends a signal serially from the inputs to the arduino where it's processed, then another signal is sent from the arduino to the servo motors; which, makes it move.\n\nCreated by Chirag")
        infoWindow = Popup(title='Information', content=content_lbl, size_hint=(None, None), size=(400, 350))
        infoWindow.open()

    def exit_app(self, instance):                                                   #Closes the program
        print('Closing the Application...')
        App.get_running_app().stop()


#Queue
class Queue:                                                                        #Queue class
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)                                                     #Adds item to queue

    def dequeue(self):
        if len(self.queue) >= 1:
            self.queue.pop()                                                        # pop(0) returns the value of the item that has been removed

        elif len(self.queue) <= 0:
            return None

    def clear(self):
        self.queue = []                                                             #Clears the queue

    def print(self):                                                                #prints items in queue
        print(self.queue)


#Arduino Robot control
def arduino():                                                                           #Checks if aruino is connected, looks at ports in windows and linux machines
    try:
        if sys.platform.startswith('win'):
            ports = list(serial.tools.list_ports.comports())
            Arduino_ports = []
            for p in ports:
                if 'Arduino' in p.description:
                    print (p)
                    Arduino_ports.append(p)
                    a_port = (Arduino_ports[0].device)
                    return a_port

        elif sys.platform.startswith('linux'):
            l_ports = "/dev/"+os.popen("dmesg | egrep ttyACM | cut -f3 -d: | tail -n1").read().strip()                        #.popen opens a open file object connected to the pipe
            return l_ports
        else:
            print('Port not found')
    except:
        print('Port not found')


# base_servo = 11                                                                      These are the pins that the servos are connected to
# shoulder_servo = 10                                                                  They connect with a baud rate of "115200"
# elbow_servo = 9
# grip_servo = 6

def update_grip(obj, value):
    update_grip_angle = int(obj.value)
    print("Grip:" + str(int(obj.value)))

def update_elbow(obj, value):
    update_elbow_angle = int(obj.value)
    print("Elbow:" + str(int(obj.value)))

def update_shoulder(obj, value):
    update_shldr_angle = int(obj.value)
    print("Shoulder:" + str(int(obj.value)))

def update_base(obj, value):
    update_base_angle = int(obj.value)
    print("Base:" + str(int(obj.value)))


#Screen Manager
w_manager = ScreenManager(transition= FadeTransition())                             #Creates a screen manager and has a fade transition
w_manager.add_widget(MainMenu())
w_manager.add_widget(SliderMode())
w_manager.add_widget(CodeMode())
w_manager.add_widget(CodeScreen())
w_manager.add_widget(SettingMode())


# The app class
class MyMain(App):
    def build(self):
        return w_manager


# Runs the App
if __name__ == '__main__':
    MyMain().run()
