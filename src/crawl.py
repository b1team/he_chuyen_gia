# Đừng chạy tất cả các ô, ấn lần lượt đi :v
import json
import time
# install chromium, its driver, and selenium
# !apt install chromium-chromedriver
# !pip install selenium
# set options to be headless, ..
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BSoup

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# open it, go to a website, and get results
wd = webdriver.Chrome('driver/chromedriver', options=options)


def get_rating():
    wd.get("http://fhub.vn/rating")
    element = wd.find_element(By.CSS_SELECTOR, '#all_stocks')
    wd.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    bs_obj = BSoup(wd.page_source, 'html.parser')
    data_dic = {}

    table = bs_obj.find(id='table_rating').find('tbody')
    for td in table.find_all('tr'):
        info = {}
        info_ls = []
        for data in td.find_all('td'):
            info_ls.append(data.text)

        info['stock_code'] = info_ls[1]
        info['RS_rating'] = info_ls[3]
        info['AD_rating'] = info_ls[4].strip()
        info['EPS_rating'] = info_ls[5]
        info['SMR_rating'] = info_ls[6].strip()
        info['composite_rating'] = info_ls[7]

        data_dic[info['stock_code']] = info

    with open('data.json', 'w') as f:
        f.write(json.dumps(data_dic, indent=4))

    return data_dic


def set_data(code: str, dict_data: dict):
    print(code)
    wd.get(f"https://finance.vietstock.vn/vi/cophieu/{code}"
           )  # Thay SSI bằng cái mã khác
    time.sleep(0.3)
    soup = BSoup(wd.page_source, 'html.parser')
    # Giá tiền
    tien_cao_homnay = soup.find(
        class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50").find_all(
            'p')[1].find('b').get_text()
    tien_thap_homnay = soup.find(
        class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50").find_all(
            'p')[2].find('b').get_text()

    tien_cao_52T = soup.find_all(
        class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50")[1].find_all(
            'p')[2].find('b').get_text()
    tien_thap_52T = soup.find_all(
        class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50")[1].find_all(
            'p')[3].find('b').get_text()

    dict_data['tien_cao_homnay'] = tien_cao_homnay
    dict_data['tien_thap_homnay'] = tien_thap_homnay
    dict_data['tien_thap_52T'] = tien_thap_52T
    dict_data['tien_cao_52T'] = tien_cao_52T
    # Doanh thu
    doanh_thu_quy_gan_nhat = soup.find(
        id='table-0').find_all('tr')[1].find_all('td')[-1].get_text()
    doanh_thu_quy_gan_nhat_lien_ke = soup.find(
        id='table-0').find_all('tr')[1].find_all('td')[-2].get_text()

    dict_data['doanh_thu_quy_gan_nhat'] = doanh_thu_quy_gan_nhat
    dict_data[
        'doanh_thu_quy_gan_nhat_lien_ke'] = doanh_thu_quy_gan_nhat_lien_ke

    # EPS
    EPS_hom_nay = soup.find(
        class_='col-xs-12 col-sm-4 col-md-4 col-c-last').find('b').get_text()
    EPS_Q_gan_nhat = soup.find(
        id='table-2').find_all('tr')[1].find_all('td')[-1].get_text()
    EPS_Q_gan_nhat_lien_ke = soup.find(
        id='table-2').find_all('tr')[1].find_all('td')[-2].get_text()

    dict_data['EPS_hom_nay'] = EPS_hom_nay
    dict_data['EPS_Q_gan_nhat'] = EPS_Q_gan_nhat
    dict_data['EPS_Q_gan_nhat_lien_ke'] = EPS_Q_gan_nhat_lien_ke

    element = wd.find_element(
        By.CSS_SELECTOR,
        "#finance-content > div > div > div:nth-child(1) > div.col-xs-14.col-sm-8.m-b.text-right > div:nth-child(2)"
    )
    wd.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    soup = BSoup(wd.page_source, 'html.parser')

    EPS_Q_gan_nhat_nam_truoc = soup.find(
        id='table-2').find_all('tr')[1].find_all('td')[-1].get_text()
    EPS_Q_gan_nhat_lien_ke_nam_truoc = soup.find(
        id='table-2').find_all('tr')[1].find_all('td')[-2].get_text()

    dict_data['EPS_Q_gan_nhat_nam_truoc'] = EPS_Q_gan_nhat_nam_truoc
    dict_data[
        'EPS_Q_gan_nhat_lien_ke_nam_truoc'] = EPS_Q_gan_nhat_lien_ke_nam_truoc

    # SAU click năm
    element = wd.find_element(
        By.XPATH, '//*[@id="finance-content"]/div/div/div[1]/div[1]/a[2]')
    wd.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    soup = BSoup(wd.page_source, 'html.parser')

    LNST_nam_gan_nhat = soup.find(
        id='table-0').find_all('tr')[4].find_all('td')[-1].get_text()
    LNST_nam_truoc = soup.find(
        id='table-0').find_all('tr')[4].find_all('td')[-2].get_text()
    LNST_nam_truoc_nua = soup.find(
        id='table-0').find_all('tr')[4].find_all('td')[-3].get_text()

    dict_data['LNST_nam_gan_nhat'] = LNST_nam_gan_nhat
    dict_data['LNST_nam_truoc'] = LNST_nam_truoc
    dict_data['LNST_nam_truoc_nua'] = LNST_nam_truoc_nua

    ROE_nam_gan_nhat = soup.find(
        id='table-2').find_all('tr')[5].find_all('td')[-1].get_text()
    ROE_nam_gan_nhat_lien_ke = soup.find(
        id='table-2').find_all('tr')[5].find_all('td')[-2].get_text()

    dict_data['ROE_nam_gan_nhat'] = ROE_nam_gan_nhat
    dict_data['ROE_nam_gan_nhat_lien_ke'] = ROE_nam_gan_nhat_lien_ke

    return dict_data


def solve(stock_code: str):
    data_dic = get_rating()
    stock = data_dic[stock_code]
    print(stock)
    while True:
        try:
            data = set_data(stock_code, stock)
            break
        except Exception as ex:
            print(ex)
            pass

    return data


if __name__ == '__main__':
    # get_rating data
    data = solve('SSI')
    print(data)
"""
data = {
    "stock_code":"SSI",
    "RS_rating":"92",
    "AD_rating":"A+",
    "EPS_rating":"27",
    "SMR_rating":"A",
    "composite_rating":"93",
    "tien_cao_homnay":"45,050",
    "tien_thap_homnay":"43,200",
    "tien_thap_52T":"20,000",
    "tien_cao_52T":"55,900",
    "doanh_thu_quy_gan_nhat":"7,292,477",
    "doanh_thu_quy_gan_nhat_lien_ke":"4,366,801",
    "EPS_hom_nay":"1,955",
    "EPS_Q_gan_nhat":"3,651.00",
    "EPS_Q_gan_nhat_lien_ke":"2,178.00",
    "EPS_Q_gan_nhat_nam_truoc":"2,372.00",
    "EPS_Q_gan_nhat_lien_ke_nam_truoc":"1,826.00",
    "LNST_nam_gan_nhat":"2,671,974",
    "LNST_nam_truoc":"1,255,932",
    "LNST_nam_truoc_nua":"907,097",
    "ROE_nam_gan_nhat":"22.49",
    "ROE_nam_gan_nhat_lien_ke":"13.05"
 }
"""
