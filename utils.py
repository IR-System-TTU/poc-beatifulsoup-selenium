def scrolldownWalmart(number, driver, scrollHeight, defaultSpeed = 0.00001): #improve performance for falabella
    for i in range(0, scrollHeight, 10):
        number = i
        driver.execute_script("window.scrollTo(0, "+str(number)+")")
        time.sleep(defaultSpeed)