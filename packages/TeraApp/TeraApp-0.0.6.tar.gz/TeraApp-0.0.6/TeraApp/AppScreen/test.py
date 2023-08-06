from TeraApp1.TeraApp.AppScreen.AppScreen import *
app = TeraApp('TeraApp', 500, 500, 'blue') #500 = x,500(2) = y
app.txt('Title', 240,2, 15) #(x = 240), (y = 2), (15 = txt size)
input1 = app.input(210, 30, 'white')

def fds():
    print(app.input_name.text())


app.buttonf('save', 210,100, 'green', fds)
app.app.exec()

