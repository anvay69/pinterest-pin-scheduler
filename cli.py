from utility import *
# import sys
import time
from tkinter.filedialog import askdirectory


def main():
    '''
    MAIN METHOD
    '''

    # start, add cookies and get to pin builder
    # start()
    # a little cute prompt :)
    print("You wanna? \n1.) Set New Profile \n2.) Create Pins")


    # set profile or start creating pins
    while True:
        try:
            choice = int(input())
            if choice == 1:
                # switch accounts and restart
                user_directory = input("user-data-dir: ")
                profile_directory = input("profile-directory: ")
                set_profile(
                    user_directory=user_directory,
                    profile_directory=profile_directory
                )
            
            elif choice == 2:
                # starting and selecting the account
                start()
                input("Did you select your account? ")

                with open("settings.json", "r") as file:
                    settings = json.load(file)
                    settings = settings["config"]

                # inputs for creating pins
                board = settings['board']
                link = settings['link']
                # images_folder = input("Folder(case sensitive): ") # not necessary yet
                print("select images folder in the window pls")
                images_folder = askdirectory()
                while images_folder == "":
                    print("SELECT IT BITCH OR I'LL KILL YOUR ENTIRE FAMILY")
                    images_folder = askdirectory()

                num = settings['num']
                location = settings["location"]
                start_date = settings['start_date']
                start_time = settings['start_time'].upper()

                # start creating pins
                driver = create_pins(
                    board=board, link=link, images_folder=images_folder,
                    num=num, location=location, start_date=start_date, start_time=start_time
                )
                
                # asking user to publish the pins after everything is done :)
                n = input("The bot won't publish.\
                        \nDone publishing? :)\
                        \nQuit time(default 5 sec): ")

                # driver quits 'n' seconds after user's prompt
                try:
                    n = int(n)
                except:
                    n = 5

                # final countdown :)
                for i in range(n, 0, -1):
                    print(f"\rQuitting in {i} seconds...", end="")
                    time.sleep(1)
                print("\rQuitting...")
                
                # task complete 😎
                driver.quit()

            else:
                # What input 🤨
                raise WhatInputException("What Input?")
            break
        except WhatInputException:
            print(f"You picked {choice}. Try Again :(")




# starting here
if __name__ == "__main__":
    main()