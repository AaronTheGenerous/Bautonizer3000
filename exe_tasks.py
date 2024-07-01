import sys
import json
import os
import datetime
import time
import subprocess
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def main(task_filename):
    if not os.path.exists(task_filename):
        print(f"Task file not found: {task_filename}")
        return

    with open(task_filename, "r") as file:
        task = json.load(file)

    service = Service("path_to_chromedriver")
    driver = webdriver.Chrome(service=service)

    try:
        if task["task_type"] == "process_articles":
            process_articles(driver, task["data"])
        elif task["task_type"] == "remove_articles_images":
            remove_articles_images(driver, task["data"])
    finally:
        driver.quit()

    # Schedule the next task if there is one
    if task.get("subsequent_tasks"):
        for next_task_filename in task["subsequent_tasks"]:
            with open(next_task_filename, "r") as file:
                next_task = json.load(file)
            execute_task(next_task_filename, next_task)

def execute_task(task_filename, task):
    service = Service("path_to_chromedriver")
    driver = webdriver.Chrome(service=service)

    try:
        if task["task_type"] == "process_articles":
            process_articles(driver, task["data"])
        elif task["task_type"] == "remove_articles_images":
            remove_articles_images(driver, task["data"])
    finally:
        driver.quit()

    # Schedule the next task if there is one
    if task.get("subsequent_tasks"):
        for next_task_filename in task["subsequent_tasks"]:
            with open(next_task_filename, "r") as file:
                next_task = json.load(file)
            execute_task(next_task_filename, next_task)

def process_articles(driver, data):
    login(driver, "feigelluck@gmail.com", "Graphicart#1")

    driver.get("https://www.graphicart.ch/shop/admin/categories.php?cPath=7")
    time.sleep(0.5)

    brand = data["marke"]
    if brand != "Kamerasysteme + Objektive":
        brand_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//b/a[text()='{brand}']"))
        )
        driver.execute_script("arguments[0].click();", brand_element)

    category = data["kategorie"]
    if category != "Kategorie wählen":
        category_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//b/a[text()='{category}']"))
        )
        driver.execute_script("arguments[0].click();", category_element)

    article_numbers = [num.strip() for num in data["article_numbers"].split(",")]
    for article_number in article_numbers:
        if not article_number:
            continue
        try:
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "tr.dataTableRow")
                )
            )
            for row in rows:
                number_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
                if number_element.text.strip() == article
