"""
### execute_task.py

---

### function: login

This method performs the login operation by locating and interacting with the necessary elements on the login page.

#### Args:
- driver: Web driver instance used for browsing.
- email: Email address for login.
- password: Password for login.

---

### function: remove_image_from_editor

This method removes all images from a specific editor on a web page using the provided WebDriver instance.

#### Args:
- driver: The WebDriver instance used to interact with the web page.
- editor_id: The ID of the editor element.

---

### function: insert_image_text_editor

This method inserts an image into a text editor using the given WebDriver object. The image URL, width, and height are specified. If a link URL is provided and the link_checkbox flag is True, a link is added to the image.

---

### function: process_articles

This method processes articles on the Graphicart website. It takes a WebDriver instance and task data as parameters. The task data should be a dictionary containing specific keys.

#### Args:
- driver: The Selenium WebDriver instance.
- task_data: A dictionary containing the task data.

---

### function: remove_articles_images

This method removes images from articles on the Graphicart website. It takes a WebDriver instance and task data as parameters.

#### Args:
- driver: The Selenium WebDriver instance.
- task_data: A dictionary containing task data.

---

### function: execute_task

Execute a task from a given task file.

#### Args:
- task_filename: The path to the task file.

---

### function: main

Execute a task specified by the given filename.

#### Args:
- task_filename: The name of the file containing the task.

#### Returns:
- None
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


def login(driver, email, password):
    """
    :param driver: Web driver instance used for browsing.
    :param email: Email address for login.
    :param password: Password for login.
    :return: None

    This method performs the login operation by locating and interacting with the necessary elements on the login page.

    The `driver` parameter should be an instance of a web driver, such as Selenium WebDriver, used for browsing the web.

    The `email` parameter should be a string representing the email address associated with the account.

    The `password` parameter should be a string representing the password for the account.

    The method does not return anything.
    """
    kundenlogin_button = WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'a.dropdown-toggle[title="Anmeldung"]'))
    )
    kundenlogin_button.click()

    email_field = WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.ID, 'box-login-dropdown-login-username'))
    )
    email_field.send_keys(email)

    password_field = WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.ID, 'box-login-dropdown-login-password'))
    )
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.XPATH, '//input[@value="Anmelden"]'))
    )
    login_button.click()


def remove_image_from_editor(driver, editor_id):
    """
    :param driver: The WebDriver instance used to interact with the web page.
    :param editor_id: The ID of the editor element.
    :return: None

    This method removes all images from a specific editor on a web page using the provided WebDriver instance.

    The method first waits for the presence of the editor iframe by locating it using its CSS selector with the given editor_id. Once the iframe is found, the WebDriver switches to it.

    Then, a JavaScript script is executed inside the iframe context. This script finds the `<ul>` element within the editor's body and iterates over its child `<li>` elements. For each `<li>`, it checks if there is an `<img>` element within it, and if so, removes it.

    After removing all the images, the WebDriver switches back to the default content.

    Please note that this method relies on the following imports:
    - `WebDriverWait` from `selenium.webdriver.support.ui`
    - `ec` (Expected Conditions) from `selenium.webdriver.support.expected_conditions`
    - `By` from `selenium.webdriver.common.by`
    """
    iframe = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, f'#{editor_id} iframe')))
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
    :param driver: The WebDriver object used to interact with the browser.
    :param img_url: The URL of the image to be inserted.
    :param img_width: The width of the image in pixels.
    :param img_height: The height of the image in pixels.
    :param link_url: The URL the image should link to.
    :param link_checkbox: A flag indicating whether a link should be added to the image.
    :return: None

    This method inserts an image into a text editor using the given WebDriver object. The image URL, width, and height are specified. If a link URL is provided and the link_checkbox flag is True, a link is added to the image.

    Example usage:
    insert_image_text_editor(driver, "https://example.com/image.jpg", 800, 600, "https://example.com", True)
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

    img_button = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpaths["img_button"])))
    driver.execute_script("arguments[0].click();", img_button)

    url_input = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, xpaths["url_input"])))
    url_input.send_keys(img_url)

    width_input = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, xpaths["width_input"])))
    width_input.clear()
    width_input.send_keys(img_width)

    height_input = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, xpaths["height_input"])))
    height_input.clear()
    height_input.send_keys(img_height)

    if "DE" in img_url:
        alignement_loc = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, xpaths["ausrichtung_input"])))
        dropdown = Select(alignement_loc)
        dropdown.select_by_visible_text("Rechts")
    else:
        actions = ActionChains(driver)
        for _ in range(6):
            actions.send_keys(Keys.TAB)
        for _ in range(2):
            actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

    if link_checkbox and link_url:
        link_tab = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpaths["link_tab"])))
        driver.execute_script("arguments[0].click();", link_tab)

        link_url_input = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, xpaths["link_url_input"])))
        link_url_input.send_keys(link_url)

        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

    if "DE" in img_url:
        ok_button = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, xpaths["ok_button"])))
        driver.execute_script("arguments[0].click();", ok_button)
    else:
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    try:
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located(
            (By.XPATH, '//div[contains(@class, "cke_dialog_title") and text()="Bildeigenschaften"]')))
    except TimeoutException:
        print("Popup did not close within 10 seconds. Attempting to click the OK button again.")
        ok_button = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpaths["ok_button"])))
        driver.execute_script("arguments[0].click();", ok_button)
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, xpaths["popup_title"])))


def process_articles(driver, task_data):
    """

    :param driver: The Selenium WebDriver instance.
    :param task_data: A dictionary containing the task data, including article numbers, image URLs, image dimensions, and other inputs.

    :return: None

    This method processes articles on the Graphicart website. It takes a WebDriver instance and task data as parameters. The task data should be a dictionary containing the following keys:
    - "article_numbers": A string of comma-separated article numbers to process.
    - "img1_url": The URL of the first image.
    - "img2_url": The URL of the second image.
    - "width": The width of the images.
    - "height": The height of the images.
    - "link_checkbox": A boolean indicating whether to include a link with the images.
    - "link_input_de": The input for the German link (optional).
    - "link_input_fr": The input for the French link (optional).

    The method starts by logging in to the website using the provided email and password.

    Then, it navigates to the appropriate category page based on the brand and category provided in the task data, if they are not set to their default values.

    It waits for the category page to load, then iterates through the provided article numbers.

    For each article number, it searches for a matching row in the table of articles. Once found, it clicks on the product link for that article.

    It calls the "insert_image_text_editor" method twice, passing the URLs, dimensions, link inputs, and checkbox value. This method inserts the images and optional links into the text editor on the product page.

    After that, it clicks the "Speichern" (Save) button, waits for the page to reload, and prints a message to indicate that the article has been processed.

    Any exceptions that occur during the processing of articles are caught, and error messages are printed.

    Finally, the WebDriver instance is closed.

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

    brand = task_data["marke"]
    if brand != 'Kamerasysteme + Objektive':
        brand_element = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, f"//b/a[text()='{brand}']")))
        driver.execute_script("arguments[0].click();", brand_element)

    category = task_data["kategorie"]
    if category != 'Kategorie wählen':
        category_element = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, f"//b/a[text()='{category}']")))
        driver.execute_script("arguments[0].click();", category_element)
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            rows = WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.dataTableRow')))

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

            submit_button_locator = (By.XPATH, '//button[@title="Speichern" and @type="submit"]')
            submit_button = WebDriverWait(driver, 10).until(ec.element_to_be_clickable(submit_button_locator))
            driver.execute_script("arguments[0].click();", submit_button)
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

            print(f"Processed article: {article_number}")

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def remove_articles_images(driver, task_data):
    """

        :param driver: The Selenium WebDriver instance.
        :param task_data: A dictionary containing task data, with the following keys:
                          - "article_numbers": A string of comma-separated article numbers to be processed.
                          - "marke": The brand name.
                          - "kategorie": The category name.
        :return: None
    """
    article_numbers = [num.strip() for num in task_data["article_numbers"].split(',')]

    login(driver, 'feigelluck@gmail.com', 'Graphicart#1')

    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")

    brand = task_data["marke"]
    if brand != 'Kamerasysteme + Objektive':
        brand_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, f"//a[text()='{brand}']")))
        driver.execute_script("arguments[0].click();", brand_element)

    category = task_data["kategorie"]
    if category != 'Kategorie wählen':
        category_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, f"//a[text()='{category}']")))
        driver.execute_script("arguments[0].click();", category_element)
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            rows = WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.dataTableRow')))

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
            submit_button = WebDriverWait(driver, 10).until(ec.element_to_be_clickable(submit_button_locator))
            driver.execute_script("arguments[0].click();", submit_button)
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")))

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def execute_task(task_filename):
    """
    Execute a task from a given task file.

    :param task_filename: The path to the task file.
    :return: None
    """
    if not os.path.exists(task_filename):
        print(f"Task file not found: {task_filename}")
        return

    with open(task_filename, 'r') as file:
        task = json.load(file)

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # if script is packed (frozen), use the directory of the executable, otherwise use the directory of this script file (__file__)
    root_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

    # go up until the root directory
    root_dir = os.path.dirname(root_dir)

    chromedriver_path = os.path.join(root_dir, 'chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_path = os.path.join(root_dir, 'chrome', 'win64-118.0.5993.70', 'chrome-win64', 'chrome.exe')
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

    if task.get("follow_up", False):
        subsequent_tasks = task.get("subsequent_tasks", [])
        # if "subsequent_tasks" doesn't exist in task, an empty list is returned.
        for next_task in subsequent_tasks:
            execute_task(next_task)


def main(task_filename):
    """
    Execute a task specified by the given filename.

    :param task_filename: The name of the file containing the task.
    :type task_filename: str
    :return: None
    """
    execute_task(task_filename)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python execute_task.py <task_filename>")
    else:
        main(sys.argv[1])
