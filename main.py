import customtkinter as ctk #customtkinter 4.6.3
import mysql.connector
import tkinter.messagebox as tmsg
import _tkinter # For _tkinter.TclError




root = ctk.CTk()
root.geometry("1050x750")
root.resizable(False,False)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 


# Some constants for theme 
FONT = ("Roboto",20)
HOVER_COLOUR = "#77C3F5" #Some blue colour
FG_COLOUR = "#CED2DD" #grey colour nearly same as the background colour
BORDER_WIDTH = 3

def page():
    """This is the function which will be executed when the user press the 'submit' button in home page"""
    try:
        global connection
        connection= mysql.connector.connect(host="localhost",user=username_var.get(),
        passwd=password_var.get())
        connection.autocommit = True
    except mysql.connector.errors.ProgrammingError:
        tmsg.showerror("Incorrect Username or Password","The entered Username or Password is invalid")

    else:
        global cursor
        cursor = connection.cursor()
        cursor.execute("show databases")
        datbases = [database for database in cursor]
        if not ('marks_management_system',) in datbases:
            cursor.execute("create database marks_management_system")
        cursor.execute("use marks_management_system")
        cursor.execute("show tables")
        tables = [table for table in cursor]
        if ('marks_student',) not in tables:
            cursor.execute("create table marks_student(admission_num int primary key,name varchar(200) not null,marks int not null)")

        choice_home_page = optionmenu_var.get()
        code_teacher = teacher_var.get()
        if choice_home_page == "Teacher":
            if code_teacher == "*123":
                Home_page.destroy()
                teacher_interface()
            else:
                tmsg.showerror(
                    f"Unauthorised teacher",
                    f"The entered name of teacher {code_teacher} is not valid please try again"
                )
        if choice_home_page == "Student":
            Home_page.destroy()
            student_interface()

#Home page

Home_page = ctk.CTkFrame(root,height=750,width=1050)
root.title("Marks Management System")
root.iconbitmap("icon.ico")
optionmenu_var = ctk.StringVar()
optionmenu_var.set("Teacher")
teacher_var = ctk.StringVar()


ctk.CTkLabel(Home_page,
            text="Choose your role",
            justify=ctk.CENTER,
            text_font=FONT).place(x=20,y=20)   

ctk.CTkOptionMenu(Home_page,
                    values=["Teacher","Student"],
                    variable=optionmenu_var,
                    width=175,
                    height=40,
                    dropdown_hover_color= HOVER_COLOUR,
                    text_font= FONT, 
                    dropdown_text_font= FONT  
                    ).place(x=430,y=20)

ctk.CTkLabel(Home_page, text="Code of teacher",
            text_font=FONT   
            ).place(x=20,y=165)

ctk.CTkEntry(Home_page,
            textvariable=teacher_var,
            text_font=FONT,
            show = "*",  
            width=200).place(x=430,y=165)

button = ctk.CTkButton(Home_page,
                    text="Submit",
                    corner_radius=15,
                    command=page,
                    border_width = BORDER_WIDTH,
                    text_font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR)
button.place(x=430,y=500)

ctk.CTkLabel(Home_page,
            text="MySQL-Username",
            text_font = FONT
            ).place(x=20,y=300)

ctk.CTkLabel(Home_page,
            text="MySQL-Password",
            text_font = FONT
            ).place(x=20,y=440)

username_var = ctk.StringVar()
password_var = ctk.StringVar()

ctk.CTkEntry(Home_page,
            textvariable=username_var,
            text_font=FONT,
            width=200
            ).place(x=430,y=300)

ctk.CTkEntry(Home_page,
            textvariable=password_var,
            text_font=FONT,
            width=300,
            show = "*"
            ).place(x=430,y=440)
Home_page.pack(fill="both",padx=30,pady=30)

def teacher_interface():
    global teacher_interface_frame
    root.title("Choose an option")
    root.geometry("650x600")

    teacher_interface_frame = ctk.CTkFrame(height=750,width=750)

    ctk.CTkLabel(teacher_interface_frame,
                text="PRESS ANY OF THE BUTTON TO",
                text_font=FONT
                ).place(x=100,y=100)

    ctk.CTkButton(teacher_interface_frame,
                    text='ISSUE MARKS OF STUDENTS',
                    command=teacher_interface_submit,
                    border_width = BORDER_WIDTH,
                    text_font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR).place(x=100,y=200)
    
    ctk.CTkButton(teacher_interface_frame,
                    text='UPDATE MARKS OF STUDENTS',
                    command=teacher_interface_update,
                    border_width = BORDER_WIDTH,
                    text_font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR).place(x=80,y=300)

    ctk.CTkButton(teacher_interface_frame,
                    text='DELETE DETAILS OF STUDENTS',
                    command=teacher_interface_delete,
                    border_width = BORDER_WIDTH,
                    text_font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR).place(x=100,y=400)
    teacher_interface_frame.pack(fill="both",padx=30,pady=30)



def teacher_interface_submit():
    """This interface is used by techer to issue the marks"""

    teacher_interface_frame.destroy()
    root.title("Issue Marks")
    root.geometry("750x750")
    teacher_page_submit = ctk.CTkFrame(height=750,width=750)
    student_name_record = ctk.CTkLabel(teacher_page_submit,
                                    text='Name',
                                    text_font=FONT #type:ignore
                                    )
    student_admi_record = ctk.CTkLabel(teacher_page_submit,
                                    text="Admission no.",
                                    text_font=FONT #type:ignore
                                    )
    student_marks_record = ctk.CTkLabel(teacher_page_submit,
                                    text="Percentage",
                                    text_font=FONT #type:ignore
                                    )
    student_name_record.place(x=20,y=20)
    student_admi_record.place(x=20,y=165)
    student_marks_record.place(x=20,y=310)
    
    global nameval, admival, marksval
    
    nameval = ctk.StringVar()
    admival = ctk.IntVar()
    marksval = ctk.IntVar()

    ctk.CTkEntry(teacher_page_submit,
            textvariable=nameval,
            text_font=FONT,   
            width=200
            ).place(x=430,y=20)

    ctk.CTkEntry(teacher_page_submit,
            textvariable=admival,
            text_font=FONT,   
            width=200
            ).place(x=430,y=165)

    ctk.CTkEntry(teacher_page_submit,
            textvariable=marksval,
            text_font=FONT,   
            width=200
            ).place(x=430,y=310)

    ctk.CTkButton(teacher_page_submit,
            text="Submit",
            command=submit_results,
            border_width = 3,
            text_font=FONT,
            border_color= HOVER_COLOUR,
            hover_color= HOVER_COLOUR,
            fg_color=FG_COLOUR
            ).place(x=430,y=450)

    ctk.CTkButton(teacher_page_submit,
            text="Exit",
            command=exit,
            border_width = 3,
            text_font=FONT,
            border_color= HOVER_COLOUR,
            hover_color= HOVER_COLOUR,
            fg_color=FG_COLOUR
            ).place(x=20,y=450)
    teacher_page_submit.pack(fill="both",padx=30,pady=30)

def submit_results():
    try:
        global marks, admission_num, name_student
        name_student = nameval.get()
        validate_name(name_student)
        marks = marksval.get()
        if marks > 100:
            raise _tkinter.TclError
        admission_num = admival.get()
        try:
            cursor.execute(f"insert into marks_student values{admission_num,name_student,marks}")
            connection.commit()
            nameval.set("")
            marksval.set(0)
            admival.set(0)
        except mysql.connector.errors.IntegrityError:
            tmsg.showerror( 
                        f"Error",
                        f"The marks of the student {admission_num} already exists please try another"
                    )
    except _tkinter.TclError:
        tmsg.showerror("Error",
                        f"The entered percentage or admission number is not valid")


def teacher_interface_update():
    teacher_interface_frame.destroy()
    root.title("Update Marks")
    global update_admivar,update_marksvar,update_namevar
    update_admivar = ctk.IntVar()
    update_marksvar = ctk.IntVar()
    update_namevar = ctk.StringVar()

    teacher_interface_update_frame = ctk.CTkFrame(height=750,width=750)
    ctk.CTkLabel(teacher_interface_update_frame,
                text="Admisson Number",
                text_font=FONT
                ).place(x=20,y=20)

    ctk.CTkEntry(teacher_interface_update_frame,
                height=40,width=200,
                text_font=FONT,
                textvariable=update_admivar
                ).place(x=300,y=20)

    ctk.CTkLabel(teacher_interface_update_frame,
                text="New-Name",
                text_font=FONT
                ).place(x=20,y=120)

    ctk.CTkEntry(teacher_interface_update_frame,
                height=40,
                width=200,
                text_font=FONT,
                textvariable=update_namevar
                ).place(x=300,y=120)

    ctk.CTkLabel(teacher_interface_update_frame,
                text="New-Marks",
                text_font=FONT
                ).place(x=20,y=240)

    ctk.CTkEntry(teacher_interface_update_frame,
                height=40,
                width=200,
                text_font=FONT,
                textvariable=update_marksvar
                ).place(x=300,y=240)

    ctk.CTkLabel(teacher_interface_update_frame,
                text="**By keeping the Admission number the",
                text_font=FONT
                ).place(x=20,y=340)

    ctk.CTkLabel(teacher_interface_update_frame,
                text="same make changes in name and marks only",
                text_font=FONT
                ).place(x=20,y=380)

    ctk.CTkButton(teacher_interface_update_frame,
                text='submit',
                command=update_results,
                fg_color=FG_COLOUR,
                hover_color= HOVER_COLOUR,
                border_color= HOVER_COLOUR,
                text_font=FONT,
                border_width = 3
                ).place(x=125,y=430)

    teacher_interface_update_frame.pack(fill="both",padx=30,pady=30)
    

def update_results():
    try:
        updated_admission_num = update_admivar.get()
        updated_marks = update_marksvar.get()
        updated_name = update_namevar.get()
        validate_name(updated_name)
        if updated_marks > 100:
            raise _tkinter.TclError
    except _tkinter.TclError:
        tmsg.showerror("","Invalid Details please try again")
    else:
        cursor.execute(f"update marks_student set marks={updated_marks},name='{updated_name}' where admission_num = {updated_admission_num}")
        update_admivar.set(0)
        update_marksvar.set(0)
        update_namevar.set("")

def teacher_interface_delete():

    teacher_interface_frame.destroy()
    root.title("Delete Marks")
    root.geometry("650x300")
    teacher_interface_delete_frame = ctk.CTkFrame(height=750,width=750)
    global delete_admivar
    delete_admivar = ctk.IntVar()
    ctk.CTkLabel(teacher_interface_delete_frame,
                text='Enter the admisson number of the student',
                text_font=FONT
                ).place(x=60,y=20)

    ctk.CTkLabel(teacher_interface_delete_frame,
                text='whose details you want to delete',
                text_font=FONT
                ).place(x=80,y=60)

    ctk.CTkEntry(teacher_interface_delete_frame,
                textvariable=delete_admivar,
                text_font=FONT,
                height=40,
                width=200
                ).place(x=160,y=120)

    ctk.CTkButton(teacher_interface_delete_frame,
                text='submit',
                command=delete_results,
                fg_color=FG_COLOUR,
                hover_color= HOVER_COLOUR,
                border_color= HOVER_COLOUR,
                text_font=FONT,
                border_width = 3
                ).place(x=190,y=180)

    teacher_interface_delete_frame.pack(fill="both",padx=20,pady=20)

def delete_results():
    try:
        deleted_admission_num = delete_admivar.get()
        delete_admivar.set(0)
    except _tkinter.TclError:
        tmsg.showinfo("","Error in admission_number")

    else:
        cursor.execute(f"delete from marks_student where admission_num = {deleted_admission_num}")

def student_interface():
    """This is the function which will be executed when user select 'student' option in home page and press 'submit' button in home page this interface will be used to check marks by the student"""
    root.geometry("750x400")
    students_page = ctk.CTkFrame(height=750,width=750)
    global name_var_student, admission_var_student
    name_var_student = ctk.StringVar()
    admission_var_student = ctk.IntVar()
    ctk.CTkLabel(students_page,
            text="Name of student",
            text_font=FONT
            ).place(x=20,y=20)
            
    ctk.CTkLabel(students_page,
            text="Admission Number",
            text_font=FONT
            ).place(x=20,y=120)
            
    name_entry = ctk.CTkEntry(students_page,
                            textvariable=name_var_student,
                            text_font=FONT,
                            width=200
                            )

    admission_entry = ctk.CTkEntry(students_page,
                                textvariable=admission_var_student,
                                text_font=FONT,
                                width=200
                                )

    name_entry.place(x=430,y=20)
    admission_entry.place(x=430,y=120)

    ctk.CTkButton(students_page,
                text="Submit",
                command=checkmarks,
                border_width = 3,
                border_color= HOVER_COLOUR,
                hover_color= HOVER_COLOUR,
                fg_color=FG_COLOUR,
                text_font=FONT
                ).place(x=100,y=220)
    students_page.pack(fill="both",padx=20,pady=20)


def checkmarks():
    """This fuction is in student's interface and this function will be executed when the user press 'submit' button in student's interface"""
    try:
        global admssion_num_student, name_student
        name_student = name_var_student.get()
        validate_name(name_student)
        admssion_num_student = admission_var_student.get()
    except _tkinter.TclError:
        tmsg.showerror("Invalid Details",
                        "You have entered invalid details please try again")
    cursor.execute(f"select * from marks_student where admission_num = {admssion_num_student} and name = '{name_student}'")

    data = [i for i in cursor]
    try:
        global marks
        marks = data[0][2]
    except IndexError:
        tmsg.showerror("","Teacher did not issue your marks please try after sometime")
    else:
        tmsg.showinfo(
                "Marks",
                f"Congrats You have got {marks} marks"
            )


def validate_name(formal_name: str):
    """This function is used to validate a name by checking whether all the characters are alphabets, space , dot"""
    formal_name1 = formal_name.replace(".", "")
    formal_name2 = formal_name1.replace(" ", "")
    if formal_name2.isalpha() == False:
        raise _tkinter.TclError



root.mainloop()
