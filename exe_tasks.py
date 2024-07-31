"""
execute_task.py
"""

import json
import os
import sys
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def login(driver, email, password):
    """
    :param driver: The WebDriver object used to interact with the browser.
    :param email: The email used for login.
    :param password: The password used for login.
    :return: None

    This method performs the login functionality on a web page. It takes the WebDriver object, email, and password as
    parameters. The method locates the login button, email field, password field, and login button elements on the
    page using various selectors. It then performs the following steps: 1. Clicks on the login button, which triggers
    the login form to appear. 2. Inputs the provided email into the email field. 3. Inputs the provided password into
    the password field. 4. Clicks on the login button to submit the form.

    Note: This method assumes that the login form elements are present on the page and can be located using the
    specified selectors. It also assumes that the login process is successful and does not handle any potential
    errors or validations.
    """
    kundenlogin_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.dropdown-toggle[title="Anmeldung"]'))
    )
    kundenlogin_button.click()

    email_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'box-login-dropdown-login-username'))
    )
    email_field.send_keys(email)

    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'box-login-dropdown-login-password'))
    )
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//input[@value="Anmelden"]'))
    )
    login_button.click()


def remove_image_from_editor(driver, editor_id):
    """
    Remove all images from the specified editor.

    :param driver: The WebDriver object.
    :param editor_id: The id of the editor.
    :return: None.
    """
    time.sleep(1)
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#{editor_id} iframe')))
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
    :param driver: The WebDriver instance.
    :param img_url: The URL of the image to be inserted.
    :param img_width: The width of the image in pixels.
    :param img_height: The height of the image in pixels.
    :param link_url: The URL to link the image to (optional).
    :param link_checkbox: A flag indicating whether to include a link for the image (optional).
    :return: None

    This method inserts an image into a text editor using the given WebDriver instance. The image is specified by its
    URL, width, and height. Optionally, a link URL can be provided to link the image to a webpage. If the
    link_checkbox flag is set to True, a link input field will be displayed.

    The method finds the appropriate XPath expressions based on the language (DE or not DE). It waits for certain
    elements to be clickable or visible before interacting with them.

    Note: The WebDriverWait class is used to wait for elements to be present or visible before interacting with them.
    """
    xpaths = {
        "img_button": '//*[@id="cke_135"]' if "DE" in img_url else '//*[@id="cke_357"]',
        "url_input": '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_549_label"]' if "DE" in img_url else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_688_label"]',
        "width_input": '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_559_label"]' if "DE" in img_url else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_698_label"]',
        "height_input": '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_562_label"]' if "DE" in img_url else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_701_label"]',
        "ausrichtung_input": '//div[contains(@class, "cke_dialog_ui_input_select") and @role="presentation"]//select['
                             'contains(@class, "cke_dialog_ui_input_select")]',
        "ok_button": '//a[contains(@class, "cke_dialog_ui_button") and @title="OK"]',
        "link_tab": '//*[@id="cke_Link_595"]' if "DE" in img_url else '//*[@id="cke_Link_734"]',
        "link_url_input": 'input.cke_dialog_ui_input_text[type="text"][aria-labelledby="cke_587_label"]' if "DE" in img_url else 'input.cke_dialog_ui_input_text[type="text"][aria-labelledby="cke_726_label"]',
        "zielseite_input": '//*[@id="cke_597_select"]' if "DE" in img_url else '//*[@id="cke_591_select"]',
        "zielseite_select": '//*[@id="cke_597_select"]/option[2]' if "DE" in img_url else '//*[@id="cke_591_select'
                                                                                          '"]/option[2]',
    }

    img_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths["img_button"])))
    driver.execute_script("arguments[0].click();", img_button)
    time.sleep(0.5)

    url_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpaths["url_input"])))
    url_input.send_keys(img_url)
    time.sleep(0.5)

    width_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpaths["width_input"])))
    width_input.clear()
    width_input.send_keys(img_width)
    time.sleep(0.5)

    height_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpaths["height_input"])))
    height_input.clear()
    height_input.send_keys(img_height)
    time.sleep(0.5)

    if "DE" in img_url:
        alignement_loc = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpaths["ausrichtung_input"])))
        dropdown = Select(alignement_loc)
        dropdown.select_by_visible_text("Rechts")
    else:
        time.sleep(0.5)
        actions = ActionChains(driver)
        for i in range(6):
            actions.send_keys(Keys.TAB)
            actions.pause(0.1)
        for i in range(2):
            actions.send_keys(Keys.ARROW_DOWN)
            actions.pause(0.1)
        actions.perform()

    if link_checkbox and link_url:
        time.sleep(0.5)
        link_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths["link_tab"])))
        driver.execute_script("arguments[0].click();", link_tab)

        link_url_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, xpaths["link_url_input"])))
        link_url_input.send_keys(link_url)

        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

    time.sleep(0.5)

    if "DE" in img_url:
        ok_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpaths["ok_button"])))
        driver.execute_script("arguments[0].click();", ok_button)
    else:
        actions = ActionChains(driver)
        actions.pause(0.1)
        actions.send_keys(Keys.TAB)
        actions.pause(0.1)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    try:
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(
            (By.XPATH, '//div[contains(@class, "cke_dialog_title") and text()="Bildeigenschaften"]')))
    except TimeoutException:
        print("Popup did not close within 10 seconds. Attempting to click the OK button again.")
        ok_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths["ok_button"])))
        driver.execute_script("arguments[0].click();", ok_button)
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, xpaths["popup_title"])))


def process_articles(driver, task_data):
    """
    :param driver: The Selenium WebDriver object.
    :param task_data: A dictionary containing the task data.
    :return: None.

    This method processes articles based on the provided task data using a Selenium WebDriver object.

    The task data dictionary should have the following keys:
    - "article_numbers": a string containing comma-separated article numbers.
    - "img1_url": a string representing the URL for the first image.
    - "img2_url": a string representing the URL for the second image.
    - "width": an integer representing the width of the images.
    - "height": an integer representing the height of the images.
    - "link_checkbox": a boolean value indicating whether a link should be added to the images.
    - "link_input_de": a string representing the link input for the German version.
    - "link_input_fr": a string representing the link input for the French version.
    - "marke": a string representing the brand of the articles.
    - "kategorie": a string representing the category of the articles.

    The method follows these steps:
    1. Extracts the article numbers from the task data.
    2. Logs in to the website using the provided credentials.
    3. Navigates to the categories page.
    4. Selects the brand and category if they are specified.
    5. Processes each article number:
       - Finds the corresponding product link.
       - Inserts the first and second images into the text editor.
       - Submits the changes.
    6. Prints a message indicating the successful processing of each article number.
    7. Quits the WebDriver.

    If an exception occurs during the processing of an article number, an error message is printed.

    Note: The method assumes that the necessary imports (e.g., time, traceback, WebDriverWait, EC, By) have been done
    prior to calling it.
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
    time.sleep(0.5)

    brand = task_data["marke"]
    if brand != 'Kamerasysteme + Objektive':
        brand_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//b/a[text()='{brand}']")))
        driver.execute_script("arguments[0].click();", brand_element)

    category = task_data["kategorie"]
    if category != 'Kategorie wählen':
        category_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//b/a[text()='{category}']")))
        driver.execute_script("arguments[0].click();", category_element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            time.sleep(1)
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.dataTableRow')))
            time.sleep(1)

            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)')
                number = number_element.text.strip()

                if number == article_number:
                    product_link_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3) a')
                    driver.execute_script("arguments[0].scrollIntoView(true);", product_link_element)
                    driver.execute_script("arguments[0].click();", product_link_element)
                    break

            insert_image_text_editor(driver, img1_url, img_width, img_height, link_input_de, link_checkbox)
            insert_image_text_editor(driver, img2_url, img_width, img_height, link_input_fr, link_checkbox)

            time.sleep(0.5)

            submit_button_locator = (By.XPATH, '//button[@title="Speichern" and @type="submit"]')
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button_locator))
            driver.execute_script("arguments[0].click();", submit_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

            print(f"Processed article: {article_number}")

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def remove_articles_images(driver, task_data):
    """
    :param driver: The WebDriver instance for controlling the browser.
    :param task_data: A dictionary containing task-specific data, including "article_numbers", "marke", and "kategorie".
    :return: None

    This method removes images from the specified articles in a web application.

    The method performs the following steps:
    1. Extracts the article numbers from the task_data dictionary.
    2. Logs into the web application using the provided credentials.
    3. Navigates to the categories page in the application.
    4. Finds and selects the specified brand and category if they are not the default values.
    5. Waits for table elements to load on the page.
    6. Iterates over the article numbers.
        a. Skips empty article numbers.
        b. Searches for the row containing the article number.
        c. Removes images from specified editors.
        d. Clicks the submit button to save the changes.
        e. Waits for table elements to load again.
        f. Catches and prints any exceptions raised during the loop.
    7. Quits the WebDriver.

    Note: The error handling in this code is minimal and should be enhanced for production use.

    Example usage:
        remove_articles_images(driver, task_data)
    """
    article_numbers = [num.strip() for num in task_data["article_numbers"].split(',')]

    login(driver, 'feigelluck@gmail.com', 'Graphicart#1')

    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")

    brand = task_data["marke"]
    if brand != 'Kamerasysteme + Objektive':
        brand_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[text()='{brand}']")))
        driver.execute_script("arguments[0].click();", brand_element)

    category = task_data["kategorie"]
    if category != 'Kategorie wählen':
        category_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[text()='{category}']")))
        driver.execute_script("arguments[0].click();", category_element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            time.sleep(1)
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.dataTableRow')))

            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)')
                number = number_element.text.strip()

                if number == article_number:
                    product_link_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3) a')
                    driver.execute_script("arguments[0].scrollIntoView(true);", product_link_element)
                    driver.execute_script("arguments[0].click();", product_link_element)
                    break

            remove_image_from_editor(driver, "cke_products_short_description_2")
            remove_image_from_editor(driver, "cke_products_short_description_5")

            submit_button_locator = (By.XPATH, '//button[@title="Speichern" and @type="submit"]')
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button_locator))
            driver.execute_script("arguments[0].click();", submit_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def execute_task(task_filename):
    """
    Execute a task by reading a task file, setting up the necessary dependencies, and executing the task.

    :param task_filename: The filename of the task file to execute.
    :return: None
    """
    if not os.path.exists(task_filename):
        print(f"Task file not found: {task_filename}")
        return

    with open(task_filename, 'r') as file:
        task = json.load(file)

    # Check if we are running as a packaged executable
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    chromedriver_path = os.path.join(base_path, 'chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_path = os.path.join(base_path, 'chrome', 'win64-118.0.5993.70', 'chrome-win64', 'chrome.exe')
    chrome_options.binary_location = chrome_path

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

    # Handle follow-up tasks
    if task.get("follow_up", False):
        for next_task in task["subsequent_tasks"]:
            execute_task(next_task)


def main(task_filename):
    """
    :param task_filename: The filename of the task to execute.
    :return: None
    """
    execute_task(task_filename)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python execute_task.py <task_filename>")
    else:
        main(sys.argv[1])
