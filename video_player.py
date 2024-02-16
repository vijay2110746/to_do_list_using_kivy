from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.textfield import MDTextField

KV = '''
Screen:
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
                size_hint_x: None
                width: root.width - dp(150)
                
            MDIconButton:
                icon: 'plus'
                on_release: app.add_task(task_input.text)
            
        ScrollView:
            MDList:
                id: task_list
'''


class TaskListItem(TwoLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description_input = MDTextField(hint_text="Enter task description", multiline=True)
        self.secondary_text = ''

    def add_description_input(self):
        if not self.secondary_text:
            self.add_widget(self.description_input)
            self.secondary_text = self.description_input


class ToDoListApp(MDApp):
    task_count = 0

    def add_task(self, task_name):
        if task_name.strip():
            self.task_count += 1
            task_item = TaskListItem(text=task_name)
            task_item.add_description_input()  # Add description input when adding task
            self.root.ids.task_list.add_widget(task_item)

    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    ToDoListApp().run()
