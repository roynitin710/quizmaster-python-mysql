from tkinter import *
from quiz import Quiz
from tkinter import ttk
from tkinter import messagebox
from database import DB


class GUI:

    def __init__(self):
        # connect to database
        self.database = DB()
        # create the gui
        self.root = Tk()
        self.root.title('Quiz Master')
        self.root.maxsize(615, 412)
        self.root.minsize(615, 412)
        self.root.configure(background='#030303')
        background = self.import_image(png="img/background.png", x_axis=0, y_axis=0)

        self.load_welcome_gui()

    # clears the screen
    def clear_gui(self, i=0):
        for i in self.root.pack_slaves()[i:]:
            i.destroy()

    # imports a .png file
    def import_image(self, png, x_axis=0, y_axis=0):
        image = PhotoImage(file=png)
        label = Label(self.root, image=image)
        label.place(x=x_axis, y=y_axis)
        return image

    # adding text to the screen
    def create_label(self, text="Blank", bg='#000000', fg='#ffffff', font_style='', font_size=10, font_type='', up=10, down=10):
        label = Label(self.root, text=text, bg=bg, fg=fg)
        label.pack(pady=(up, down))
        label.configure(font=(font_style, font_size, font_type))
        return label

    # input field
    def input_field(self, field_name, up=1, down=1):
        input = Entry(self.root)
        input.insert(0, field_name)
        input.pack(pady=(up, down), ipadx=60, ipady=10)
        return input

    # welcome screen
    def load_welcome_gui(self):
        self.clear_gui()
        # heading
        self.create_label(": Quiz Master :", '#000000', '#ffff00', 'Roman', 22, 'bold', 27, 10)
        # sub_heading
        self.create_label("Welcome to Quiz Master", '#000000', '#ffff00', 'verdana', 12, 'bold', 30, 10)
        # go to login page
        Button(self.root, text="Already have an account? | Log In", bg='#050542', fg='#f6f0f0', width=30, height=2, cursor= 'hand2', command=lambda: self.load_login_gui()).pack(pady=(10, 10))
        # divider
        self.create_label("-------------- or --------------", '#000000', '#ffff00', 'verdana')
        # create an account
        Button(self.root, text="Don't have an account? | Sign Up", bg='#050542', fg='#f6f0f0', width=30, height=2, cursor= 'hand2', command=lambda: self.load_signup_gui()).pack(pady=(10, 10))

        self.root.mainloop()

    # load signup screen
    def load_signup_gui(self):
        self.clear_gui(1)
        # inputs
        self.name_input = self.input_field('Name', up=40, down=5)
        self.email_input = self.input_field('Email', up=5, down=5)
        self.password_input = self.input_field('Password', up=5, down=5)
        # create the account
        Button(self.root, text="Sign Up", font=('verdana', 10, 'bold'), bg='#050542', fg='#f6f0f0', width=20, height=1, cursor= 'hand2', command=lambda: self.perform_signup()).pack(pady=(20, 20))
        # go to login page
        Button(self.root, text="Already have an account? | LogIn", bg='#050542', fg='#f6f0f0', width=30, height=1, cursor= 'hand2', command=lambda: self.load_login_gui()).pack(pady=(30, 10))

    # perform signup
    def perform_signup(self):
        # fetch input provided by the user
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()
        # check for email
        if ('@' in email) & (email.endswith(".com")):
            # check length of password
            if 5 <= len(password) <= 20:
                # register
                response = self.database.register_user(name, email, password)
                if response == 1:
                    messagebox.showinfo("Quiz Master", "Registration Successful")
                    self.load_login_gui()
                elif response == -1:
                    messagebox.showerror("Quiz Master", "Email already exists")
                else:
                    messagebox.showerror("Quiz Master", "Some error occurred!")
            else:
                messagebox.showerror("Quiz Master", "Password must be of 5 to 20 characters")
        else:
            messagebox.showerror("Quiz Master", "Please enter a valid email")

    # load login screen
    def load_login_gui(self):
        self.clear_gui(1)
        # inputs
        self.email_input = self.input_field('Email', up=70, down=5)
        self.password_input = self.input_field('Password', up=5, down=5)
        # login
        Button(self.root, text="Log In", font=('arial', 10, 'bold'), bg='#050542', fg='#f6f0f0', width=20, height=1, cursor='hand2', command=lambda: self.perform_login()).pack(pady=(20, 20))
        # go to signup page
        Button(self.root, text="Don't have an account? | Sign Up", bg='#050542', fg='#f6f0f0', width=30, height=1, cursor= 'hand2', command=lambda: self.load_signup_gui()).pack(pady=(50, 10))

    # perform login
    def perform_login(self):
        # fetch input provided by the user
        email = self.email_input.get()
        password = self.password_input.get()
        # check and login
        data = self.database.login_user(email, password)
        if data == 0:
            messagebox.showerror("Quiz Master", "Some error occurred!")
        else:
            if len(data) == 0:
                messagebox.showerror("Quiz Master", "Incorrect email or password")
            else:
                # save user info of logged in user
                self.user_id = data[0][0]
                self.load_category()

    # choose category
    def load_category(self):
        self.clear_gui(1)
        # fetch logged in user data from database
        data = self.database.fetch_user_data(self.user_id)
        # welcome
        self.create_label(text="Welcome, Quiz Master " + data[0][1], bg='#000000', fg='#52ade2', font_style='', font_size=15, font_type='', up=10, down=5)
        # select category
        self.create_label(text="Choose a category: -", bg='#000000', fg='#ffffff', font_style='', font_size=12, font_type='', up=15, down=10)
        Button(self.root, text="Computer Science", bg='#050542', fg='#f6f0f0', width=20, height=1, cursor= 'hand2', command=lambda: self.load_menu(18)).pack(pady=(7, 5))
        Button(self.root, text="Mathematics", bg='#050542', fg='#f6f0f0', width=20, height=1, cursor= 'hand2', command=lambda: self.load_menu(19)).pack(pady=(7, 5))
        Button(self.root, text="Gadgets", bg='#050542', fg='#f6f0f0', width=20, height=1, cursor= 'hand2', command=lambda: self.load_menu(30)).pack(pady=(7, 5))
        Button(self.root, text="General Knowledge", bg='#050542', fg='#f6f0f0', width=20, cursor= 'hand2', height=1, command=lambda: self.load_menu(9)).pack(pady=(7, 5))
        Button(self.root, text="Log Out", font=('arial', 8, 'bold'), bg='#832b19', fg='#f6f0f0', width=20, height=1, cursor= 'hand2', command=lambda: self.logout()).pack(pady=(35, 10))

    # menu
    def load_menu(self, category):
        self.clear_gui(1)
        # fetch logged in user data from database
        data = self.database.fetch_user_data(self.user_id)
        self.create_label(text="Welcome, Quiz Master " + data[0][1], bg='#000000', fg='#ffffff', font_style='', font_size=15, font_type='', up=10, down=10)
        # select what to do
        Button(self.root, text="Take The Quiz", bg='#050542', fg='#f6f0f0', width=30, height=2, cursor= 'hand2', command=lambda: self.extract_quiz(category)).pack(pady=(10, 10))
        Button(self.root, text="View The Score Board", bg='#050542', fg='#f6f0f0', width=30, height=2, cursor= 'hand2', command=lambda: self.score_board(category)).pack(pady=(10, 10))
        Button(self.root, text="Back", bg='#050542', fg='#f6f0f0', width=30, height=2, cursor= 'hand2', command=lambda: self.load_category()).pack(pady=(10, 10))

    # conduct the quiz
    def extract_quiz(self, category):
        self.clear_gui(1)
        # conduct quiz
        quiz = Quiz()
        check = quiz.connect(category)
        if check == 0:
            # poor/no internet connection
            messagebox.showerror("Quiz Master", "Please check your internet connection and try again.")
            self.load_menu(category)
        else:
            # extract from url
            self.questions = quiz.extract_questions()
            self.options = quiz.extract_options()
            self.answers = quiz.extract_answers()

            update_score = 0
            correct_ans = 0
            self.conduct_quiz(0, update_score, correct_ans, category)

    def conduct_quiz(self, i, update_score, correct_ans, category):
        self.clear_gui(1)
        # fit to screen
        que = self.questions[i].split(" ")
        question = ["Q", str(i + 1), ". "]
        question = question + que
        for _ in range(1, len(question)):
            if _ % 8 == 0:
                question.insert(_ + 1, "\n")
        question = " ".join(question)
        self.create_label(text=question, bg='#000000', fg='#ffffff', font_style='', font_size=10, font_type='', up=10,
                          down=10)
        for j in range(4):
            Button(text="{}. ".format(chr(97 + j)) + self.options[i][j], bg='#050542', fg='#ffffff', width=30, height=1, cursor='hand2', command=lambda: self.check_answer(i, j, update_score, correct_ans, category)).pack(pady=(10, 10))
        # skip button
        Button(text="Skip", bg='#832b19', fg='#f6f0f0', width=20, height=1, cursor='hand2', command=lambda: self.check_answer(i, "Skip", update_score, correct_ans, category)).pack(pady=(10, 10))
        # Note
        self.create_label(text="Note: Correct Ans= +5, Wrong Ans= -2, Skip= +0", bg='#000000', fg='#ffffff', font_style='', font_size=7, font_type='', up=10, down=10)

    def check_answer(self, i, j, update_score, correct_ans, category):
        if j == "Skip":
            update_score += 0
        elif self.options[i][j] == self.answers[i]:
            update_score += 5
            correct_ans += 1
        else:
            update_score -= 2
        if i >= 9:
            self.update_score_db(update_score, correct_ans, category)
        else:
            self.conduct_quiz(i+1, update_score, correct_ans, category)

    def update_score_db(self, update_score, correct_ans, category):
        D = {18: 'score_cs', 19: 'score_maths', 30: 'score_gadgets', 9: 'score_gk'}
        self.database.update_score_in_db(update_score, D[category], self.user_id)
        self.clear_gui(1)
        self.create_label(text=": Result :", font_size=20, down=20)
        self.create_label(text="No. of Correct Answers= {}".format(correct_ans), font_size=20)
        self.create_label(text="Marks Obtained= {}".format(update_score), font_size=20)
        Button(text="View Score Board", bg='#050542', fg='#f6f0f0', width=30, height=1, cursor='hand2', command=lambda: self.score_board(category)).pack(pady=(20, 10))

    # view score bard
    def score_board(self, category):
        self.clear_gui(1)
        D = {18: 'score_cs', 19: 'score_maths', 30: 'score_gadgets', 9: 'score_gk'}
        # fetch score of all users from database of the specific category
        data = self.database.fetch_score(D[category])
        # display scores
        leader_board = ttk.Treeview(self.root)
        leader_board['columns'] = ("Name", "Email ID", "Score")
        # formate the columns
        leader_board.column("#0", anchor=CENTER, width=35)
        leader_board.column("Name", anchor=E, width=100)
        leader_board.column("Email ID", anchor=E, width=140)
        leader_board.column("Score", anchor=CENTER, width=40)
        # create heading
        leader_board.heading("#0", text="Rank ", anchor=E)
        leader_board.heading("Name", text="Name ", anchor=E)
        leader_board.heading("Email ID", text="Email ID ", anchor=E)
        leader_board.heading("Score", text="Score ", anchor=E)
        # add data
        count = 0
        for i in data:
            if i[0] == self.user_id:
                leader_board.insert(parent='', index='end', iid=count, text=count + 1, values=(i[1], i[2], i[3]))
            else:
                leader_board.insert(parent='', index='end', iid=count, text=count + 1, values=(i[1], i[2], i[3]))
            count += 1

        leader_board.pack(pady=20)

        Button(self.root, text="Back to Menu", bg='#050542', fg='#f6f0f0', width=20, height=1, cursor= 'hand2', command=lambda: self.load_menu(category)).pack(pady=(10, 10))
        self.create_label(text="Note: Want to make it better? Retake the quiz.", font_size=7, up=3, down=10)

    # logout
    def logout(self):
        self.user_id = None
        self.load_welcome_gui()
