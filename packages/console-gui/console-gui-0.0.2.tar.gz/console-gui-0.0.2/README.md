# console-gui

1 - install:
    pip install console-gui

2 - use
    from gui import *

    # when we change the text
    # component = what is the component calling the func
    def on_text_change(component):
        reader.components['readonly'].config(text=component.text)


    componets=[
        Field('readonly', None, readonly=True, text='hello readonly'), # readonly lets the user not click on it
        Field('this is a input filid', on_text_change),
        Button('this is a disable button', None, enable=False), # gray out the button not letting the user click it
        Button('this is a exit button', lambda _: exit(0)) # exit the prorgam when click
    ]

    reader = Reader(componets)

    reader.read()

3 - add more
    from gui.components import Component

    class MyComponent(Component):
        def __init__(self, name, click, **kwargs):
            super().__init__(name, click, **kwargs)
            self.text = name
        
        # calls when we click
        def on_click(self):
            self.text = 'pizza'
            self.click(self)
        
        # what will is show
        def __str__(self):
            return self.text
