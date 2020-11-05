# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:21:29 2020

@author: xor
"""


import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from pynput import keyboard
import threading
import time
import pyautogui
import os
import ast
import sys


class MainWindow:
    """
    The main program class whose task is to display the main program window
    for the end user. From this window, user can navigate to the right part of
    the program or simply open "about program" infobox.

    Attributes
    ----------
    root : tkinter.Tk object
        root widget from tkinter package, which is necessary for the program to
        start

    logo_label : tkinter.Label object
         label containing the name/logo of the program, displayed in the main
         window

    start_button : tkinter.Button object
        a button that takes the user to the right part of the program

    about_button : tkinter.Button object
        a button that display (as an infobox) general information

    exit_button : tkinter.Button object
        a button that quit program

    Methods
    ----------
    menu()
        create all tkinter objects in the main program window
        set default properties for that window (like geometry)
        and pack all created widget

    start_click()
        the method that handles the 'start_button' click event

    about_click()
        the method that handles the 'about_button' click event
    """

    def __init__(self, master):
        """
        Constructor

        Parameters
        ----------
        master : tkinter.Tk object
            root widget from tkinter package
        """

        self.root = master
        self.menu()


    def menu(self):
        """
        sets title of the main window to 'PyTin2 - Clicker',
        geometry to '260x100' and disable resizable property,
        creates tkinter widgets and pack them into single column

        """

        # main frame properties
        self.root.title('PyTin2 - Clicker')
        self.root.resizable(False, False)
        self.root.geometry('260x100')

        ### main frame widgets
        self.logo_label = tk.Label(self.root, text = 'Welcome to PyTin 2!')
        self.start_button = tk.Button(self.root, text = 'start',
                                 width = 30, command = self.start_click)
        self.about_button = tk.Button(self.root, text = 'about',
                                 width = 30, command = self.about_click)
        self.exit_button = tk.Button(self.root, text = 'exit',
                                width = 30, command = self.root.quit)

        ### packing widgets on the main window
        self.logo_label.pack()
        self.start_button.pack()
        self.about_button.pack()
        self.exit_button.pack()

    def start_click(self):
        """
        withdraw main window widget, and create a new instance of object called
        SecondaryWindow (class created to manage window with all program functionality)

        """

        self.root.withdraw()
        new_window = SecondaryWindow(self.root)

    def about_click(self):
        """
        shows information about author and program in simple system info messagebox

        """

        messagebox.showinfo('About',
                            'Simple clicker to automate process in metin2, created by xor')

class SecondaryWindow:
    """
    This class is responsible for handling all program functionality. Creating
    an instance of this class display new window widget which contains list
    object that lists all the commands the clicker should execute and few buttons
    that are used for managing other functionalities.

    Creating an instance of this class starts 2 threads: one listening for
    global hotkeys, and one which manage the main loop of the program.

    Parameters
    ----------
    root : tkinter.Tk object
        root widget from tkinter package, which is necessary for the program to
        start

    secondary_window : tkinter.Toplevel objects
        new window that is shown after creation of the instance of class

    list_of_orders : list object
        At first it is completly empty, but it was created to hold all the commands
        to be executed by the program while running

    clicker_running : boolean variable
        default set to False, main use is to check if clicker is running

    program_running : boolean variable
        default set to True, used to start program after creating class instance

    click_delay : float variable
        default set to 0.001, define how long the clicker should wait between
        each press of the mouse

    sequence_delay : float variable
        default set to 0.01, define how long the program should wait between
        repeating the whole sequence of added command

    listener : pynput thread object
        is responsible for listening for global hotkeys

    program_thread : threading.Thread objects
        is responsible for running the program in the background
    """

    def __init__(self, master):
        """
        Constructor

        Parameters
        ----------
        master : tkinter.Tk object
            root widget from tkinter package
        """
        ### secondary frame

        self.root = master
        self.secondary_window = tk.Toplevel()

        self.list_of_orders = []
        self.clicker_running = False
        self.program_running = True
        self.click_delay = 0.001
        self.sequence_delay = 0.01

        self.menu()

        # this listener is responsible for listening for global hotkeys pressed
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+z' : self.on_activate_z,
            '<ctrl>+<shift>+x' : self.on_activate_x,
            '<ctrl>+<shift>+c' : self.on_activate_c,
            '<ctrl>+<shift>+v' : self.run_command})
        self.program_thread = threading.Thread(target = self.clicker_run)

        self.program_thread.start()
        self.listener.start()

    def menu(self):
        """
        sets title of the window to 'PyTin2 - Clicker',
        disable resizable property,
        creates tkinter widget objects and pack them into new window widget

        it creates:
        1 tkinter.Listbox
        6 tkinter.Button (RUN, SAVE, LOAD, CLEAR, HOW TO, CLOSE)
        1 tkinter.Label (as statusbar)

        """

        self.secondary_window.title('PyTin2 - Clicker')
        self.secondary_window.resizable(False, False)
        self.order_listbox = tk.Listbox(self.secondary_window, width = 50, selectmode = tk.BROWSE)
        self.run_button = tk.Button(self.secondary_window, text = 'RUN', width = 10,
                                    height = 1, command = self.run_command)
        self.save_button = tk.Button(self.secondary_window, text = 'SAVE', width = 10,
                                     height = 1, command = self.save_command)
        self.load_button = tk.Button(self.secondary_window, text = 'LOAD', width = 10,
                                     height = 1, command = self.load_command)
        self.clear_button = tk.Button(self.secondary_window, text = 'CLEAR', width = 10,
                                      height = 1, command = self.clear_command)
        self.add_button = tk.Button(self.secondary_window, text = 'HOW TO', width = 10,
                                       height = 1, command = self.info_command)
        self.close_button = tk.Button(self.secondary_window, text = 'CLOSE', width = 10,
                                      height = 1, command = self.close_windows)
        self.statusbar = tk.Label(self.secondary_window, text = "Not activated...",
                                        bd = 1, relief = tk.SUNKEN, anchor = tk.W)

        self.order_listbox.bind('<Double-Button>', self.listbox_selection)

        self.order_listbox.grid(row = 0, rowspan = 6, column = 0, padx = 6, pady = 2)
        self.run_button.grid(row = 0, column = 1, pady = 1, padx = 1)
        self.save_button.grid(row = 1, column = 1, pady = 1, padx = 1)
        self.load_button.grid(row = 2, column = 1, pady = 1, padx = 1)
        self.clear_button.grid(row = 3, column = 1, pady = 1, padx = 1)
        self.add_button.grid(row = 4, column = 1, pady = 1, padx = 1)
        self.close_button.grid(row = 5, column = 1, pady = 1, padx = 1)
        self.statusbar.grid(row = 6, column = 0, columnspan = 2, sticky = 'WE')

    def order_list_update(self):
        """
        this method is responsible for updating listbox widget based on the
        list_of_orders list
        """

        self.order_listbox.delete(0, 'end')
        for i in self.list_of_orders:
            self.order_listbox.insert('end', i)

    def listbox_selection(self, evt):
        """
        this method is responsible for creating new instance of DialogWindow
        class (special class to manage dialog boxes). It works everytime when
        user select and then doubleclick on listbox item
        """

        idx = self.order_listbox.curselection()[0]
        command = list(self.list_of_orders[idx].keys())[0]
        value = self.list_of_orders[idx].get(command)
        dialog = DialogWindow(master = self.root,
                                parent = self,
                                command = command,
                                value = value,
                                index = idx)

    def run_command(self):
        """
        the method assigned to the 'run_button', it starts the clikcer and changes
        accordingly statusbar
        it can be also run by clicking 'ctrl + shift + v' hotkey on keyboard
        by user
        """

        if self.clicker_running:
            self.clicker_running = False
            self.statusbar.config(text = 'Not activated...')
        else:
            self.clicker_running = True
            self.statusbar.config(text = 'Activated...')

    def save_command(self):
        """
        this method is responsible for opening save dialog, and create special
        save file (extension: .ptsave) which contains whole sequence of commands
        added to list_of_orders list
        """

        filename = fd.asksaveasfilename(filetypes = [("Pytin2 SaveFile", "*.ptsave")],
                                            defaultextension = '.ptsave')
        if filename:
            with open(filename, 'w') as file:
                for each in self.list_of_orders:
                    file.write("%s\n" % each)

    def load_command(self):
        """
        this method is responsible for opening load dialog, and add to list_of_orders
        list all commands written in special save file (extension: .ptsave)
        which contains sequence of commands for clicker
        """

        filename = fd.askopenfilename(filetypes = [("Pytin2 SaveFile", "*.ptsave")])
        if os.path.isfile(filename):
            temp_order_list = []
            with open(filename, 'r') as file:
                line = file.readline()
                while line:
                    text = line.replace('\n', '')
                    dict_obj = ast.literal_eval(text)
                    temp_order_list.append(dict_obj)
                    line = file.readline()
            self.list_of_orders = temp_order_list.copy()
            self.order_list_update()

    def clear_command(self):
        """
        clears whole list_of_orders list and order_listbox widget
        """

        self.list_of_orders.clear()
        self.order_listbox.delete(0,'end')

    def info_command(self):
        """
        displays a infobox with basic program functionality description
        """

        messagebox.showinfo('How to use',
        '''Hotkeys:
            <ctrl>+<shift>+z - left mouse click
            <ctrl>+<shift>+x - right mouse click
            <ctrl>+<shift>+c - move cursor to position
            <ctrl>+<shift>+v - start/stop clicker
        You can also start/stop clicker with RUN button.
        Double left click on list object to modify its properties
        Save button - create .ptsave file to save your sequence
        Load button - load .ptsave file with previous sequence''')

    def close_windows(self):
        """
        stops all threads and program, destroy SecondaryWindow instance, and
        restores main app window
        """

        self.listener.stop()
        self.program_running = False
        self.clicker_running = False
        self.secondary_window.destroy()
        self.root.deiconify()

    def on_activate_z(self):
        """
        adds left click command to list_of_orders list and update order_listbox
        widget with it, after clicking 'ctrl + shift + z' hotkey on keyboard
        by user
        """

        self.list_of_orders.append({'lclick' : 1})
        self.order_list_update()

    def on_activate_x(self):
        """
        adds right click command to list_of_orders list and update order_listbox
        widget with it, after clicking 'ctrl + shift + x' hotkey on keyboard
        by user
        """

        self.list_of_orders.append({'rclick' : 1})
        self.order_list_update()

    def on_activate_c(self):
        """
        adds moveTo command to list_of_orders list and update order_listbox
        widget with it, after clicking 'ctrl + shift + c' hotkey on keyboard
        by user
        """

        x, y = pyautogui.position()
        self.list_of_orders.append({'moveTo' : (x, y)})
        self.order_list_update()

    def clicker_run(self):
        """
        main loop of clicker, which is responsible for reacting to a particular
        command from the list_of_orders and repeating the entire
        sequence of commands

        contains two loops which are manage by changing program_running and
        clicker_running values
        """

        while self.program_running:
            while self.clicker_running:
                for value in self.list_of_orders:
                    command = list(value.keys())[0]
                    if command == 'moveTo':
                        x, y = value.get(command)
                        pyautogui.moveTo(x, y)
                    elif command == 'lclick':
                        pyautogui.click(button = 'left',
                                        clicks = value.get(command),
                                        interval = self.click_delay)
                    elif command == 'rclick':
                        pyautogui.click(button = 'right',
                                        clicks = value.get(command),
                                        interval = self.click_delay)
                time.sleep(self.sequence_delay)

class DialogWindow:
    """
    This class is responsible for handling the functionality of the listbox
    created in the SecondaryWindow instance and for displaying appropriate
    dialob boxes, depending on the selected objects inside the listbox widget

    Parameters
    ----------

    root : tkinter.Tk object
        root widget from tkinter package, which is necessary for the program to
        start

    parent : SecondaryWindow instance
        instance of SecondaryWindow class, it's necessary to properly edit
        values in working program

    dialog_window : tkinter.TopLevel object
        new dialog window that is shown after clicking on listbox widget item
        from SecondaryWindow instance

    command : str variable
        passed from SecondaryWindow instance, it's necessary to open proper
        dialogbox depending on which object is selected

    value : tuple(int x, int y) or single int variable
        passed value of dict object from SecondaryWindow instance

    index : int variable
        index of currently selected item in listbox widget from SecondaryWindow
        instance


    Methods
    ----------
    menu_moveTo()
        if the passed command is 'moveTo' then it creates dialogbox which allows
        user to change x, y coordinates assigned to command or remove it completly
        from list_of_orders list

    menu_click()
        if the passed command is 'rclick' or 'lclick' then it creates dialogbox
        which allows user to change number of clicks assigned to command or
        remove it completly from list_of_orders list

    edit_command()
        the method that handles the 'edit_button' click event

    delete_command()
        the method that handles the 'delete_button' click event

    cancel_command()
        the method that handles the 'cancel_button' click event

    """

    def __init__(self, master, parent, command, value, index):
        """
        Constructor

        Parameters
        ----------
        master : tkinter.Tk object
            root widget from tkinter package

        parent : SecondaryWindow instances
            passed instance of SecondaryWindow to dialogbox

        command : str variable
            passed 'command' from currently selected item in listbox object
            from SecondaryWindow instance

        value : tuple(int x, int y) or single int variable
            passed 'command' value from currently selected item in listbox object
            from SecondaryWindow instance

        index : int variable
            passed index of currently selected item in listbox object
            from SecondaryWindow instance
        """

        self.root = master
        self.parent = parent
        self.dialog_window = tk.Toplevel()
        self.dialog_window.resizable(False, False)
        self.command = command
        self.value = value
        self.index = index
        if self.command == 'moveTo':
            self.menu_moveTo()
        else:
            self.menu_click()

    def menu_moveTo(self):
        """
        sets title of the dialogbox to 'moveTo'
        and creates tkinter widgets and pack them into dialogbox:

        2 tkinter.Label (x, y)
        2 tkinter.Entry (x value, y value)
        3 tkinter.Buttons (EDIT, DELETE, CANCEL)

        """

        self.dialog_window.title('moveTo')
        x, y = self.value
        self.x_label = tk.Label(self.dialog_window, text = 'x:')
        self.y_label = tk.Label(self.dialog_window, text = 'y:')
        self.x_entry = tk.Entry(self.dialog_window, width = 7)
        self.x_entry.insert(0, str(x))
        self.y_entry = tk.Entry(self.dialog_window, width = 7)
        self.y_entry.insert(0, str(y))
        self.edit_button = tk.Button(self.dialog_window, text = 'EDIT', command = self.edit_command)
        self.delete_button = tk.Button(self.dialog_window, text = 'DELETE', command = self.delete_command)
        self.cancel_button = tk.Button(self.dialog_window, text = 'CANCEL', command = self.cancel_command)

        self.x_label.grid(row = 0, column = 0)
        self.x_entry.grid(row = 0, column = 1)
        self.y_label.grid(row = 0, column = 2)
        self.y_entry.grid(row = 0, column = 3)
        self.edit_button.grid(row = 1, column = 0, sticky = 'W')
        self.delete_button.grid(row = 1, column = 1, columnspan = 2, sticky = "WE")
        self.cancel_button.grid(row = 1, column = 3, sticky = 'E')

    def menu_click(self):
        """
        sets title of the dialogbox to 'click'
        creates tkinter widgets and pack them into dialogbox:

        1 tkinter.Label (clicks)
        1 tkinter.Entry (number of clicks)
        3 tkinter.Buttons (EDIT, DELETE, CANCEL)

        """

        self.dialog_window.title('click')
        self.click_label = tk.Label(self.dialog_window, text = 'number of clicks:')
        # possible solution but not as precise as the entry widget
        # can be added in feauter, but is not necessary
        #self.click_slider = tk.Scale(self.dialog_window, from_ = 1, to = 200, orient = tk.HORIZONTAL, showvalue = self.value, resolution = 1)
        self.click_entry = tk.Entry(self.dialog_window, width = 7)
        self.click_entry.insert(0, str(self.value))
        self.edit_button = tk.Button(self.dialog_window, text = 'EDIT', command = self.edit_command)
        self.delete_button = tk.Button(self.dialog_window, text = 'DELETE', command = self.delete_command)
        self.cancel_button = tk.Button(self.dialog_window, text = 'CANCEL', command = self.cancel_command)

        self.click_label.grid(row = 0, column = 0, columnspan = 3)
        self.click_entry.grid(row = 1, column = 0, columnspan = 3)
        self.edit_button.grid(row = 2, column = 0)
        self.delete_button.grid(row = 2, column = 1)
        self.cancel_button.grid(row = 2, column = 2)

    def edit_command(self):
        """
        edit selected item value in list_of_orders listbox in passed
         SecondaryWindow instance

        """

        if self.command == 'moveTo':
            (x, y) = (int(self.x_entry.get()), int(self.y_entry.get()))
            self.parent.list_of_orders[self.index] = {self.command : (x, y)}
            self.parent.order_list_update()
            self.dialog_window.destroy()
        else:
            clicks = int(self.click_entry.get())
            self.parent.list_of_orders[self.index] = {self.command : clicks}
            self.parent.order_list_update()
            self.dialog_window.destroy()

    def delete_command(self):
        """
        removes selected item in list_of_orders listbox in passed
         SecondaryWindow instance
        """

        self.parent.list_of_orders.pop(self.index)
        self.parent.order_list_update()
        self.dialog_window.destroy()

    def cancel_command(self):
        """
        simply destroys dialogbox window
        """

        self.dialog_window.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()
