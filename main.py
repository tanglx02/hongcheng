# 1.导入库
import math
import random
import mariadb
import os
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.edge.options import Options
import base64
from selenium.webdriver.common.by import By
import base64
import ddddocr

#全局属性
ocr = ddddocr.DdddOcr()  # 获取识别对象
#conn = mariadb.connect(user='root', password='Ysb@12345678', host='10.180.100.250', port=23456, database='yunjing') #连接数据库
#设置浏览器属性
driver_path='./call/msedgedriver.exe'
def get_options(params):
    """
    Edge浏览器添加启动参数辅助函数
    :param params: 启动参数,为字符串类型直接添加,为列表或元组类型添加多个
    :return: 添加启动参数后的字典
    """
    options = {
        "browserName": "MicrosoftEdge",
        "version": "",
        "platform": "WINDOWS",
        "ms:edgeOptions": {
            "extensions": [], "args": []
        }
    }
    if isinstance(params, str):
        options["ms:edgeOptions"]["args"].append(params)
    elif isinstance(params, (list, tuple)):
        # 利用集合去重
        params = list(set(params))
        options["ms:edgeOptions"]["args"].extend(params)

    return options
edge_option = get_options("--ignore-certificate-errors")

# 随机sleep
def sleep(MIN,Max):
    time_num=random.randint(MIN,Max)
    time.sleep(time_num)

#执行浏览器操作
def run_hongcheng(username,password):
    # 运行前关闭浏览器的所有窗口
    print("尝试关闭多余的360急速浏览器进程")
    os.system("taskkill /im 360ChromeX.exe /f")

    #创建浏览器对象并打开url
    driver = webdriver.Edge(executable_path=driver_path, capabilities=edge_option)  #创建对象
    driver.maximize_window()    #窗口最大化
    driver.delete_all_cookies()  # 清空cookie
    driver.get('https://swfucce.sccchina.net/')  # 打开url
    time.sleep(5)  # 等待3秒 #正式环境改为5秒
    def login():
        driver.refresh()
        time.sleep(5)
        #输入账号密码
        print("开始登录")
        print("输入账号")
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[1]/input').send_keys(username)
        print("输入密码")
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[2]/input').send_keys(password)
        #识别验证码并输入
        print("输入验证码")
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[3]/img').click()  #点击验证码
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[3]/div/input').click()
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[3]/div/input').clear()
        image_data = driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[3]/img')
        image_data.screenshot('tmp_yzm.png')
        with open('tmp_yzm.png', 'rb') as f:
            image_bytes = f.read()
        res = ocr.classification(image_bytes)  # 识别验证码
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[3]/div[3]/div/input').send_keys(res)  # 输入验证码
        #点击登录
        driver.find_element_by_xpath('//*[@id="login-form"]/form/div[2]/div[1]/div[4]/input').click()   #点击登录
        time.sleep(10)  #登录后等待10秒
        login_url=driver.current_url
        return login_url
    # 判断登录状态
    i = 0
    while i <= 2:  # 尝试登录次数(三次未成功为验证码错误,最后一次判定为账号密码错误)
        i += 1
        try:
            login_url = login()  # 获取登录后的url
        except:
            driver.refresh()    # 如果登录页面失败刷新浏览器
            login_url=login()   # 获取登录后的url
        if login_url != 'https://swfucce.sccchina.net/' :
            print('登录成功！')
            break
        elif i == 1:
            print("登录失败，尝试重新登录")
            continue
        elif i == 2:
            print("多次登陆失败！账号密码错误或者网页信息发生改变!")
            return 'login_error'
            # 记录此账号标记为login_error
    def view():
        driver.refresh() #刷新浏览器
        time.sleep(30)
        #点击弹窗
        try:
            driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/span').click()
            print("检测到弹窗,以点击")
        except:
            print("没有检查到弹窗")
        time.sleep(2)
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/span[2]').click()
            print("检测到弹窗,以点击")
        except:
            print("没有检查到弹窗")
        #等待继续开发`
        #打印登录用户
        hi_name=driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div[1]/div/div[2]/p[1]').text
        print(hi_name)
        #课程总数
        study_all=driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div/div[3]/div[1]/div')
        study_all=len(study_all)
        #遍历检查学习课程列表
        #study_list={"study_0":["课程状态","课程序号","课程名称","已学习时间","总时间"]}
        study_list={}
        print(f"未学习的课程数量为:")
        for x in range(1,study_all+1):
            #获取课程状态
            status=driver.find_element_by_xpath(f'/html/body/div[3]/div[1]/div/div[3]/div[1]/div[{x}]/div[2]/div[1]/div[2]')
            study_status=status.get_attribute('class')
            if study_status=="courseFlag courseEd":
                continue
            study_num=x
            study_name=driver.find_element_by_xpath(f'/html/body/div[3]/div[1]/div/div[3]/div[1]/div[{x}]/div[2]/div[2]/div[1]/div/p[1]').text
            study_time=driver.find_element_by_xpath(f'/html/body/div[3]/div[1]/div/div[3]/div[1]/div[{x}]/div[2]/div[2]/div[1]/p[2]/span[8]').text
            study_start_time = float(study_time[:study_time.index("/") - 1])
            study_all_time = int(study_time[study_time.index("/") + 2:])
            if study_start_time>=study_all_time:
                continue
            study_list[f"study_{x}"]=[study_status,study_num,study_name,study_start_time,study_all_time]
            print(f"课程序号:{x},课程名称:{study_name[2:]},课程总时间为{study_all_time},课程已学习时间:{study_start_time}")
        #开始点击学习视频
        def 中国近现代史纲要():
            pass
        def 思想政治理论实践教学():
            pass
        def 毛泽东思想和中国特色社会主义理论体系概论():
            pass
        def 马克思主义基本原理概论():
            pass
        def 高等数学():
            pass

    try:
        view()
        return 'ok'
    except:
        print("浏览失败")
        return 'view_error'

status=run_hongcheng("2430809010405",'tanglx!2002')
print(status)
time.sleep(10000)