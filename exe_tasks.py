# execute_task.py

import sys
import json
import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def login(driver, email, password):
    kundenlogin_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a.dropdown-toggle[title="Anmeldung"]')
        )
    )
    kundenlogin_button.click()

    email_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "box-login-dropdown-login-username"))
    )
    email_field.send_keys(email)

    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "box-login-dropdown-login-password"))
    )
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//input[@value="Anmelden"]'))
    )
    login_button.click()


def remove_image_from_editor(driver, editor_id):
    time.sleep(1)
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"#{editor_id} iframe"))
    )
    driver.switch_to.frame(iframe)
    script = """
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
    """
    driver.execute_script(script)
    driver.switch_to.default_content()


def insert_image_text_editor(
    driver, img_url, img_width, img_height, link_url, link_checkbox
):
    editor_id = (
        "cke_products_short_description_2"
        if "DE" in img_url
        else "cke_products_short_description_5"
    )
    xpaths = {
        "img_button": '//*[@id="cke_135"]' if "DE" in img_url else '//*[@id="cke_357"]',
        "url_input": (
            '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_549_label"]'
            if "DE" in img_url
            else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_688_label"]'
        ),
        "width_input": (
            '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_559_label"]'
            if "DE" in img_url
            else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_698_label"]'
        ),
        "height_input": (
            '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_562_label"]'
            if "DE" in img_url
            else '//input[contains(@class, "cke_dialog_ui_input_text") and @aria-labelledby="cke_701_label"]'
        ),
        "ausrichtung_input": (
            '//select[contains(@class, "cke_dialog_ui_input_select") and @aria-labelledby[contains(., "_label")] and @style="width:90px"]'
            if "DE" in img_url
            else "//tr[4]/td[@role='presentation']/div[@role='presentation']//select[@safeclass~'\bcke_dialog_ui_input_select\b']"
        ),
        "ok_button": '//a[contains(@class, "cke_dialog_ui_button_ok") and @title="OK"]',
        "link_tab": (
            '//*[@id="cke_Link_595"]' if "DE" in img_url else '//*[@id="cke_Link_734"]'
        ),
        "link_url_input": (
            'input.cke_dialog_ui_input_text[type="text"][aria-labelledby="cke_587_label"]'
            if "DE" in img_url
            else 'input.cke_dialog_ui_input_text[type="text"][aria-labelledby="cke_726_label"]'
        ),
        "zielseite_input": (
            '//*[@id="cke_597_select"]'
            if "DE" in img_url
            else '//*[@id="cke_591_select"]'
        ),
        "zielseite_select": (
            '//*[@id="cke_597_select"]/option[2]'
            if "DE" in img_url
            else '//*[@id="cke_591_select"]/option[2]'
        ),
    }

    img_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpaths["img_button"]))
    )
    driver.execute_script("arguments[0].click();", img_button)
    time.sleep(0.5)

    url_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, xpaths["url_input"]))
    )
    url_input.send_keys(img_url)
    time.sleep(0.5)

    width_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpaths["width_input"]))
    )
    width_input.clear()
    width_input.send_keys(img_width)
    time.sleep(0.5)

    height_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpaths["height_input"]))
    )
    height_input.clear()
    height_input.send_keys(img_height)
    time.sleep(0.5)

    alignement_loc = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpaths["ausrichtung_input"]))
    )
    dropdown = Select(alignement_loc)
    dropdown.select_by_visible_text("Rechts")

    if link_checkbox and link_url:
        time.sleep(0.5)
        link_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths["link_tab"]))
        )
        driver.execute_script("arguments[0].click();", link_tab)

        link_url_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, xpaths["link_url_input"])
            )
        )
        link_url_input.send_keys(link_url)

        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

    time.sleep(0.5)

    ok_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpaths["ok_button"]))
    )
    driver.execute_script("arguments[0].click();", ok_button)

    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    '//div[contains(@class, "cke_dialog_title") and text()="Bildeigenschaften"]',
                )
            )
        )
    except TimeoutException:
        print(
            "Popup did not close within 10 seconds. Attempting to click the OK button again."
        )
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths["ok_button"]))
        )
        driver.execute_script("arguments[0].click();", ok_button)
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, xpaths["popup_title"]))
        )


def process_articles(driver, task_data):
    article_numbers = [num.strip() for num in task_data["article_numbers"].split(",")]
    img1_url = task_data["img1_url"]
    img2_url = task_data["img2_url"]
    img_width = task_data["width"]
    img_height = task_data["height"]
    link_checkbox = task_data["link_checkbox"]
    link_input_de = task_data["link_input_de"]
    link_input_fr = task_data["link_input_fr"]

    login(driver, "feigelluck@gmail.com", "Graphicart#1")

    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")
    time.sleep(0.5)

    brand = task_data["marke"]
    if brand != "Kamerasysteme + Objektive":
        brand_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//b/a[text()='{brand}']"))
        )
        driver.execute_script("arguments[0].click();", brand_element)

    category = task_data["kategorie"]
    if category != "Kategorie wählen":
        category_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//b/a[text()='{category}']"))
        )
        driver.execute_script("arguments[0].click();", category_element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")
            )
        )

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")
        )
    )

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            time.sleep(1)
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "tr.dataTableRow")
                )
            )
            time.sleep(1)

            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
                number = number_element.text.strip()

                if number == article_number:
                    product_link_element = row.find_element(
                        By.CSS_SELECTOR, "td:nth-child(3) a"
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", product_link_element
                    )
                    driver.execute_script("arguments[0].click();", product_link_element)
                    break

            insert_image_text_editor(
                driver, img1_url, img_width, img_height, link_input_de, link_checkbox
            )
            insert_image_text_editor(
                driver, img2_url, img_width, img_height, link_input_fr, link_checkbox
            )

            time.sleep(0.5)

            submit_button_locator = (
                By.XPATH,
                '//button[@title="Speichern" and @type="submit"]',
            )
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(submit_button_locator)
            )
            driver.execute_script("arguments[0].click();", submit_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "table.gx-compatibility-table.gx-categories-table",
                    )
                )
            )

            print(f"Processed article: {article_number}")

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def remove_articles_images(driver, task_data):
    article_numbers = [num.strip() for num in task_data["article_numbers"].split(",")]

    login(driver, "feigelluck@gmail.com", "Graphicart#1")

    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")

    brand = task_data["marke"]
    if brand != "Kamerasysteme + Objektive":
        brand_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[text()='{brand}']"))
        )
        driver.execute_script("arguments[0].click();", brand_element)

    category = task_data["kategorie"]
    if category != "Kategorie wählen":
        category_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[text()='{category}']"))
        )
        driver.execute_script("arguments[0].click();", category_element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")
            )
        )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.gx-compatibility-table.gx-categories-table")
        )
    )

    for article_number in article_numbers:
        if not article_number:
            print("Skipping empty article number")
            continue

        try:
            time.sleep(1)
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "tr.dataTableRow")
                )
            )

            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
                number = number_element.text.strip()

                if number == article_number:
                    product_link_element = row.find_element(
                        By.CSS_SELECTOR, "td:nth-child(3) a"
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", product_link_element
                    )
                    driver.execute_script("arguments[0].click();", product_link_element)
                    break

            remove_image_from_editor(driver, "cke_products_short_description_2")
            remove_image_from_editor(driver, "cke_products_short_description_5")

            submit_button_locator = (
                By.XPATH,
                '//button[@title="Speichern" and @type="submit"]',
            )
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(submit_button_locator)
            )
            driver.execute_script("arguments[0].click();", submit_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "table.gx-compatibility-table.gx-categories-table",
                    )
                )
            )

        except Exception as e:
            print(f"Exception raised in for loop for article_number {article_number}:")
            traceback.print_exc()

    driver.quit()


def main(task_filename):
    if not os.path.exists(task_filename):
        print(f"Task file not found: {task_filename}")
        return

    with open(task_filename, "r") as file:
        task = json.load(file)

    # Check if we are running as a packaged executable
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    chromedriver_path = os.path.join(base_path, "chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_path = os.path.join(
        base_path, "chrome", "win64-118.0.5993.70", "chrome-win64", "chrome.exe"
    )
    chrome_options.binary_location = chrome_path

    service = Service(chromedriver_path)

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.graphicart.ch/shop/de/")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if task["task_type"] == "process_articles":
        process_articles(driver, task["data"])
    elif task["task_type"] == "remove_articles_images":
        remove_articles_images(driver, task["data"])
    else:
        raise ValueError(f'Invalid task_type: {task["task_type"]}')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python execute_task.py <task_filename>")
    else:
        main(sys.argv[1])
