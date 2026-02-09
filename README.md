Pinterest Pin Scheduler
=======================
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-00BFFF?style=flat&logo=python&logoColor=white)
![Chrome](https://img.shields.io/badge/Google_Chrome-4285F4?style=flat&logo=google-chrome&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=flat&logo=json&logoColor=white)
![Pinterest](https://img.shields.io/badge/Pinterest-%23E60023.svg?logo=Pinterest&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)


This project is a powerful tool designed to help users manually schedule pins on Pinterest using Selenium and Python. By automating the pin creation process, this application allows for efficient management of Pinterest boards, making it easier to engage with audiences and promote content effectively.



Prerequisites
-------------

Before you begin, ensure you have the following installed on your machine:

*   **Python 3.x:** The programming language used to develop this application.
*   **Google Chrome:** The web browser used for automation.
*   **ChromeDriver:** Automatically handled by `webdriver-manager`, this is required for Selenium to control Chrome.



Installation
------------

Follow these steps to set up the project on your local machine:

1.  **Clone the repository:**
    
        git clone git@github.com:anvay69/pinterest-pin-scheduler.git
        cd pinterest-pin-scheduler
    
2.  **Install required packages:**
    
        pip install -r requirements.txt
    
    This command installs all necessary libraries specified in the `requirements.txt` file.
    
3.  **Configure your settings:**
    
    Open the `settings.json` file and modify the following fields:
    
    *   `"user-data-dir"`: Path to your Chrome user data directory, where your profiles are stored.
    *   `"profile-dir"`: Name of the specific Chrome profile to use.
    *   To use the CLI, update the `"config"` section with your desired board name, link, number of pins, location, start date, and start time.



Usage
-----

Once everything is set up, you can run the application:

1.  **Run the CLI version:**
    
        python cli.py
    
    You will be prompted to either set a new profile or create pins. Follow the prompts to input your profile information and select the images folder.
    
2.  **Using the GUI version:**
    
        python pin_scheduler.py
    
    Click on "Launch" to start the profile. Fill in the required fields such as board, link, location, date, and time. Select the folder containing the images for your pins. Click "Begin" to start scheduling your pins.
    


Features
--------

*   **Profile Management:** Easily set and switch between different Chrome profiles to manage multiple Pinterest accounts without hassle.
*   **Image Uploading:** Select multiple images from your local directory to create engaging pins quickly.
*   **Scheduling Pins:** Specify the date and time for each pin to be published, allowing for strategic posting.
*   **User-Friendly Interface:** A graphical user interface built with CustomTkinter makes it easy to navigate and use the application.
*   **Error Handling:** Built-in error handling ensures smooth operation and provides feedback for any issues encountered during the pin creation process.



File Descriptions
-----------------

### 1. cli.py
This file provides a command-line interface for users to schedule pins. It uses `settings.json`'s `"config"` key to get variables like *board name*, *link*, *number of images*, *start date*, *start time*, *location*.

### 2. pin_scheduler.py
This file implements the GUI using CustomTkinter, allowing users to:
- Launch the application and manage widget layout.
- Input details for the Pinterest board, link, location, date, time, and number of pins.
- Validate inputs and handle image folder selection.

### 3. utility.py
This file contains utility functions for:
- Managing user profiles and ChromeDriver settings.
- Creating pins, including board selection and image uploads.
- Handling date formats and scheduling.
- Managing error handling for various operations.

### 4. settings.json
This configuration file stores:
- Paths for the Chrome user data and profile.
- Board name, link, number of pins, location, date, and time.
- CSS selectors for Pinterest interactions.
- Date formats for scheduling (US and UK).



Date Format Handling
--------------------

The application supports multiple date formats based on the user's specified location. The following formats are used:

*   **US Format:** `%m/%d/%Y` (e.g., 06/19/2024)
*   **UK Format:** `%d/%m/%Y` (e.g., 19/06/2024)

When the user selects a location, the application automatically adjusts the date input format accordingly. This ensures that the dates entered by the user are correctly interpreted by Pinterest.



Wait Times and Implicit Waits
-----------------------------

The application uses implicit waits to ensure that elements are fully loaded before interactions are attempted. This helps prevent errors related to elements not being available for interaction. The following wait times are implemented:

*   Implicit wait of 10 seconds is set for the WebDriver to allow time for page elements to load before executing further actions.
*   Specific waits are used in the `create_pins` function to ensure that elements such as buttons and input fields are present before attempting to interact with them.



Contributing
------------

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. Any contributions, whether they be bug fixes, new features, or improvements to the documentation, are welcome!



Contact
-------

If you have any questions or feedback, please reach out to me at [anvayjain64@gmail.com](mailto:anvayjain64@gmail.com).
