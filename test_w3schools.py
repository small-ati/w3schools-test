import pytest,os,random,requests,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
@pytest.fixture(params=['edge'])
def driver(request):
    """每条测试用例前，按需启动/关闭浏览器"""
    browser = request.param
    if browser == 'edge':
        driver_path = os.path.join(os.path.dirname(__file__),'msedgedriver.exe')
        service = EdgeService(driver_path)
        driver = webdriver.Edge(service=service)
    yield driver
    driver.quit()
def test_homepage_api():
    """验证首页接口状态码和标题"""
    url = 'https://www.w3schools.com/python'
    response = requests.get(url,timeout=10)
    assert response.status_code == 200 ,'状态码不符:{response.status_code}'
    html = response.text
    start = html.find('<title>') + len("<title>")
    end = html.find("</title>")
    title = html[start:end] if start > -1 and end > -1 else ''
    assert "Python Tutorial" in title ,f"标题不符:{title}"
@pytest.fixture
def base_url(request):
    """获取命令行传入的网址，如果没有则用默认值"""
    return request.config.getoption("--url")
@pytest.mark.parametrize("link_text",[
    "Python HOME",
    "Python Intro",
    "Python Get Started",
])
def test_navigation_links(link_text,base_url,site_config,driver):
    """逐个验证每个期望链接是否存在于导航栏"""
    url = base_url
    if site_config is None or site_config["nav_bar_id"] is None:
        pytest.skip("当前网站没有配置导航栏，跳过测试")
    try:
        driver.get(url)
        wait = WebDriverWait(driver,10)
        nav_bar = wait.until(EC.presence_of_element_located((By.ID,'leftmenuinner')))
        all_links = nav_bar.find_elements(By.TAG_NAME,'a')
        actual_texts = [link.text.strip() for link in all_links if link.text.strip()]
        assert link_text in actual_texts,f"链接:'{link_text}'不在导航栏中"
    except:
        screenshot_dir = os.path.join(os.path.dirname(__file__),'screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"error_{timestamp}.png"
        filepath = os.path.join(os.path.dirname(__file__),filename)
        driver.save_screenshot(filepath)
        print(f"截图已保存:{file_path}")
@pytest.mark.parametrize("run",range(3))
def test_random_link_click(run,base_url,site_configdriver):
    """随机点击一个链接，验证跳转后标题包含 Python（重复3次）"""
    url = base_url
    try:
        driver.get(url)
        wait = WebDriverWait(driver,10)
        nav_bar = wait.until(EC.presence_of_element_located((By.ID,'leftmenuinner')))
        all_links = nav_bar.find_elements(By.TAG_NAME,'a')
        valid_links = [link for link in all_links if link.text.strip()]
        assert len(valid_links) > 0 , "没有找到有效链接"
        random_link = random.choice(valid_links)
        random_text = random_link.text.strip()
        print(f'\n第{run+1}次随机点击："{random_text}"')
        try:
            random_link.click()
        except:
            driver.execute_script('arguments[0].click;',random_link)
        WebDriverWait(driver,10).until(EC.title_contains("Python"))
        page_title = driver.title
        assert site_config["title_keyword"] in page_title , f"标题不符：{page_title}"
        print(f"第{run+1}次点击后标题:'{page_title}'")
    except:
        screenshot_dir = os.path.join(os.path.dirname(__file__),'screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"error_{timestamp}.png"
        file_path = os.path.join(screenshot_dir,filename)
        driver.save_screenshot(file_path)
        print(f"截图已保存:{file_path}")
