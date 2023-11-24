# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
#
# dr = webdriver.Chrome()
# dr.implicitly_wait(10)  # 最大等待时间10秒(弹性等待)
# dr.set_window_size(1920, 1080)
# url = "https://www.photoworld.com.cn/category/images/page/2"
# dr.get(url)
#
# group = dr.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/article")
# for item in group:
#     # print(g.find_element(By.CLASS_NAME, "excerpt").text)
#     try:
#         print(
#             item.find_element(By.TAG_NAME, "aside").find_element(By.CLASS_NAME, "recent-author").text
#         )
#     except:
#         print("Null")




