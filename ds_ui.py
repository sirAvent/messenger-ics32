import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import ds_messenger
from ds_messenger import DirectMessage


class loadedUser():
    """
    A loadedUser object used for storing data on the currently loaded user account on the UI.
    Useful for finding current username and password.

    Attributes:

    username - The username of the currently loaded account.
    password - The password of the currently loaded account.
    """
    def __init__(self, username=None, password=None):
        global current_username
        global current_password
        self.username = current_username
        self.password = current_password


    def set_password(self, entry:str) -> None:
        '''
        Set the password attribute to the inputted string.
        Useful when a new user is logged in.
        '''
        self.password = entry


    def set_username(self, entry:str) -> None:
        '''
        Set the username attribute to the inputted string.
        Useful when a new user is logged in.
        '''
        self.username = entry


    def set_dsuserver(self, entry:str) -> None:
        '''
        Set the dsusver attribute to the inputted string.
        Use for third-party applications since the default
        server is the ICS 32's distributed address.
        '''
        self.dsuserver = entry


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        global clicked_user
        clicked_user = None
        #clicked_user is the currently selected user in the Message Tree widget.

        # a list of the DirectMessage objects, same structure needed for message objects
        self._messages = [DirectMessage]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    

    def node_select(self, event) -> None:
        """
        Update the entry_editor with the full message entry when the corresponding node in the message
        is selected.
        """
        index = int(self.messages_tree.selection()[0]) - 1
        global clicked_user
        clicked_user = (self._messages[index])
        try:
            global current_user
            global chat_history
            #Call the global variables. Useful when other classes change the variable
            current_user = ds_messenger.DirectMessenger('168.235.86.101', current_username, current_password)
            recieved_messages = (current_user.retrieve_all())
            new_messages = (current_user.retrieve_new())
            chat_history = []
            self.set_chat_entry('')
            for message in recieved_messages[::-1]:
                if message['from'] == clicked_user:
                    self.add_chat_entry(clicked_user + ': ' + message['message']+'\n')
                    chat_history.append(clicked_user + ': ' + message['message']+'\n') 
        except:
            #Except branch will execute when there is no currently loaded user.
            pass


    def get_text_entry(self) -> str:
        """
        Return the text that is currently displayed in the entry_editor widget.
        """
        return self.entry_editor.get('1.0', 'end').rstrip()


    def set_chat_entry(self, text:str) -> None:
        """
        Set the text to be displayed in the entry_editor widget.
        This method is useful for clearing the widget, just pass an empty string.
        """
        self.chat.config(state=tk.NORMAL)
        self.chat.delete(1.0, tk.END)
        self.chat.insert(1.0, text)
        self.chat.config(state=tk.DISABLED)

    
    def add_chat_entry(self, text:str) -> None:
        """
        Append the chat to be displayed in the chat widget.
        This method is useful adding multiple lines of messages from a user.
        """
        self.chat.config(state=tk.NORMAL)
        self.chat.insert(1.0, text)
        self.chat.config(state=tk.DISABLED)


    def set_text_entry(self, text:str) -> None:
        """
        Set the text to be displayed in the entry_editor widget.
        This method is useful for clearing the widget, just pass an empty string.
        """
        self.entry_editor.delete(1.0, tk.END)
        self.entry_editor.insert(1.0, text)
    

    def set_messages(self, messages:list) -> None:
        """
        Populate the self._messages attribute with messages from a user.
        """
        self._messages = messages
        self.messages_tree.delete(*self.messages_tree.get_children())
        for i in range(0, len(self._messages)):
            self._insert_message_tree(i, self._messages[i])


    def insert_message(self, message: DirectMessage) -> None:
        """
        Insert a single DirectMessage user to the message_tree widget.
        """
        self._clicked_user = message
        self._messages.append(message)
        self._insert_message_tree(len(self._messages), message)


    def reset_ui(self) -> None:
        """
        Reset all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DirectMessage account is loaded, for example.
        """
        self.set_text_entry("")
        self._messages = []
        for item in self.messages_tree.get_children():
            self.messages_tree.delete(item)


    def _insert_message_tree(self, id, message: DirectMessage) -> None:
        """
        Insert a username into the messages_tree widget.
        """
        entry = message
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if entry == None:
            return None
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.messages_tree.insert('', id, id, text=entry)
    

    def _draw(self) -> None:
        """
        Call only once upon initialization to add widgets to the frame
        """
        messages_frame = tk.Frame(master=self, width=250)
        messages_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.messages_tree = ttk.Treeview(messages_frame)
        self.messages_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.messages_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=5)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.entry_editor = tk.Text(editor_frame, width=0, height=10, bg= 'white')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=0, pady=0)
        
        self.chat = tk.Text(editor_frame, width=0, bg='white', state=tk.DISABLED)
        self.chat.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)

        self.chat_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.chat['yscrollcommand'] = self.chat_scrollbar.set
        self.chat_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
        



class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None, update_callback=None, add_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._update_callback = update_callback
        self._add_callback = add_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    
    def update_click(self) -> None:
        """
        Call the callback function specified in the update_callback class attribute, if
        available, when the update widget has been clicked.
        """
        if self._update_callback is not None:
            self._update_callback()

  
    def save_click(self) -> None:
        """
        Call the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()

            
    def add_click(self) -> None:
        """
        Call the callback function specified in the add_callback class attribute, if
        available, when the add_button has been clicked.
        """
        if self._add_callback is not None:
            self._add_callback()


    def set_status(self, message) -> None:
        """
        Update the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)
    

    def _draw(self) -> None:
        """
        Call only once upon initialization to add widgets to the frame
        """
        save_button = tk.Button(master=self, text="Send", width=10, bg ="light blue")
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        update_button = tk.Button(master=self, text="Update Messages", width=15, bg ="light blue")
        update_button.configure(command=self.update_click)
        update_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.add_user = tk.Button(master=self, text="Add User", width=20, bg ="light blue", state= tk.DISABLED)
        self.add_user.configure(command=self.add_click)
        self.add_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Currently Logged In As: " + str(current_username))
        self.footer_label.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5)



class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame.

    Contain the attributes for current username and password. Useful for updating
    other widgets.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        global current_username
        global current_password
        self.root = root
        self._is_online = False
        current_username = None
        current_password = None

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()


    def add_user(self) -> str:
        """
        Open a new window asking for a user.

        Reference Code taken from DJANGOCENTRAL, see README.txt
        """
        ROOT = tk.Tk()
        ROOT.withdraw()
        USER_INP = simpledialog.askstring(title="New User Window", prompt='' + '\n\nAdd User.')
        if USER_INP != None:
            try:
                return USER_INP
            except Exception as e:
                print(e)
        else:
            #else branch will execute when the user inputs an empty string. Returning none ensures that the username does not become populated with the empty string.
            return None
        


    def add(self) -> None:
        """
        Add a user to the Tree Widget
        """
        userToAdd = self.add_user()
        self.body.insert_message(userToAdd)


    def send_message(self) -> None:
        """
        Send the text currently in the entry_editor widget to the active User.
        """
        try:
            message=(self.body.get_text_entry())
            if message != '':
                global chat_history
                self.body.set_text_entry("")
                sent_status = current_user.send(message, clicked_user)
                new_messages = current_user.retrieve_new()
                if sent_status is True:
                    chat_history = chat_history[::-1]
                    chat_history.append(current_username + ': ' + message + '\n')
                    chat_history = chat_history[::-1]
                    self.body.set_chat_entry('')
                    for message in chat_history:
                        self.body.add_chat_entry(message)
                    if new_messages != []:
                        for message in new_messages:
                            if message['from'] == clicked_user:
                                chat_history = chat_history[::-1]
                                chat_history.append(clicked_user + ': ' + message['message']+'\n')
                                chat_history = chat_history[::-1]
                                self.body.set_chat_entry('')
                            for message in chat_history:
                                self.body.add_chat_entry(message)
        except Exception as e:
            #except branch will execute when there is no selected user to send a message to.
            pass


    def update_chat(self) -> None:
        '''
        Populate the chat widget with newly recieved messages.
        '''
        global chat_history
        #global call so that both user and receiver will have their messages in order and displayed.
        try:
            new_messages = current_user.retrieve_new()
            if new_messages != []:
                for message in new_messages:
                    if message['from'] == clicked_user:
                        chat_history = chat_history[::-1]
                        chat_history.append(clicked_user + ': ' + message['message']+'\n')
                        chat_history = chat_history[::-1]
                        self.body.set_chat_entry('')
                    for message in chat_history:
                        self.body.add_chat_entry(message)
        except:
            #Except block will execute when there is no selected user to recieve messages from
            pass

            

    def log_in(self) -> None:
        '''
        Open a new window populating username and password from user input.
        
        Code found by Avent Chiu from https://www.simplifiedpython.net/python-gui-login/
        '''
        try:
            #Close another login screen if it already exists. Prevent users from spamming new windows
            self.login_screen.destroy()
        except:
            pass
        self.login_screen = tk.Tk()
        self.login_screen.title("Login")
        self.login_screen.geometry("300x250")
         
        self.username = tk.StringVar()
        self.password = tk.StringVar()
         
        tk.Label(self.login_screen, text=("Currently Logged In as:\n" + str(current_username) + "\nPlease enter details below")).pack()
        tk.Label(self.login_screen, text="").pack()
            
        self.username_lable = tk.Label(self.login_screen, text="Username * ")
        self.username_lable.pack()
         
        self.username_entry = tk.Entry(self.login_screen, textvariable=self.username)
        self.username_entry.pack()
           
        self.password_lable = tk.Label(self.login_screen, text="Password * ")
        self.password_lable.pack()
            
        self.password_entry = tk.Entry(self.login_screen, textvariable=self.password)
        self.password_entry.pack()
            
        tk.Label(self.login_screen, text="").pack()
            
        tk.Button(self.login_screen, text="Login", width=10, height=1, command = self.login_user).pack()

        

    def login_user(self) -> None:
        '''
        Populate namespace with newly inputted username and password.
        Responsible for closing the login window when login button is pressed.
        '''
        username_info = self.username_entry.get()
        password_info = self.password_entry.get()
        global current_username
        current_username = username_info
        global current_password
        #global variables because many methods are able to change it. Ensure that the variables are accurate.
        current_password = password_info
        self.login_screen.destroy()
        self.footer.set_status('Currently Logged In As: ' + str(username_info))
        self.body.reset_ui()
        self.body.set_chat_entry('')
        if current_username != '':
            self.footer.add_user['state'] = tk.NORMAL
        else:
            self.footer.add_user['state'] = tk.DISABLED
            self.footer.set_status('Currently Logged In As: None')

    
    def _draw(self) -> None:
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        
        menu_bar.add_command(command=self.log_in, label='Log In')
        #Log in button

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, save_callback=self.send_message, update_callback=self.update_chat, add_callback = self.add)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Messenger App")
    main.geometry("720x280")
    main.option_add('*tearOff', False)
    MainApp(main)
    main.update()
    main.geometry("720x600")
    main.minsize(720, 600)
    main.mainloop()
    
