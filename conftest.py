import pytest
def pytest_addoption(parser):
    parser.addoption("--url",action="store",default="https://www.w3schools.com/python",
                     help="要测试的网站")
SITE_CONFIG = {
    "https://www.w3schools.com/python/":{
        "nav_bar_id":"leftmenuinner",
        "title_keyword":"Python",
        "expected_links":["Python HOME","Python Intro","Python Get Started"],
        },
    "https://www.example.com":{
        "nav_bar_id":None,
        "title_keyword":"Example",
        "expected_links":[],
        },
    }
@pytest.fixture
def base_url(request):
    return request.config.getoption('--url')
@pytest.fixture
def site_config(base_url):
    url = base_url.rstrip('/')
    for key,config in SITE_CONFIG.items():
        if key.rstrip('/') == url:
            return config
        return None
