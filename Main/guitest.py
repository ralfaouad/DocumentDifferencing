import PySimpleGUI as sg

layout = [[sg.Text("Document Differencing Tool")],
        [sg.Text('Document A', size=(15, 1)), sg.InputText(key="DOCA"), sg.FileBrowse()],
        [sg.Text('Document B', size=(15, 1)), sg.InputText(key="DOCB"), sg.FileBrowse()],
        [sg.Button("Start")],
        [sg.Text("", size=(0, 1), key='OUTPUT')],
        [sg.Text('Name of Patched File'),sg.InputText(key="PATCH")]
        ]

window = sg.Window('Document Differencing', layout, finalize=True)
while True:
        event, values = window.read()
        print(event,values)
        if event in (sg.WIN_CLOSED, 'Exit'):
             break
        if event == 'Start':
            print(event,values)
            treeA = values["DOCA"]
            treeB = values["DOCB"]
            #TED
            #Patched File
            #XML
            window["OUTPUT"].update(value="TED")
window.close()