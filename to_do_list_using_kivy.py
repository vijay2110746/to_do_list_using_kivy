from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivy.metrics import dp
# from kivymd.uix.button import MB
import mysql.connector


global_username=None
global_password=None
datatask=None
conn=mysql.connector.connect(host='localhost',user='root',password='vijay',database='login')
try:
    if conn.is_connected():
        print("yes")
except:
    print("Errored")

cur=conn.cursor()

KV = '''
Manager:
    SignUp:
    Login:
    ToDoList:
<SignUp>:
    name:"first"
    MDCard:
        size_hint: None,None
        size: 450,500
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

        MDFlatButton:
            text:'new user? SignUP'
            font_size:14
            pos_hint:{'center_x':0.5}
            on_release: app.switch()

<Login>:
    name:'second'
    MDCard:
        size_hint: None,None
        size: 450,600
        pos_hint: {"center_x":0.5,"center_y":0.5}
        elevation: 10
        padding:25
        spacing:15
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

        MDTextField:
            id:pass_input2
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
            on_press: app.signup(user.text,mail_input.text,pass_input1.text,pass_input2.text)
        
        MDFlatButton:
            text:'already registered? SignIn'
            font_size:14
            pos_hint:{'center_x':0.5}
            on_release: app.switch1()
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
            
            MDRaisedButton:
                text: 'Save'
                on_release: app.savedata()
        
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
            print(task_name)
            task_card = TaskCard(task_name=task_name)
            self.root.get_screen('third').ids.task_list.add_widget(task_card)
            self.root.get_screen('third').ids.task_input.text = ''

    def switch(self):
        self.root.current='second'

    def switch1(self):
        self.root.current='first'
        
    def signup(self, username, email, password,confirm):
        global global_username,global_password
        if password==confirm:
            print(f'Username: {username}, Email: {email}, Password: {password} registered successfully.')
            q = "INSERT INTO users (user, email, password) VALUES (%s, %s, %s)"
            v=(username,email,password)
            cur.execute(q,v)
            conn.commit()
            global_username=username
            global_password=password
            print('executed')
            self.root.current='third'


    def login(self, username, password):
        global global_username,global_password
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        res = cur.fetchall()
        print(res)
        username1=[]
        password1=[]
        for i in res:
            username1.append(i[1])
            password1.append(i[3])
        if username in username1:
            ind=username1.index(username)
            if password1[ind]==password:
                print("verified")
                global_username=username
                global_password=password
                self.root.current='third'
                q='select tasks from users where user = %s and password = %s'
                v=(username,password)
                cur.execute(q,v)
                res=cur.fetchone()
                # print(res[0])
                r=res[0].split('::::::')
                for i in r:
                    self.add_task(i)


            else:
                print("Login credentials dont match!!!")
        else:
            print("Username not in database!!!")
    
    def savedata(self):
        tasks=[]
        task_list=self.root.get_screen('third').ids.task_list
        for widget in task_list.children:
            if isinstance(widget,TaskCard):
                tasks.append(widget.task_name)

        print(tasks)
        
        r=''
        ts=len(tasks)
        for task in reversed(range(ts)):
            if tasks[task]==tasks[0]:
                r+=tasks[task]
            else:
                r+=tasks[task]+'::::::'
        
        if global_username and global_password:
            q="update users set tasks = %s where password=%s and user = %s"
            v=(r,global_password,global_username)
            cur.execute(q,v)
            conn.commit()

        print('tasks ',tasks)

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
        # print(app.root.get_screen('third').ids.task_list)
        
    

if __name__ == '__main__':
    LoginApp().run()
