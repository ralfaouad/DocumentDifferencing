import PySimpleGUI as sg
import subprocess
import sys


def FText(text, in_key=None, default=None, tooltip=None, input_size=None, text_size=None):
    """
    A "Fixed-sized Text Input".  Returns a row with a Text and an Input element.
    """
    if input_size is None:
        input_size = (20, 1)
    if text_size is None:
        text_size = (20, 1)
    return [sg.Text(text, size=text_size, justification='r', tooltip=tooltip),
            sg.Input(default_text=default, key=in_key, size=input_size, tooltip=tooltip)]


def main():

    # This version of the GUI uses this large dictionary to drive 100% of the creation of the
    #   layout that collections the parameters for the command line call.  It's really simplistic
    #   at the moment with a tuple containing information about each entry.
    # The definition of the GUI.  Defines:
    #   PSG Input Key
    #   Tuple of items needed to build a line in the layout
    #       0 - The command line's parameter
    #       1 - The text to display next to input
    #       2 - The default value for the input
    #       3 - Size of input field (None for default)
    #       4 - Tooltip string
    #       5 - List of additional elements to include on the same row

    # input_defintion = {
    #     '-FILEA-' : ('--input_file', 'Document A', '', (40,1),'The XML file to transform to the first ROLT', [sg.FileBrowse()]),
    #     '-FILEB-' : ('--input_file', 'Document B', '', (40,1),'The XML file to transform to the second ROLT', [sg.FileBrowse()]),
    #     # '-OUT FILE-' : ('--output_file', 'Output File', '', (40,1), "the output file. (optional. if not included, it'll just modify the input file name)", [sg.FileSaveAs()]),
    #     # '-SIM-' : ('--silent_threshold', 'Silent Threshold', 0.03, None, "the volume amount that frames' audio needs to surpass to be consider \"sounded\". It ranges from 0 (silence) to 1 (max volume)", []),
    #     # '-SOUNDED SPEED-' : ('--sounded_speed', 'Sounded Speed', 1.00, None, "the speed that sounded (spoken) frames should be played at. Typically 1.", []),
    #     # '-SILENT SPEED-' : ('--silent_speed', 'Silent Speed', 5.00, None, "the speed that silent frames should be played at. 999999 for jumpcutting.", []),
    #     # '-FRAME MARGIN-' : ('--frame_margin', 'Frame Margin', 1, None, "some silent frames adjacent to sounded frames are included to provide context. How many frames on either the side of speech should be included? That's this variable.", []),
    #     # '-SAMPLE RATE-' : ('--sample_rate', 'Sample Rate', 44100, None, "sample rate of the input and output videos", []),
    #     # '-FRAME RATE-' : ('--frame_rate', 'Frame Rate', 30, None, "frame rate of the input and output videos. optional... I try to find it out myself, but it doesn't always work.", []),
    #     # '-FRAME QUALITY-' : ('--frame_quality', 'Frame Quality', 3, None, "quality of frames to be extracted from input video. 1 is highest, 31 is lowest, 3 is the default.", [])
    #                 }

    # the command that will be invoked with the parameters
    command_to_run = r'python .\Main\main.py '

    # Find longest input descrption
    # text_len = max([len(input_defintion[key][1]) for key in input_defintion])
    # Top part of layout that's not table driven
    layout = [[sg.Text('Document Differencing', font='Any 20')],
            [sg.Text('Document A', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
            [sg.Text('Document B', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
            [sg.Submit("Calculate Similarity"), sg.Cancel()]]
    
    
    # Computed part of layout that's based on the dictionary of attributes (the table driven part)
    # for key in input_defintion:
    #     layout_def = input_defintion[key]
    #     line = FText(layout_def[1], in_key=key, default=layout_def[2], tooltip=layout_def[4], input_size=layout_def[3], text_size=(text_len,1))
    #     if layout_def[5] != []:
    #         line += layout_def[5]
    #     layout += [line]

    # Bottom part of layout that's not table driven
    # layout += [[sg.Text('Distance and Similarity Measures:')],
    #     [sg.Text(size=(80,3), key='-COMMAND LINE-', text_color='yellow', font='Courier 8')],
    #     [sg.MLine(size=(80,10), reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, write_only=True, font='Courier 8', autoscroll=True, key='-ML-')],
    #     [sg.Button('Start'), sg.Button('Exit')]]

    window = sg.Window('Document Differencing', layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Calculate Similarity':
            main(A,B)
    window.close()


def runCommand(cmd, timeout=None, window=None):
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.refresh() if window else None  # yes, a 1-line if, so shoot me

    retval = p.wait(timeout)
    return (retval, output)

if __name__ == '__main__':
    # sg.theme('Dark Grey 11')
    main()