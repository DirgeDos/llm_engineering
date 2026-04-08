from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

if __name__ == '__main__':
    TARGET_URL = "https://www.bright.cn/cp/zones/residential_proxy1/play"
    COOKIE_STR = "Hm_lvt_b4ae6de566ab613d22c0f8844dd852d2=1774426028; HMACCOUNT=1A5B73C5F9DD5E65; AGL_USER_ID=0b30e8b8-1e20-49ab-97f3-484302ad0acc; brd_device_id=5c325852-d2f7-4c6e-a062-56d39cbee2fb; _ga=GA1.1.83429603.1774425966; hubspotutk=193b4c62fe29e1a7b9a293f1b18bff6b; __hssrc=1; allow_cookies=1774426068385; XSRF-TOKEN=39173edeff14458985cb470aadb1428ead64767c8f996faf; _gcl_au=1.1.2131004200.1774425963.1433174459.1774425972.1774426137; two_step_verification=j%3A%7B%22email%22%3A%22danous%40ichestnuts.com%22%2C%22token%22%3A%22d08405ea5148d6af9caa508dc50a3f70720f2641e0167a549f32b907fe17f15c433ba4bfee643116695096198e372f6a%22%7D; connect.sid=s%3AVShrzqrd-qcnRr8m9xCWIswnh0F6xfcB.l9RuFYTbIAe2%2B3VL5SEW89q7ITIityy4Jgk9d7mTAzw; pll_language=zh-hans; brd_is_eu=false; _clck=1wdxzwg%5E2%5Eg4n%5E0%5E2275; mkt_sid3=72cc67e5-d1f4-4504-b072-38266c9711ef; brd_falcon_id=72cc67e5-d1f4-4504-b072-38266c9711ef; _clsk=iae87s%5E1774431335063%5E1%5E1%5Ea.clarity.ms%2Fcollect; user=%7B%22display_name%22%3A%22danous%40ichestnuts.com%22%2C%22verified%22%3A%222026-03-25T08%3A06%3A17.149Z%22%7D; user_heading_url=/cp/start; mp_f6ddaef254cfb0b8455d909449a24693_mixpanel=%7B%22distinct_id%22%3A%22danous%40ichestnuts.com%22%2C%22%24device_id%22%3A%224ba12cff-83d2-4989-9906-ea8975f4d64f%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fbrightdata.com%2F%22%2C%22%24initial_referring_domain%22%3A%22brightdata.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fbrightdata.com%2F%22%2C%22%24initial_referring_domain%22%3A%22brightdata.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22%24user_id%22%3A%22danous%40ichestnuts.com%22%2C%22customer_id%22%3A%22hl_808393df%22%7D; Hm_lpvt_b4ae6de566ab613d22c0f8844dd852d2=1774487510; _ga_KQX3XWKR2T=GS2.1.s1774487508$o3$g1$t1774487511$j57$l0$h0; __hstc=106683420.193b4c62fe29e1a7b9a293f1b18bff6b.1774426031760.1774434720550.1774487511516.4; __hssc=106683420.1.1774487511516"
    cookie_arr = COOKIE_STR.split(";")
    COOKIES = []

    for cookie in cookie_arr:
        cookie.strip()
        kv = cookie.split("=")
        COOKIES.append({"name": str(kv[0]).strip(), "value": str(kv[1]).strip()})

    # 初始化Chrome浏览器（自动安装驱动）
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # 无头模式（不弹出浏览器窗口）
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    # 启动浏览器
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # 1. 先访问域名，才能设置Cookie
        driver.get("https://www.bright.cn/")
        time.sleep(1)

        # 2. 添加登录Cookie（关键：保持登录状态）
        for cookie in COOKIES:
            driver.add_cookie(cookie)

        # 3. 访问目标页面
        driver.get(TARGET_URL)
        print("✅ 已打开目标页面，等待JS渲染完成...")

        # 4. 等待页面加载完成（等待国家下拉框出现）
        wait = WebDriverWait(driver, 20)
        # 定位国家选择下拉框（根据页面元素定位，通用选择器）
        country_dropdown_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.uikit-dropdown__indicators svg[data-testid='dropdown-indicator']")
            )
        )
        # JS强制点击（永远不会报错）
        time.sleep(1)
        print("✅ 页面渲染完成，开始提取数据...")

        # ================ 核心：提取国家 + 城市数据 ================
        # 方案：直接获取页面渲染后的 国家下拉框所有选项 + 城市下拉框所有选项
        # 1. 点击国家下拉框，展开所有国家
        driver.execute_script("arguments[0].click();", country_dropdown_btn)
        time.sleep(1)

        # 2. 提取所有国家（适配页面下拉框元素）
        country_elements = driver.find_elements(By.CSS_SELECTOR, "div.uikit-dropdown__option, div[class*='option-item']")
        country_list = [ele.text.strip() for ele in country_elements if ele.text.strip()]
        print(f"\n===== 提取到国家列表（共{len(country_list)}个）=====")
        for country in country_list:
            print(country)

        # 3. 选择第一个国家，提取对应城市
        if country_list:
            first_country = country_elements[0]
            driver.execute_script("arguments[0].click();", first_country)
            time.sleep(2)
            print(f"\n===== 选择国家：{first_country.text}，提取城市列表 =====")

            # 定位城市下拉框，提取城市
            city_elements = driver.find_elements(By.CSS_SELECTOR,
                                                 "div.uikit-dropdown__option div[class*='MenuItemText']")
            city_list = [ele.text.strip() for ele in city_elements if ele.text.strip() and len(ele.text.strip()) > 1]

            print(f"共提取到 {len(city_list)} 个城市：")
            for city in city_list:
                print(f"- {city}")

    except Exception as e:
        print(f"❌ 出错了：{str(e)}")
        # 打印当前页面源码，用于排查
        print("\n当前页面渲染后的HTML：")
        print(driver.page_source[:2000])

    finally:
        # 关闭浏览器
        driver.quit()
