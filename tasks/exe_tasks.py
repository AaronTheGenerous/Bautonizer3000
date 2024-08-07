"""
### exe_tasks.py

Script for automatic processing of promotional banner images on Webshop

©Aaron Hafner
GraphicArt AG
31.07.2024

Overview
This script is designed to automate tasks related to managing promotional banner images on the GraphicArt AG webshop. It leverages Selenium WebDriver for browser automation, allowing users to perform tasks like logging in, inserting images into text editors, and processing or removing article images programmatically.

Functions
wait_for_element(driver, timeout, condition)
Waits for an element to be present or a condition to be met within a given timeout period.

Parameters:
driver: The WebDriver instance.
timeout: Maximum time to wait for the condition to be met (in seconds).
condition: The expected condition to wait for, can be a callable or an expected condition object.
Returns: The element that meets the condition.
login(driver, email, password)
Performs a login action by entering the provided email and password.

Parameters:
driver: The WebDriver instance used to interact with the browser.
email: The email address used for login.
password: The password used for login.
Returns: None.
remove_image_from_editor(driver, editor_id)
Removes all images from the editor with the given ID.

Parameters:
driver: The WebDriver instance used to interact with the browser.
editor_id: The ID of the editor element.
Returns: None.
insert_image_text_editor(driver, img_url, img_width, img_height, link_url, link_checkbox)
Inserts an image into a text editor with the specified parameters.

Parameters:
driver: The Selenium WebDriver instance.
img_url: The URL of the image to be inserted.
img_width: The width of the image.
img_height: The height of the image.
link_url: The URL of the link associated with the image (optional).
link_checkbox: A boolean indicating whether a link should be added to the image (optional).
Returns: None.
process_articles(driver, task_data)
Processes a list of articles by performing operations like inserting images.

Parameters:
driver: WebDriver object representing the web browser used for automated testing.
task_data: Dictionary containing the data needed to process the articles.
Returns: None.
remove_articles_images(driver, task_data)
Removes article images from the website based on the provided task data.

Parameters:
driver: WebDriver object representing the browser.
task_data: Dictionary containing task-specific data.
Returns: None.
execute_task(task_filename)
Executes a task based on the information provided in the task file.

Parameters:
task_filename: The filename or path of the task file containing the task information.
Returns: None.
Main Execution
main(task_filename)
Main entry point for executing a task.

Parameters:
task_filename: The filename of the task file to be executed.
Returns: None.
Usage
To execute the script, run the following command:

bash
Copy code
python execute_task.py <task_filename>
Replace <task_filename> with the path to your task file.

Example Task File
The task file should be a JSON file containing the necessary information to perform the tasks, such as:

json
Copy code
{
  "task_type": "process_articles",
  "data": {
    "article_numbers": "123,456,789",
    "img1_url": "https://example.com/image1.jpg",
    "img2_url": "https://example.com/image2.jpg",
    "width": "100",
    "height": "100",
    "link_checkbox": true,
    "link_input_de": "https://example.com/de",
    "link_input_fr": "https://example.com/fr",
    "marke": "Some Brand",
    "kategorie": "Some Category"
  },
  "follow_up": false,
  "subsequent_tasks": []
}
This script is designed to simplify and automate repetitive tasks, ensuring efficiency and consistency in handling promotional content on the webshop.
"""

import json
import os
import sys
import traceback

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait


def wait_for_element(driver, timeout, condition):
    """
    Waits for an element to be present or condition to be True within a given timeout.

    :param driver: The WebDriver instance.
    :param timeout: The maximum amount of time (in seconds) to wait for the condition to be met.
    :param condition: The expected condition to wait for. This can be a callable condition or an expected condition object.
    :return: The element that meets the condition.
    """
    return WebDriverWait(driver, timeout).until(condition)


def login(driver, email, password):
    """
    :param driver: The WebDriver instance used to interact with the browser.
    :param email: The email address used for login.
    :param password: The password used for login.
    :return: None

    This method performs a login action by first clicking on the "Anmeldung" button, then entering the provided email address and password into the corresponding fields, and finally clicking on the "Anmelden" button to submit the login.

    Example usage:
        login(driver, 'user@example.com', 'password')
    """
    kundenlogin_button = wait_for_element(driver, 30, ec.presence_of_element_located((By.CSS_SELECTOR, 'a.dropdown-toggle[title="Anmeldung"]')))
    kundenlogin_button.click()

    email_field = wait_for_element(driver, 30, ec.presence_of_element_located((By.ID, 'box-login-dropdown-login-username')))
    email_field.send_keys(email)

    password_field = wait_for_element(driver, 30, ec.presence_of_element_located((By.ID, 'box-login-dropdown-login-password')))
    password_field.send_keys(password)

    login_button = wait_for_element(driver, 30, ec.presence_of_element_located((By.XPATH, '//input[@value="Anmelden"]')))
    login_button.click()


def remove_image_from_editor(driver, editor_id):
    """
    Remove all images from the editor with the given ID.

    :param driver: The WebDriver instance used to interact with the browser.
    :type driver: selenium.webdriver.WebDriver
    :param editor_id: The ID of the editor element.
    :type editor_id: str
    :return: None
    :rtype: None
    """
    iframe = wait_for_element(driver, 10, ec.presence_of_element_located((By.CSS_SELECTOR, f'#{editor_id} iframe')))
    driver.switch_to.frame(iframe)
    script = '''
    var ul = document.querySelector('body ul');
    if (ul) {
        var lis = ul.children;
        for (var i = 0; i < lis.length; i++) {
            var img = lis[i].querySelector('img');
            if (img) {
                img.remove();
            }
        }
    }
    '''
    driver.execute_script(script)
    driver.switch_to.default_content()


def insert_image_text_editor(driver, img_url, img_width, img_height, link_url, link_checkbox):
    """
    :param driver: The Selenium WebDriver instance.
    :param img_url: The URL of the image to be inserted.
    :param img_width: The width of the image.
    :param img_height: The height of the image.
    :param link_url: The URL of the link associated with the image (optional).
    :param link_checkbox: A boolean value indicating whether a link should be added to the image (optional).
    :return: None

    This method inserts an image into a text editor using the given parameters. It locates the image button in the editor, clicks on it, and enters the image URL, width, and height. If the image URL contains "DE", it selects the "Rechts" alignment option. If the link_checkbox parameter is True and a link URL is provided, it selects the link tab, enters the link URL, and navigates down to the "OK" button. After clicking the "OK" button, it waits for the image properties popup to close. If the popup does not close within 10 seconds, it attempts to click the "OK" button again.
    """
    def fill_input(xpath, value):
        """
        :param xpath: The XPath expression used to locate the input field.
        :param value: The value to be filled into the input field.
        :return: None

        This method locates an input field using the provided XPath expression, clears any existing value, and fills in the provided value.
        """
        input_field = wait_for_element(driver, 10, ec.visibility_of_element_located((By.XPATH, xpath)))
        input_field.clear()
        input_field.send_keys(value)

    xpaths = {
        "img_button": '//*[@id="cke_135"]' if "DE" in img_url else '//*[@id="cke_357"]',
        "url_input": '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_549_label"]' if "DE" in img_url else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_688_label"]',
        "width_input": '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_559_label"]' if "DE" in img_url else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_698_label"]',
        "height_input": '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_562_label"]' if "DE" in img_url else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_701_label"]',
        "ok_button": '//a[contains(@class, "cke_dialog_ui_button") and @title="OK"]',
        "link_tab": '//*[@id="cke_Link_595"]' if "DE" in img_url else '//*[@id="cke_Link_734"]',
        "link_url_input": 'input.cke_dialog_ui_input_text[type="text"][aria-labelledby="cke_587_label"]' if "DE" in img_url else 'input.cke_dialog_ui_input_text[type="text"][aria-labelledby="cke_726_label"]',
    }

    img_button = wait_for_element(driver, 10, ec.element_to_be_clickable((By.XPATH, xpaths["img_button"])))
    driver.execute_script("arguments[0].click();", img_button)

    fill_input(xpaths["url_input"], img_url)
    fill_input(xpaths["width_input"], img_width)
    fill_input(xpaths["height_input"], img_height)

    if "DE" in img_url:
        alignement_loc = wait_for_element(driver, 10, ec.visibility_of_element_located((By.XPATH, xpaths["ausrichtung_input"])))
        Select(alignement_loc).select_by_visible_text("Rechts")
    else:
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * 6 + Keys.ARROW_DOWN * 2).perform()

    if link_checkbox and link_url:
        link_tab = wait_for_element(driver, 10, ec.element_to_be_clickable((By.XPATH, xpaths["link_tab"])))
        driver.execute_script("arguments[0].click();", link_tab)
        fill_input(xpaths["link_url_input"], link_url)
        ActionChains(driver).send_keys(Keys.TAB * 2 + Keys.ARROW_DOWN).perform()

    ok_button = wait_for_element(driver, 10, ec.visibility_of_element_located((By.XPATH, xpaths["ok_button"])))
    driver.execute_script("arguments[0].click();", ok_button)

    try:
        wait_for_element(driver, 10, ec.invisibility_of_element_located((By.XPATH, '//div[contains(@class, "cke_dialog_title") and text()="Bildeigenschaften"]')))
    except TimeoutException:
        print("Popup did not close within 10 seconds. Attempting to click the OK button again.")
        ok_button = wait_for_element(driver, 10, ec.element_to_be_clickable((By.XPATH, xpaths["ok_button"])))
        driver.execute_script("arguments[0].click();", ok_button)
        wait_for_element(driver, 10, ec.invisibility_of_element_located((By.XPATH, xpaths["popup_title"])))


def process_articles(driver, task_data):
    """
    :param driver: WebDriver object, represents the web browser used for automated testing.
    :param task_data: dict, contains the data needed to process the articles.
    :return: None

    This method processes a list of articles by performing the following steps:
    1. Extracts the article numbers from the task_data.
    2. Gets the image URLs, image width and height, checkbox status, and input for link in both German and French languages from the task_data.
    3. Calls the login function with the provided driver and login credentials.
    4. Opens the specified URL.
    5. Defines a helper function navigate_to_element which navigates to a specific element by text.
    6. If the specified "marke" is not 'Kamerasysteme + Objektive', calls navigate_to_element with the provided "marke".
    7. If the specified "kategorie" is not 'Kategorie wählen', calls navigate_to_element with the provided "kategorie" and waits for the category table to be present.
    8. Waits for the category table to be present.
    9. Iterates through the article numbers.
       a. If the article number is empty, skips to the next iteration.
       b. Tries to find the rows containing article information.
       c. Iterates through the rows and finds the row with the matching article number.
       d. Scrolls to the product link and clicks on it.
       e. Calls the insert_image_text_editor function with the provided image URL, image width, image height, link input, and checkbox status for both German and French languages.
       f. Finds and clicks the submit button.
       g. Waits for the category table to be present.
       h. Prints the processed article number.
       i. If an exception occurs, prints the exception message.

    Note: The method assumes the presence of the functions login, wait_for_element, insert_image_text_editor, and traceback.print_exc().

    Example Usage:
        driver = WebDriver()
        task_data = {
            "article_numbers": "123,456,789",
            "img1_url": "https://example.com/image1.jpg",
            "img2_url": "https://example.com/image2.jpg",
            "width": "100",
            "height": "100",
            "link_checkbox": True,
            "link_input_de": "https://example.com/de",
            "link_input_fr": "https://example.com/fr",
            "marke": "Some Brand",
            "kategorie": "Some Category"
        }
        process_articles(driver, task_data)
    """
    article_numbers = [num.strip() for num in task_data["article_numbers"].split(',')]
    img1_url = task_data["img1_url"]
    img2_url = task_data["img2_url"]
    img_width = task_data["width"]
    img_height = task_data["height"]
    link_checkbox = task_data["link_checkbox"]
    link_input_de = task_data["link_input_de"]
    link_input_fr = task_data["link_input_fr"]

    login(driver, 'feigelluck@gmail.com', 'Graphicart#1')
    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")

    def navigate_to_element(text):
        """
        :navigate_to_element:

        :param text: The text of the element to navigate to.
        :return: None
        """
        element = wait_for_element(driver, 20, ec.presence_of_element_located((By.XPATH, f"//b/a[text()='{text}']")))
        driver.execute_script("arguments[0].click();", element)

    if task_data["marke"] != 'Kamerasysteme + Objektive':
        navigate_to_element(task_data["marke"])

    if task_data["kategorie"] != 'Kategorie wählen':
        navigate_to_element(task_data["kategorie"])
        wait_for_element(driver, 10, ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    wait_for_element(driver, 20, ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            rows = wait_for_element(driver, 10, ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.dataTableRow')))
            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)')
                if number_element.text.strip() == article_number:
                    product_link_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3) a')
                    driver.execute_script("arguments[0].scrollIntoView(true);", product_link_element)
                    driver.execute_script("arguments[0].click();", product_link_element)
                    break

            insert_image_text_editor(driver, img1_url, img_width, img_height, link_input_de, link_checkbox)
            insert_image_text_editor(driver, img2_url, img_width, img_height, link_input_fr, link_checkbox)

            submit_button = wait_for_element(driver, 10, ec.element_to_be_clickable((By.XPATH, '//button[@title="Speichern" and @type="submit"]')))
            driver.execute_script("arguments[0].click();", submit_button)
            wait_for_element(driver, 10, ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

            print(f"Processed article: {article_number}")

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def remove_articles_images(driver, task_data):
    """
    :param driver: WebDriver object representing the browser
    :param task_data: Dictionary containing task-specific data
    :return: None

    This method removes articles images from a website. It takes a WebDriver object and task-specific data as parameters. The method iterates through a list of article numbers provided in the task_data dictionary and performs the following steps for each article number:

    1. Navigates to the admin categories page of the website.
    2. If the "marke" value in the task_data dictionary is not equal to 'Kamerasysteme + Objektive', it navigates to the element corresponding to the "marke" value.
    3. If the "kategorie" value in the task_data dictionary is not equal to 'Kategorie wählen', it navigates to the element corresponding to the "kategorie" value and waits for a compatibility table to load.
    4. Waits for a compatibility table to load.
    5. Searches for the article number in the table rows and clicks on the corresponding product link.
    6. Removes images from two editors named "cke_products_short_description_2" and "cke_products_short_description_5".
    7. Clicks the submit button to save the changes.
    8. Waits for a compatibility table to load again.

    If an exception occurs during the process, it prints the exception message along with the corresponding article number.

    Finally, it quits the driver.
    """
    article_numbers = [num.strip() for num in task_data["article_numbers"].split(',')]

    login(driver, 'feigelluck@gmail.com', 'Graphicart#1')
    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")

    def navigate_to_element(text):
        """
        Navigates to the element with the given text.

        :param text: The text of the element to navigate to.
        :return: None
        """
        element = wait_for_element(driver, 10, ec.presence_of_element_located((By.XPATH, f"//a[text()='{text}']")))
        driver.execute_script("arguments[0].click();", element)

    if task_data["marke"] != 'Kamerasysteme + Objektive':
        navigate_to_element(task_data["marke"])

    if task_data["kategorie"] != 'Kategorie wählen':
        navigate_to_element(task_data["kategorie"])
        wait_for_element(driver, 10, ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    wait_for_element(driver, 10, ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            rows = wait_for_element(driver, 10, ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.dataTableRow')))
            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)')
                if number_element.text.strip() == article_number:
                    product_link_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3) a')
                    driver.execute_script("arguments[0].scrollIntoView(true);", product_link_element)
                    driver.execute_script("arguments[0].click();", product_link_element)
                    break

            remove_image_from_editor(driver, "cke_products_short_description_2")
            remove_image_from_editor(driver, "cke_products_short_description_5")

            submit_button = wait_for_element(driver, 10, ec.element_to_be_clickable((By.XPATH, '//button[@title="Speichern" and @type="submit"]')))
            driver.execute_script("arguments[0].click();", submit_button)
            wait_for_element(driver, 10, ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def execute_task(task_filename):
    """
    :param task_filename: The filename or path of the task file containing the information about the task to be executed.
    :return: None

    This method executes a task based on the information provided in the task file. It loads the task file, initializes the web driver, and performs the specified task. If there is a follow-up task specified in the task file, it recursively calls the `execute_task` method to execute the follow-up task.

    Example usage:
    ```
    execute_task("task.json")
    ```
    """
    if not os.path.exists(task_filename):
        print(f"Task file not found: {task_filename}")
        return

    with open(task_filename, 'r') as file:
        task = json.load(file)

    base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(base_path, 'chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.path.join(base_path, 'chrome', 'win64-118.0.5993.70', 'chrome-win64', 'chrome.exe')

    service = Service(chromedriver_path)

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.graphicart.ch/shop/de/")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    try:
        if task["task_type"] == "process_articles":
            process_articles(driver, task["data"])
        elif task["task_type"] == "remove_articles_images":
            remove_articles_images(driver, task["data"])
        else:
            raise ValueError(f'Invalid task_type: {task["task_type"]}')
    finally:
        driver.quit()

    if task.get("follow_up", False):
        for next_task in task.get("subsequent_tasks", []):
            execute_task(next_task)


def main(task_filename):
    """
    :param task_filename: The filename of the task file to be executed.
    :return: None

    This is the main entry point for executing a task. It takes a task filename as input and calls execute_task method to perform the task.
    """
    execute_task(task_filename)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python execute_task.py <task_filename>")
    else:
        main(sys.argv[1])
