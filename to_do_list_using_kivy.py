from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivy.metrics import dp

KV = '''
Manager:
    SignUp:
    Login:
    ToDoList:
<SignUp>:
    name:"first"
    MDCard:
        size_hint: None,None
        size: 350,400
        pos_hint: {"center_x":0.5,"center_y":0.5}
        elevation: 10
        padding:25
        spacing:25
        orientation: 'vertical'
    
        MDLabel:
            id: Sign_In
            text: "Sign In"
            font_size:40
            halign:'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding:15
        
        MDTextField:
            id:user
            hint_text:'username'
            icon_right:'account'
            width: 200
            height:100
            font_size: 18
            pos_hint:{'center_x':0.5}
        MDTextField:
            id:pass_input
            hint_text:'password'
            icon_right:'eye-off'
            password:True
            width: 200
            height:100
            font_size: 18
            pos_hint:{'center_x':0.5}
        
        
        MDRaisedButton:
            text:"Log In"
            font_size: 18
            pos_hint:{'center_x':0.5}
            on_release: app.login(user.text,pass_input.text)
<Login>:
    name:'second'
    MDCard:
        size_hint: None,None
        size: 350,500
        pos_hint: {"center_x":0.5,"center_y":0.5}
        elevation: 10
        padding:25
        spacing:25
        orientation: 'vertical'
    
        MDLabel:
            id: Sign_Up
            text: "Sign Up"
            font_size:40
            halign:'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding:15
        
        MDTextField:
            id:user
            hint_text:'username'
            icon_right:'account'
            width: 200
            height:100
            font_size: 18
            pos_hint:{'center_x':0.5}

        MDTextField:
            id:mail_input
            hint_text:'email'
            icon_right:'email'
            width: 200
            height:100
            font_size: 18
            pos_hint:{'center_x':0.5}
            
        MDTextField:
            id:pass_input1
            hint_text:'password'
            icon_right:'eye-off'
            password:True
            width: 200
            height:100
            font_size: 18
            pos_hint:{'center_x':0.5}
        
        
        MDRaisedButton:
            text:"Sign Up"
            font_size: 18
            pos_hint:{'center_x':0.5}
            on_press: app.signup(user.text,mail_input.text,pass_input.text)
<ToDoList>:
    name:'third'
    MDBoxLayout:
        orientation: 'vertical'
        
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(8)
            spacing: dp(8)
            
            MDIconButton:
                icon: 'menu'
            
            MDLabel:
                text: 'To-Do List'
                halign: 'center'
                font_style: 'H6'
        
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(8)
            spacing: dp(8)
            
            MDTextField:
                id: task_input
                hint_text: "Enter task name"
                width: root.width - dp(150)
                hint_text_color: app.theme_cls.disabled_hint_text_color
                line_color_normal: app.theme_cls.primary_color
                mode: "rectangle"
                color_mode: "primary"
                on_text_validate: app.add_task(self.text)
                
            MDIconButton:
                icon: 'plus'
                on_release: app.add_task(task_input.text)
            
        ScrollView:
            MDList:
                id: task_list
                spacing: dp(16)
'''

class SignUp(Screen):
    pass

class Login(Screen):
    pass

class ToDoList(Screen):
    pass

class Manager(ScreenManager):
    pass

class LoginApp(MDApp):
    task_count=0
    def build(self):
        return Builder.load_string(KV)

    def add_task(self, task_name):
        if task_name.strip():
            task_card = TaskCard(task_name=task_name)
            self.root.get_screen('third').ids.task_list.add_widget(task_card)
            self.root.get_screen('third').ids.task_input.text = ''

    def signup(self, username, email, password):
        print(f'Username: {username}, Email: {email}, Password: {password} registered successfully.')

    def login(self, username, password):
        if username == 'admin' and password == 'password':
            self.root.current='third'
        else:
            print('Login failed')

class TaskCard(MDCard):
    def __init__(self, task_name, **kwargs):
        super().__init__(**kwargs)
        self.task_name = task_name
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(72)
        self.spacing = dp(8)
        self.elevation=dp(6)
        
        checkbox = MDCheckbox()
        task_label = MDLabel(text=task_name)
        delete_button = MDIconButton(icon='delete')
        delete_button.bind(on_release=self.delete_task)
        
        self.add_widget(checkbox)
        self.add_widget(task_label)
        self.add_widget(delete_button)
    
    def delete_task(self, instance):
        app = MDApp.get_running_app()
        app.root.get_screen('third').ids.task_list.remove_widget(self)

if __name__ == '__main__':
    LoginApp().run()
