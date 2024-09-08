from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.pickers import MDDatePicker
from kivy.lang.builder import Builder
import datetime
from database import MySQL
from morning import Morning
from night import Night
from graph import Graph

class LoginScreen(Screen):
    pass
class MenuScreenAdmin(Screen):
    pass
class MenuScreen(Screen):
    pass
class MorningScreen(Screen):
    pass
class EveningScreen(Screen):
    pass
class ToDoScreen(Screen):
    pass
class AddToDoScreen(Screen):
    pass
class SetGraphScreen(Screen):
    pass
class GraphScreen(Screen):
    pass
class AddUserScreen(Screen):
    pass

## WIDGETS ##
class MenuButton(MDRectangleFlatButton):
    text = "Menu"
    pos_hint = {"center_x":0.5, "center_y":0.2}

## ScreenManager
sm = ScreenManager()
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(MenuScreenAdmin(name="adminmenu"))
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(MorningScreen(name="morning"))
sm.add_widget(EveningScreen(name="evening"))
sm.add_widget(ToDoScreen(name="todo"))
sm.add_widget(AddToDoScreen(name="addtodo"))
sm.add_widget(SetGraphScreen(name="setgraph"))
sm.add_widget(GraphScreen(name="graph"))
sm.add_widget(AddUserScreen(name="adduser"))

## Set admins
ADMINS = [1]

class MyApp(MDApp):
    def build(self):
        self.id = None
        self.graph_dates = []
        screen = Builder.load_file('ui.kv')

        self.theme_cls.theme_style = "Dark"

        return screen
    
    ### LOG IN ###
    def login_button_pressed(self):
        self.username = self.root.get_screen("login").username.text
        db = MySQL()
        user_valid, self.id = db.check_user_login(self.username)
        if user_valid:
            if self.id in ADMINS:
                self.root.current = "adminmenu"
            else:
                self.root.current = "menu"
        else:
            self.login_error_dialog(self.username)

    def login_error_dialog(self, username):
        if username == "":
            string_error = "Please enter a username"
        else:
            string_error = self.username + " does not exist"
        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Login Failed", text=string_error,
                                buttons=[close_button])

        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


    ### WAKE UP ###
    def wakeup_button_pressed(self):
        morn = Morning(self.id)
        todays_wake_up_time = morn.todays_wakeup_time
        wakeup_time_label = self.root.get_screen("morning").ids.wake_up_time
        wakeup_time_label.text = todays_wake_up_time
        self.root.current = "morning"


    ### REGISTER DAY ###
    def submit_data_button_pressed(self):
        slider_data = self.root.get_screen("evening").slider_data
        switch_data = self.root.get_screen("evening").switch_data
        meditation = switch_data[0]
        ifast = switch_data[1]
        new_data = []

        # set first object in list to weight and adjust number
        new_data.append(round(50 + (slider_data[0] * 10),1))

        # go through the rest of the slider objects and add the values to list
        for i in range(1, len(slider_data)):
            new_data.append(int(slider_data[i]))

        # append all of the switches status to list
        for switch in switch_data:
            new_data.append(switch.active)

        Night(self.id, new_data)

        self.menu_button_pressed()

    ### TO-DO ###
    def todo_button_pressed(self):
        self.update_todo_list()

    def update_todo_list(self):
        todo_list_container = self.root.get_screen("todo").ids.container
        todo_list_container.clear_widgets()
        db = MySQL()
        todolist = db.get_todo_list(self.id)
        for task, detail in todolist.items():
            item = TwoLineListItem(text=task, secondary_text=detail,on_press=lambda x: self.list_item_pressed(x.text))
            todo_list_container.add_widget(item)
        self.root.current = "todo"

    def list_item_pressed(self, item_text):
        close_button = MDFlatButton(text="Cancel", on_release=self.close_dialog)
        remove_button = MDFlatButton(text="Remove", on_press=lambda x: self.remove_task(item_text))
        self.dialog = MDDialog(title="Remove task", text=f"Do you wish to remove \'{item_text}\'",
                            buttons=[remove_button, close_button])
        self.dialog.open()

    def remove_task(self, task_name):
        db = MySQL()
        if db.remove_task_from_db(self.id, task_name):
            self.dialog.dismiss()
            self.update_todo_list()
        else:
            print("something went terribly wrong!")

    def new_task_button_pressed(self):
        self.root.get_screen("addtodo").ids.task_input.text = ""
        self.root.get_screen("addtodo").ids.detail_input.text = ""
        self.root.current = "addtodo"

    def add_task_button_pressed(self):
        self.add_task()
        self.update_todo_list()

    def add_task(self):
        task = self.root.get_screen("addtodo").task.text
        detail = self.root.get_screen("addtodo").detail.text
        if task == "":
            close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Couldn't add task", text="Please enter a task title",
                                buttons=[close_button])
            self.dialog.open()
        else:
            db = MySQL()
            db.add_data("to_do_lists", {"user_id":self.id,"task":task,"detail":detail})


    #### GRAPH ###
    def graph_button_pressed(self):
        last_week = f"{datetime.date.today()- datetime.timedelta(days=6)} ~ {datetime.date.today()}"
        self.root.get_screen("setgraph").ids.date_label.text = last_week + " (7 days)"
        self.root.current = "setgraph"

    def get_date(self, instance, value, date_range):
        try:
            start_date = str(date_range[0]).replace("-", "/")
            end_date = str(date_range[-1]).replace("-", "/")
            label_text = f"{start_date} ~ {end_date} ({len(date_range)} days)"
            self.root.get_screen("setgraph").ids.date_label.text = label_text
        except:
            last_week = f"{datetime.date.today()- datetime.timedelta(days=6)} ~ {datetime.date.today()}"
            self.root.get_screen("setgraph").ids.date_label.text = last_week + " (7 days)"
            self.root.current = "setgraph"

        for date in date_range:
            self.graph_dates.append(str(date))

    def on_cancel(self, instance, value):
        pass

    def open_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.get_date, on_cancel=self.on_cancel)
        date_dialog.open()

    def get_graph_input_button_pressed(self):
        self.root.get_screen("graph").ids.bx1.clear_widgets()
        self.root.get_screen("graph").ids.bx2.clear_widgets()
        checkboxes = self.root.get_screen("setgraph").box_data
        target_values = []
        for box in checkboxes:
            target_values.append(box.active)
        target_keys = [
            "walking",
            "exercise",
            "skillup",
            "reading",
        ]
        graph_targets = dict(zip(target_keys,target_values))
        targets_only = [key for key,value in graph_targets.items() if value]
        print(graph_targets, "\n", targets_only)

        if not self.graph_dates:
            end_date_value = datetime.date.today()
            start_date = end_date_value - datetime.timedelta(days=6)

            current_date = start_date

            while current_date <= end_date_value:
                self.graph_dates.append(current_date.strftime("%Y-%m-%d"))
                current_date += datetime.timedelta(days=1)
        Graph(self, self.id, self.graph_dates, targets_only)
        self.root.current = "graph"

    ### ADD USER ###
    def add_user_button_pressed(self):
        new_user_username = self.root.get_screen("adduser").new_user_username.text
        #new_user_pw = self.root.get_screen("adduser").new_user_pw.text
        db = MySQL()

        is_available, message = db.check_if_available(new_user_username)
        if is_available == False:
            self.add_user_dialog("Something Went Wrong", message)
        else:
            db.add_user(new_user_username)
            self.add_user_dialog("User Successfully Added", message)
            self.menu_button_pressed()

    def add_user_dialog(self, title_msg, text_msg):
        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        self.dialog = MDDialog(title=title_msg, text=text_msg,
                            buttons=[close_button])
        self.dialog.open()

    ### MENU BUTTON ###
    def menu_button_pressed(self):
        if self.id in ADMINS:
            self.root.current = "adminmenu"
        else:
            self.root.current = "menu"

MyApp().run()
