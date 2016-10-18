from flask import current_app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

CLARO_URL = 'http://piloto.dacclaro.com.pe/pretups/'

def do_recharge(phone_number, amount):
    try:
        if current_app.debug: driver = webdriver.Chrome('chromedriver.exe')
        else: driver = webdriver.PhantomJS()
        wait = WebDriverWait(driver, 10)
        driver.get(CLARO_URL)

        # login
        element = wait.until(expected_conditions.presence_of_element_located((By.NAME, 'loginID')))
        element.send_keys(current_app.config.get('CLARO_USERNAME'))
        element = driver.find_element_by_name('password')
        element.send_keys(current_app.config.get('CLARO_PASSWORD'))
        element.submit()

        # switch to frame
        element = wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'FRAME')))
        driver.switch_to.frame(element)

        # click on mobile recharge module
        element = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH,
                '//a[@href="/pretups/c2sRechargeAction.do?method=c2sRechargeAuthorize&moduleCode=C2STRF"]')))
        element.click()

        # fill form
        element = wait.until(expected_conditions.presence_of_element_located((By.NAME, 'subscriberMsisdn')))
        element.send_keys(phone_number)
        element = driver.find_element_by_name('amount')
        element.send_keys(amount)
        element = driver.find_element_by_name('pin')
        element.send_keys(current_app.config.get('CLARO_PIN'))
        element.submit()

        # confirm
        element = wait.until(expected_conditions.element_to_be_clickable((By.NAME, 'btnSubmit')))
        element.click()

        # get confirm
        while True:
            element = wait.until(
                expected_conditions.element_to_be_clickable((By.XPATH,
                     '//a[@href="javascript:submitNotification()"]')))
            element.click()

            # wait until form appears
            wait.until(expected_conditions.presence_of_element_located((By.NAME, 'CSRF_TOKEN')))

            # get in process or success
            in_process = driver.find_elements_by_xpath('//td[contains(text(), "En proceso")]')
            success = driver.find_elements_by_xpath('//td[contains(text(), "EXITOSO")]')

            if success or not in_process:
                if success: return True
                elif not in_process: return False

    except Exception, e:
        current_app.logger.error(e)
        return False

    finally:
        driver.close()