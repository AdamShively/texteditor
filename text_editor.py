"""
This program is a text editor.
Author: Adam Shively
Version: 1.3
Since: 01-19-2022
"""
import PySimpleGUI as sg
import pathlib
import tkinter.font as TkFont
import clipboard

class TextEditor:

    #Initialization function
    def __init__(self, curr_font, curr_font_size, bold, italic, under, strike, wrapped):
        self.file = None
        self.curr_font = curr_font
        self.curr_font_size = curr_font_size
        self.bold = bold
        self.italic = italic
        self.under = under
        self.strike = strike
        self.wrapped = wrapped
        self.window = TextEditor.create_window()
        
    def create_window(theme=None):
        if theme:
            sg.theme(theme)

        edit_layout = ['Delete', 'Copy', 'Paste', 'Select All']

        setup = [['File', ['New', 'Open', 'Save', 'Save As', 'Exit']],
            ['Edit', [edit_layout]],
            ['Format', ['Font', 'Word Wrap']],
            ['View',['Theme','Count']],
            ['Help', ['Ask For Help']]]

        layout = [[sg.Menu(setup)],      
                [sg.Multiline(size=(90, 25), key='-BODY-', right_click_menu= ['', edit_layout])]] 

        return sg.Window('Text Editor', layout=layout, resizable=True, margins=(0,0), return_keyboard_events=True, finalize=True)

    def new(self, values):

        if self.file:    #Make sure file exists.
            file_path = pathlib.Path(self.file)
            file_text = file_path.read_text()

            if values['-BODY-'] == file_text:   #If no changes made to text, no need to save.
                self.window['-BODY-'].update(value='')
                return None

        layout2 = [[[sg.Text('Save File?')],sg.Button('Save'), sg.Button('Do Not Save'), sg.Button('Cancel')]]
        wind  = sg.Window('', layout2, grab_anywhere=False, size=(220, 90), return_keyboard_events=True, keep_on_top=True, finalize=True)

        while True:
            event, _ = wind.read()
            if event in(sg.WIN_CLOSED, 'Cancel'):
                wind.close()
                break

            if event in ('Save',):
                wind.close()
                self.save_file(values)
                self.window['-BODY-'].update(value='')
                self.file=None
                break

            if event in ('Do Not Save',):
                wind.close()
                self.window['-BODY-'].update(value='')
                self.file=None
                break

    #Open a file.
    def open(self):
        file_name = sg.popup_get_file('Open', no_window=True)
        if file_name:
            file = pathlib.Path((file_name))
            self.window['-BODY-'].update(value=file.read_text())
            self.file = file

    #Save file.
    def save_file(self, values):
        if self.file:
            self.file.write_text(values['-BODY-'])
        else:
            self.save_file_as(values)

    #Save a new file.
    def save_file_as(self, values):
        file_name = sg.popup_get_file('Save As', save_as=True, no_window=True)
        if file_name:
            self.file = pathlib.Path(file_name)
            self.file.write_text(values['-BODY-'])

    #Copy current text.
    def copy(self):
        try:
            text = self.window['-BODY-'].Widget.selection_get()
            clipboard.copy(text)  #Add selected to clipboard
                
        except:
            sg.popup_error('ERROR', 'Select portion of text to be copied.', keep_on_top=True)

    #Paste current text.
    def paste(self):

        try:                        #Deletes selected before pasting
            self.window['-BODY-'].Widget.delete("sel.first", "sel.last")
            text = clipboard.paste()    
            self.window['-BODY-'].Widget.insert("insert", text) #Paste text
            
        except:                     
            text = clipboard.paste()    
            self.window['-BODY-'].Widget.insert("insert", text) #Paste text

    #Delete slected text.
    def delete(self):
        try:
            self.window['-BODY-'].Widget.delete("sel.first", "sel.last")  #Delete selected
                
        except:               
            sg.popup_error('ERROR', 'Select portion of text to be deleted.', keep_on_top=True)

    #Select all text in body.
    def select_all(self):
        self.window['-BODY-'].Widget.tag_add("sel","1.0","end")

        #Set the wrapping of current text.
    def wrap(self):
        if self.wrapped:
            self.window['-BODY-'].Widget.configure(wrap='none')
        else:
            self.window['-BODY-'].Widget.configure(wrap='word')

        self.wrapped = not self.wrapped

    #Set the font of current text.
    def font(self):

        font_list = TextEditor.font_list()
        
        style_layout = [[sg.Text('Font Style:'),sg.Text(self.curr_font,font=[self.curr_font], key='-STYLE_SELECT-')],
                [sg.Listbox(values=font_list, default_values=[self.curr_font,], size=(32, 16), key='-STYLE_LIST-', enable_events=True)]]

        font_size_arr = [6,8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
        size_layout = [[sg.Text('Font Size:'),sg.Text(self.curr_font_size, key='-SIZE_SELECT-')],
                [sg.Listbox(values=font_size_arr,default_values=[self.curr_font_size,], size=(10, 16), key='-SIZE_LIST-', enable_events=True)]]

        radio_layout = [
                [sg.Checkbox('Bold', key ='-BOL-', default=(self.bold=='bold'), font=TkFont.Font(weight="bold"))],
                [sg.Checkbox('Italic', key ='-ITA-', default=(self.italic=='italic'), font=TkFont.Font(slant ="italic"))],
                [sg.Checkbox('Underline', key ='-UND-', default=(self.under==1), font=TkFont.Font(underline ="1"))],
                [sg.Checkbox('Strikethough', key ='-STK-', default=(self.strike==1), font=TkFont.Font(overstrike ="1"))]]

        font_buttons = [[sg.Button('OK'),sg.Button('Exit')]]

        #Create a window for font options.
        font_window = sg.Window('', [[sg.Column(style_layout),sg.Column(size_layout),sg.Column(radio_layout)],font_buttons],keep_on_top=True, finalize=True)

        #Event loop for font options. 
        while True:  
            font_event, font_values = font_window.read()

            if font_event in (sg.WIN_CLOSED, 'Exit'):
                break

            font_style = font_values['-STYLE_LIST-']
            font_window['-STYLE_SELECT-'].update(font_style[0], font=font_style)

            font_size = font_values['-SIZE_LIST-'][0]
            font_window['-SIZE_SELECT-'].update(font_size)
                
            if font_event in ('OK',):

                if font_values['-BOL-'] == True:
                    self.bold = 'bold'
                else:
                    self.bold = 'normal'
                if font_values['-ITA-'] == True:
                    self.italic = 'italic'
                else:
                    self.italic = 'roman'
                if font_values['-UND-'] == True:
                    self.under = 1
                else:
                    self.under = 0
                if font_values['-STK-'] == True:
                    self.strike = 1
                else:
                    self.strike = 0

                self.curr_font = font_style[0]
                self.curr_font_size = font_size

                f = TkFont.Font(family=font_style[0],size=font_size,weight=self.bold,slant=self.italic,underline=self.under,overstrike=self.strike)
                self.window['-BODY-'].update(font=f)

                break
            
        font_window.close()

    #Create a list of fonts to choose from.
    def font_list():
        font_tuple = TkFont.families()
        fonts = []

        for font in font_tuple:
            if font[0] != '@':  #Filter out unwanted available fonts.
                fonts.append(font)
        return fonts

    #Count words and characters.
    def count(values):
        body = values['-BODY-']

        words = body.split()
        number_of_words = len(words)

        number_of_characters = 0
        for c in words:
            number_of_characters += len(c)

        result = f'Words: {number_of_words} Characters: {number_of_characters}'
        sg.Popup('Text Counts.', result, keep_on_top=True)

    #Change theme of window.
    def change_theme(self, values):
        temp_text = values['-BODY-']
        e, v = sg.Window('Choose Theme',
                        [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME_LIST-'), sg.OK(), sg.Cancel()]]
                        ,keep_on_top=True).read(close=True)

        theme = v['-THEME_LIST-']

        if e == 'OK':
            self.window.close()
            self.window = TextEditor.create_window(theme)
            self.window.maximize()
            self.window['-BODY-'].expand(expand_x=True, expand_y=True)
            self.window['-BODY-'].update(temp_text)

            f = TkFont.Font(family=self.curr_font,size=self.curr_font_size,weight=self.bold,slant=self.italic,underline=self.under,overstrike=self.strike)
            self.window['-BODY-'].update(font=f)

    def ask_help():
        msg = ''' 
        Do you have questions or concerns?
        Feel free to send an email to 
        ______________@gmail.com.
        Check out my github at 
        https://github.com/AdamShively
        '''
        sg.Popup('', msg, keep_on_top=True)

    #Main window
    def main(self):
        self.window.maximize()
        self.window['-BODY-'].expand(expand_x=True, expand_y=True)

        while True:
            
            event, values = self.window.read()
            if event in(sg.WIN_CLOSED, 'Exit'):
                break

            if event in('New',):
                self.new(values)

            if event in('Open',):
                self.file = self.open()

            if event in ('Save',):
                self.save_file(values)

            if event in ('Save As',):
                self.save_file_as(values) 

            if event in ('Copy',):
                self.copy()

            if event in ('Paste',):
                self.paste()

            if event in ('Delete',):  
                self.delete()

            if event in ('Select All',):
                self.select_all()    

            if event in ('Word Wrap',):
                self.wrap()

            if event in ('Font',):
                self.font()

            if event in ('Theme',):
                self.change_theme(values)

            if event in ('Count',):
                TextEditor.count(values)

            if event in ('Ask For Help',):
                TextEditor.ask_help()

        self.window.close()

if __name__ == "__main__":
    te = TextEditor('System', 6, 'normal', 'roman', 0, 0, True)
    te.main()
