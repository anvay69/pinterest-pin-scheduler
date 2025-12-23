import customtkinter as ctk
from tkinter.messagebox import showerror, showinfo, askyesno
from tkinter.filedialog import askdirectory

from PIL import Image, ImageTk
import os

import utility



widgets = dict()
board_options = None
location_options = None


def test():
    print(widgets["window"])



def launch_profile():
    # starting the driver
    utility.start()
    widgets["cat"].configure(text="Starting the profile")
    widgets["cat"].update()
    widgets["window"].update()

    # getting driver and selectors
    driver = utility.driver
    selectors = utility.selectors
    # confirming the window setting
    showinfo("Confirmation", "Did you set the window? ")
    print("Window Set Confirmed")

    board_button = driver.find_element("css selector", selectors["board_select"])
    board_button.click()
    utility.WebDriverWait(driver=driver, timeout=10).until(
        utility.EC.presence_of_element_located(("css selector", selectors["time_common"]))
    )  
    boards = driver.find_elements("css selector", selectors["time_common"])

    location_options = utility.date_locations.keys()
    board_options = [board.get_attribute("innerHTML").replace("amp;", "") for board in boards]
    board_button.click()

    widgets["date_location"].configure(values=location_options)
    widgets["board_dropdown"].configure(values=board_options)

    widgets["startup_frame"].pack_forget()
    widgets["main_frame"].pack(side="top")



def select_folder():
    folder_name = askdirectory()
    if folder_name != "":
        widgets["folder_entry"].delete(0, "end")
        widgets["folder_entry"].insert(0, folder_name)



def go_to_builder():
    if utility.driver == None:
        showerror(
            "Unexpected Error",
            "Cannot go to builder, the driver is not active yet."
        )
    
    utility.driver.get("https://in.pinterest.com/pin-builder")
    driver = utility.driver
    selectors = utility.selectors
    # confirming the window setting
    showinfo("Confirmation", "Did you set the window? ")
    print("Window Set Confirmed")

    board_button = driver.find_element("css selector", selectors["board_select"])
    board_button.click()
    utility.WebDriverWait(driver=driver, timeout=10).until(
        utility.EC.presence_of_element_located(("css selector", selectors["time_common"]))
    )  
    boards = driver.find_elements("css selector", selectors["time_common"])

    location_options = utility.date_locations.keys()
    board_options = [board.get_attribute("innerHTML").replace("amp;", "") for board in boards]
    board_button.click()

    widgets["date_location"].configure(values=location_options)
    widgets["board_dropdown"].configure(values=board_options)

    widgets["startup_frame"].pack_forget()
    widgets["main_frame"].pack(side="top")



def quit_driver():
    if utility.driver == None:
        return
    
    confirm = askyesno(
        "Confirm Process",
        "Are you sure you want to force quit the browser?"
    )
    if confirm:
        utility.driver.quit()



def update_location(value):
    modifier = utility.date_locations[value]
    placeholder = modifier.replace("%d", "DD").replace("%m", "MM").replace("%Y", "YYYY")
    widgets["start_date"].configure(placeholder_text=placeholder)



def date_not_valid(date_string, location):
    # TODO
    return False



def time_not_valid(time_string, date_string, location):
    # TODO
    return False



def begin_scheduling():
    board = widgets["board_dropdown"].get().strip()
    if board == "None":
        showerror(
            "Input Error",
            "No board selected"
        )
        return
    
    link = widgets["link"].get().strip()
    if not link:
        showerror(
            "Input Error",
            "Link Field Empty"
        )
        return
    
    location = widgets["date_location"].get().strip()
    if location == "None":
        showerror(
            "Input Error",
            "No location Selected"
        )
        return
    
    start_date = widgets["start_date"].get().strip()
    if start_date == "":
        showerror(
            "Input Error",
            "Start Date Field Empty"
        )
        return
    
    if date_not_valid(start_date, location):
        showerror(
            "Invalid Date",
            "Format of Date is Invalid or the Date Itself is Invalid."
        )
        return
    
    start_time = widgets["start_time"].get().strip()
    if start_time == "":
        showerror(
            "Input Error",
            "Time Field Left Blank"
        )
        return

    if time_not_valid(start_time, start_date, location):
        showerror(
            "Invalid Time",
            "Format of Time or the Time itself is Invalid."
        )
        return
    
    num = widgets["num"].get().strip()
    try:
        num = int(num)
    except ValueError:
        showerror(
            "Invalid Input",
            "Number of pins must be a base 10 natural number."
        )
        return
    
    images_folder = widgets["folder_entry"].get().strip()
    if images_folder == "":
        showerror(
            "Input Error",
            "Folder Field left blank."
        )
        return
    
    if not os.path.exists(images_folder):
        showerror(
            "Invalid Input",
            f"Given Folder \"{images_folder}\" does not exists"
        )
        return
    
    try:
        widgets["main_frame"].pack_forget()
        widgets["startup_frame"].pack()
        utility.create_pins(
            board=board, link=link,
            images_folder=images_folder,
            num=num, location=location,
            start_date=start_date, start_time=start_time
        )
    except AssertionError as e:
        showerror(
            "Fatal Expected Error",
            f"Something Went Wrong.\n {str(e)}"
        )
    except Exception as e:
        showerror(
            "Fatal Unexpected Error",
            f"Something Went Wrong.\n {str(e)}"
        )
    
    widgets["startup_frame"].pack_forget()
    widgets["main_frame"].pack()
    


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

window = ctk.CTk(fg_color="white")
widgets["window"] = window
window.geometry("480x250")
window.resizable(False, False)
window.title("Auto Pin Scheduler (for Pinterest)")

window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open("./images/logo.png")))

# upper frame
title_frame = ctk.CTkFrame(
    window, width=580, height=70,
    corner_radius= 0, fg_color="#CDB4DB", border_width=0
)
title_frame.pack_propagate(False)
title_frame.pack(side="top")

# icon label
icon_img = Image.open("./images/pinterest.png")
icon_ctk = ctk.CTkImage(
    light_image=icon_img, dark_image=icon_img,
    size=(60, 60)
)
widgets["icon"] = ctk.CTkLabel(title_frame, text="", image=icon_ctk)
widgets["icon"].pack(side="left")

# title label
title_img = Image.open("images\pin_scheduler - Copy.png")
title_ctk = ctk.CTkImage(
    light_image=title_img, dark_image=title_img,
    size=(250, 240*0.2)
)
title = ctk.CTkLabel(title_frame, text="", 
                     image=title_ctk)
title.pack(side="left")

# sub title frame for the two buttons
title_sub_frame = ctk.CTkFrame(title_frame, fg_color="#CDB4DB")
title_sub_frame.pack(side="right", padx=10)

# launch button
launch_img = Image.open("./images/launch.png")
launch_ctk = ctk.CTkImage(
    light_image=launch_img, dark_image=launch_img, 
    size=(20, 20)
)
widgets["launch"] = ctk.CTkButton(
    title_sub_frame, text="Launch", image=launch_ctk, compound="left",
    width=70, text_color="#000000", fg_color="#CDB4DB",
    hover_color="#FFC8DD", font=('Arial', 13, 'bold'), command=launch_profile
)
widgets["launch"].pack(side="top")

# profile button
profile_img = Image.open("./images/profile.png")
profile_ctk = ctk.CTkImage(
    light_image=profile_img, dark_image=profile_img,
    size=(20, 20)
)
widgets["set_profile"] = ctk.CTkButton(
    title_sub_frame, image=profile_ctk, text="Set Profile", compound="left",
    width=70, text_color="#000000", fg_color="#CDB4DB", hover_color="#FFC8DD", font=('Arial', 13, 'bold')
)
widgets["set_profile"].pack(side="top")


# startup main frame
startup_main_frame = ctk.CTkFrame(
    window, width=450,
    border_width=0, corner_radius=0,
    fg_color="white", height=180
)
startup_main_frame.pack(side="top")
widgets["startup_frame"] = startup_main_frame

cat_img = Image.open("./images/cat.jpeg")
cat_ctk = ctk.CTkImage(light_image=cat_img, dark_image=cat_img, size=(150, 150))

cat = ctk.CTkLabel(
    startup_main_frame,
    text="Please Launch A Profile First", image=cat_ctk,
    compound="top", font=('Arial', 18, 'bold'), text_color="purple"
)
cat.pack()
widgets["cat"] = cat


# main frame
main_frame = ctk.CTkFrame(
    window, width=450,
    border_width=0, corner_radius=0,
    fg_color="white"
)
widgets["main_frame"] = main_frame


# row one
row_one = ctk.CTkFrame(main_frame, fg_color="white")
row_one.pack(side="top", pady=10)

# board dropdown frame
board_frame = ctk.CTkFrame(
    row_one, fg_color="white", border_width=4, 
    border_color='#bde0fe'
)
board_frame.pack(side="left")

board_label = ctk.CTkLabel(
    board_frame, text=" Select Board: ", text_color="black",
    font=('Arial', 13, 'bold'), fg_color="#bde0fe", corner_radius=0
)
board_label.pack(side="left", pady=3)

widgets["board_dropdown"] = ctk.CTkOptionMenu(
    board_frame, dropdown_hover_color="#ffc8dd",
    button_color="#bde0fe", button_hover_color="#ffc8dd",
    text_color="black", fg_color="white",
    corner_radius=0, values=[""], 
    variable=ctk.StringVar(value="None")
)
widgets["board_dropdown"].pack(side="left", pady=3)


# link input frame
link_frame = ctk.CTkFrame(
    row_one, fg_color="white", border_width=4, 
    border_color='#bde0fe'
)
link_frame.pack(side="left", padx=10)

# link label
link_label = ctk.CTkLabel(
    link_frame, text=" Link: ", text_color="black",
    font=('Arial', 13, 'bold'), fg_color="#bde0fe", corner_radius=0
)
link_label.pack(side="left", pady=3)

# input
widgets["link"] = ctk.CTkEntry(
    link_frame, fg_color="#f9d7f1",
    corner_radius=0, border_width=0
)
widgets["link"].pack(side="left", pady=3)


# row 2 : date format, start date, start time
row_two = ctk.CTkFrame(main_frame, fg_color="white")
row_two.pack(side="top")

# location frame
location_frame = ctk.CTkFrame(
    row_two, fg_color="white",
    border_width=4, border_color="#bde0fe"
)
location_frame.pack(side="left")

# location label
location_label = ctk.CTkLabel(
    location_frame, text="  Location:  ", fg_color="#bde0fe",
    font=('Arial', 13, 'bold'), text_color="black", corner_radius=0
)
location_label.pack(side="left", pady=3)

# location input
widgets["date_location"] = ctk.CTkOptionMenu(
    location_frame, dropdown_hover_color="#ffc8dd",
    button_color="#bde0fe", button_hover_color="#ffc8dd",
    text_color="black", fg_color="white",
    corner_radius=0, values=[""], width=60,
    variable=ctk.StringVar(value="None"),
    command=update_location
)
widgets["date_location"].pack(side="left", pady=3)


# date frame
date_frame = ctk.CTkFrame(
    row_two, fg_color="white",
    border_width=4, border_color="#bde0fe"
)
date_frame.pack(side="left", padx=10)

# date label
date_label = ctk.CTkLabel(
    date_frame, text="  Start Date:  ", fg_color="#bde0fe",
    font=('Arial', 13, 'bold'), text_color="black", corner_radius=0
)
date_label.pack(side="left", pady=3)

# date input
widgets["start_date"] = ctk.CTkEntry(
    date_frame, fg_color="#f9d7f1",
    corner_radius=0, border_width=0, width=70
)
widgets["start_date"].pack(side="left", pady=3)


# time frame
time_frame = ctk.CTkFrame(
    row_two, fg_color="white",
    border_width=4, border_color="#bde0fe"
)
time_frame.pack(side="left")

# time label
time_label = ctk.CTkLabel(
    time_frame, text="  Start Time:  ", fg_color="#bde0fe",
    font=('Arial', 13, 'bold'), text_color="black", corner_radius=0
)
time_label.pack(side="left", pady=3)

# time input
widgets["start_time"] = ctk.CTkEntry(
    time_frame, fg_color="#f9d7f1",
    corner_radius=0, border_width=0, width=70,
    placeholder_text="HH:MM AM/PM"
)
widgets["start_time"].pack(side="left", pady=3)


# row 3
row_three = ctk.CTkFrame(main_frame, fg_color="white")
row_three.pack(side="top", pady=10)

# number frame
number_frame = ctk.CTkFrame(
    row_three, fg_color="white",
    border_width=4, border_color="#bde0fe"
)
number_frame.pack(side="left")

# number label
number_label = ctk.CTkLabel(
    number_frame, text="  No. Pins:  ", fg_color="#bde0fe",
    font=('Arial', 13, 'bold'), text_color="black", corner_radius=0
)
number_label.pack(side="left", pady=3)

# number input
widgets["num"] = ctk.CTkEntry(
    number_frame, fg_color="#f9d7f1",
    corner_radius=0, border_width=0, width=50
)
widgets["num"].pack(side="left", pady=3)


# folder button
widgets["folder"] = ctk.CTkButton(
    row_three, fg_color="transparent", text="Select Folder",
    font=('Arial', 14, 'bold'), text_color="black",
    border_width=3, border_color="#bde0fe", hover_color="#bde0fe",
    corner_radius=0, command=select_folder
)
widgets["folder"].pack(side="left", padx=10)


# folder label
widgets["folder_entry"] = ctk.CTkEntry(
    row_three, width=120, placeholder_text="folder path",
    text_color="black", border_width=0, bg_color="white",
    fg_color="#ffcefd"
)
widgets["folder_entry"].pack(side="left")


# row four: go to builder, quit, begin
row_four = ctk.CTkFrame(main_frame, fg_color="white")
row_four.pack(side="top")

# go to builder button
widgets["go_to_builder"] = ctk.CTkButton(
    row_four, fg_color="transparent", text="Go To Builder",
    font=('Arial', 14, 'bold'), text_color="black",
    border_width=3, border_color="#bde0fe", hover_color="#bde0fe",
    corner_radius=0, command=go_to_builder
)
widgets["go_to_builder"].pack(side="left")

# begin button
widgets["begin"] = ctk.CTkButton(
    row_four, fg_color="#ffc8dd", text="Begin",
    font=('Arial', 14, 'bold'), text_color="black",
    corner_radius=0, hover_color="#ffafcc", command=begin_scheduling
)
widgets["begin"].pack(side="left", padx=10)

# quit button
widgets["quit"] = ctk.CTkButton(
    row_four, fg_color="transparent", text="QUIT",
    font=('Arial', 14, 'bold'), text_color="black",
    border_width=3, border_color="#718697", hover_color="#718697",
    corner_radius=0, command=quit_driver
)
widgets["quit"].pack(side="left")


def run():
    window.mainloop()

if __name__ == "__main__":
    run()