import config
import location
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

chromedriver_location = "C:/Users/" + location.location + "/Downloads/chromedriver_win32/chromedriver"
driver = webdriver.Chrome(chromedriver_location)

set_viewport_size(driver,1920,1000)

driver.get("https://www.pro-football-reference.com/play-index/win_prob.cgi")
driver.execute_script("window.scrollTo(0, 150)")

score_diff = '//*[@id="wp_calc"]/div/div[1]/div[1]/input'

##document.querySelector("#wp_calc > div > div.fields > div:nth-child(3) > div:nth-child(2) > div.choicefield > input[type=radio]")

quarter1 = '//*[@id="wp_calc"]/div/div[1]/div[3]/div[1]/div[1]/input'
quarter2 = '//*[@id="wp_calc"]/div/div[1]/div[3]/div[2]/div[1]/input'
quarter3 = '//*[@id="wp_calc"]/div/div[1]/div[3]/div[3]/div[1]/input'
quarter4 = '//*[@id="wp_calc"]/div/div[1]/div[3]/div[4]/div[1]/input'
quarterOT = '//*[@id="wp_calc"]/div/div[1]/div[3]/div[5]/div[1]/input'

time_min = '//*[@id="wp_calc"]/div/div[1]/div[4]/input[1]'
time_sec = '//*[@id="wp_calc"]/div/div[1]/div[4]/input[2]'

side_of_field = '//*[@id="field"]'
yard_line = '//*[@id="wp_calc"]/div/div[1]/div[5]/input'

down1 = '//*[@id="wp_calc"]/div/div[1]/div[6]/div[1]/div[1]/input'
down2 = '//*[@id="wp_calc"]/div/div[1]/div[6]/div[2]/div[1]/input'
down3 = '//*[@id="wp_calc"]/div/div[1]/div[6]/div[3]/div[1]/input'
down4 = '//*[@id="wp_calc"]/div/div[1]/div[6]/div[4]/div[1]/input'
yards_to_go = '//*[@id="wp_calc"]/div/div[1]/div[7]/input'

submit = '//*[@id="wp_calc"]/div/div[2]/div/input'


driver.find_element_by_xpath(score_diff).send_keys("-1")
driver.find_element_by_css_selector('#wp_calc > div > div.fields > div:nth-child(3) > div:nth-child(2) > div.choicefield > input[type=radio]').click()
driver.find_element_by_xpath(time_min).send_keys("3")
driver.find_element_by_xpath(time_sec).send_keys("44")

select = Select(driver.find_element_by_xpath(side_of_field))
select.select_by_visible_text("Opp")

driver.find_element_by_xpath(yard_line).send_keys("10")
driver.find_element_by_xpath(down3).click()
driver.find_element_by_xpath(yards_to_go).send_keys('3')

# driver.find_element_by_xpath(submit).click()

# expPoints1 = driver.find_element_by_xpath('//*[@id="pi"]/div[2]/h3[1]').text

# print("Pre-penalty EP: " + expPoints1.split(" ")[2])

# driver.get("https://www.pro-football-reference.com/play-index/win_prob.cgi")
# driver.execute_script("window.scrollTo(0, 150)")

# driver.find_element_by_xpath(score_diff).send_keys("-1")
# driver.find_element_by_xpath(quarter4).click()
# driver.find_element_by_xpath(time_min).send_keys("3")
# driver.find_element_by_xpath(time_sec).send_keys("44")

# select = Select(driver.find_element_by_xpath(side_of_field))
# select.select_by_visible_text("Opp")

# driver.find_element_by_xpath(yard_line).send_keys("5")
# driver.find_element_by_xpath(down3).click()
# driver.find_element_by_xpath(yards_to_go).send_keys('5')

# driver.find_element_by_xpath(submit).click()

# expPoints2 = driver.find_element_by_xpath('//*[@id="pi"]/div[2]/h3[1]').text

# print("Post-penalty EP: " + expPoints2.split(" ")[2])

# EPA = float(expPoints2.split(" ")[2]) - float(expPoints1.split(" ")[2])

# print("Expected Points Added because of penalty: " + str(EPA))
