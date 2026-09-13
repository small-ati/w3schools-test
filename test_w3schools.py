import os,time,random,requests,pytest
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
@pytest.fixture(params=['edge'])
def driver(request):
    '''配置多个浏览器驱动器'''
    browser = request.param
    if browser == 'edge':
        driver_path = os.path.join(os.path.dirname(__file__),'msedgedriver.exe')
        service = EdgeService(driver_path)
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Edge(service=service,options=options)
        driver.set_page_load_timeout(60)
        yield driver
        driver.quit()
def test_homepage_api(base_url):
    '''接口测试，获取标题并验证'''
    if base_url.startswith('file://'):
        pytest.skip('本地文件不需要接口测试')
    headers = {
        'User-Agent':'Mozilla/5.0(windows NT 10.0; win64; x64) AppleWebKit/537.36(KHTML,like Gecko)Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
    response = requests.get(base_url,timeout=10,headers=headers)
    assert response.status_code == 200,f'状态码不符:{response.status_code}'
    html = response.text
    start = html.find('<title>') + len('<title>')
    end = html.find('</title>')
    title = html[start:end] if start > -1 and end > -1 else ''
    assert 'Python Tutorial' in title ,f'标题不符:{title}'
def test_navigation_links(driver,base_url,site_config):
    '''检查导航栏并验证多个链接是否有效'''
    if site_config is None or site_config['nav_bar_id'] is None:
        pytest.skip('当前网站未配置导航栏，跳过测试')
    driver.get(base_url)
    wait = WebDriverWait(driver,10)
    nav_bar = wait.until(EC.presence_of_element_located((By.ID,site_config['nav_bar_id'])))
    all_links = nav_bar.find_elements(By.TAG_NAME,'a')
    actual_texts = [link.text.strip()for link in all_links if link.text.strip()]
    missing = set(site_config['expected_links']) - set(actual_texts)
    assert not missing ,f'缺失:{missing}'
@pytest.mark.parametrize('run',range(3))
def test_random_link_click(driver,run,base_url,site_config):
    '''随机点击页面链接并获取标题并验证'''
    if site_config is None or site_config['nav_bar_id'] is None:
        pytest.skip('当前网址未配置导航栏，跳过测试')
    try:
        driver.get(base_url)
        wait = WebDriverWait(driver,10)
        nav_bar = wait.until(EC.presence_of_element_located((By.ID,site_config['nav_bar_id'])))
        all_links = nav_bar.find_elements(By.TAG_NAME,'a')
        valid_links = [link for link in all_links if link.text.strip()]
        assert len(valid_links) > 0,f'没有找到有效链接'
        random_link = random.choice(valid_links)
        random_text = random_link.text.strip()
        print(f'第{run+1}次随机点击:{random_text}')
        try:
            random_link.click()
        except:
            driver.execute_script('arguments[0].click;',random_link)
        WebDriverWait(driver,10).until(EC.title_contains(site_config['title_keyword']))
        page_title = driver.title
        assert site_config['title_keyword'] in page_title,f'标题不符：{page_title}'
        print(f'第{run+1}次点击->{page_title}')
    except:
        screenshot_dir = os.path.join(os.path.dirname(__file__),'screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        timetamp = time.strftime('%Y%m%d_%H%M%S')
        file_name = f'error_{timetamp}.png'
        file_path = os.path.join(screenshot_dir,file_name)
        driver.save_screenshot(file_path)
        print(f'图片已保存到:{file_path}')
        raise
def test_search_box_exists(driver,base_url):
    '''验证页面存在搜索框'''
    driver.get(base_url)
    wait = WebDriverWait(driver,10)
    search_box = wait.until(EC.presence_of_element_located((By.ID,'search2')))
    assert search_box is not None,'搜索框不存在'
