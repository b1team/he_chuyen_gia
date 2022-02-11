import json
import logging
import time

from bs4 import BeautifulSoup as BSoup
from retry.api import retry_call
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# open it, go to a website, and get results
wd = webdriver.Chrome(
    service=Service(ChromeDriverManager(print_first_line=False).install()),
    options=options,
)


def get_rating(use_cache=True, cache_file="cache.json"):
    logger.info("CRAWLING RATING")
    if use_cache:
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
            logger.info("CRAWLING RATING FROM CACHE FILE SUCCESS")
            return data
        except FileNotFoundError:
            logger.warning("CACHE FILE NOT FOUND")
            pass

    wd.get("http://fhub.vn/rating")
    element = wd.find_element(By.CSS_SELECTOR, "#all_stocks")
    wd.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    bs_obj = BSoup(wd.page_source, "html.parser")
    data_dic = {}

    table = bs_obj.find(id="table_rating").find("tbody")
    for td in table.find_all("tr"):
        info = {}
        info_ls = []
        for data in td.find_all("td"):
            info_ls.append(data.text)

        info["stock_code"] = info_ls[1]
        info["RS_rating"] = info_ls[3]
        info["AD_rating"] = info_ls[4].strip()
        info["EPS_rating"] = info_ls[5]
        info["SMR_rating"] = info_ls[6].strip()
        info["composite_rating"] = info_ls[7]

        data_dic[info["stock_code"]] = info

    with open("data.json", "w") as f:
        f.write(json.dumps(data_dic, indent=4))
        logger.info("CACHING RATING")
    logger.info("CRAWLING RATING DONE")

    return data_dic


def get_revenue_data(stock_code: str):
    logger.info("CRAWLING REVENUE DATA OF %s", stock_code)
    dict_data = dict()
    wd.get(f"https://finance.vietstock.vn/vi/cophieu/{stock_code}")
    time.sleep(0.3)
    soup = BSoup(wd.page_source, "html.parser")
    # Giá tiền
    tien_cao_homnay = (
        soup.find(class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50")
        .find_all("p")[1]
        .find("b")
        .get_text()
    )
    tien_thap_homnay = (
        soup.find(class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50")
        .find_all("p")[2]
        .find("b")
        .get_text()
    )

    tien_cao_52T = (
        soup.find_all(class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50")[1]
        .find_all("p")[2]
        .find("b")
        .get_text()
    )
    tien_thap_52T = (
        soup.find_all(class_="col-xs-12 col-sm-5 col-md-5 col-c bg-50")[1]
        .find_all("p")[3]
        .find("b")
        .get_text()
    )

    dict_data["tien_cao_homnay"] = tien_cao_homnay
    dict_data["tien_thap_homnay"] = tien_thap_homnay
    dict_data["tien_thap_52T"] = tien_thap_52T
    dict_data["tien_cao_52T"] = tien_cao_52T
    # Doanh thu
    doanh_thu_quy_gan_nhat = (
        soup.find(id="table-0").find_all("tr")[1].find_all("td")[-1].get_text()
    )
    doanh_thu_quy_gan_nhat_lien_ke = (
        soup.find(id="table-0").find_all("tr")[1].find_all("td")[-2].get_text()
    )

    dict_data["doanh_thu_quy_gan_nhat"] = doanh_thu_quy_gan_nhat
    dict_data["doanh_thu_quy_gan_nhat_lien_ke"] = doanh_thu_quy_gan_nhat_lien_ke

    # EPS
    EPS_hom_nay = (
        soup.find(class_="col-xs-12 col-sm-4 col-md-4 col-c-last").find("b").get_text()
    )
    EPS_Q_gan_nhat = (
        soup.find(id="table-2").find_all("tr")[1].find_all("td")[-1].get_text()
    )
    EPS_Q_gan_nhat_lien_ke = (
        soup.find(id="table-2").find_all("tr")[1].find_all("td")[-2].get_text()
    )

    dict_data["EPS_hom_nay"] = EPS_hom_nay
    dict_data["EPS_Q_gan_nhat"] = EPS_Q_gan_nhat
    dict_data["EPS_Q_gan_nhat_lien_ke"] = EPS_Q_gan_nhat_lien_ke

    element = wd.find_element(
        By.CSS_SELECTOR,
        "#finance-content > div > div > div:nth-child(1) > div.col-xs-14.col-sm-8.m-b.text-right > div:nth-child(2)",
    )
    wd.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    soup = BSoup(wd.page_source, "html.parser")

    EPS_Q_gan_nhat_nam_truoc = (
        soup.find(id="table-2").find_all("tr")[1].find_all("td")[-1].get_text()
    )
    EPS_Q_gan_nhat_lien_ke_nam_truoc = (
        soup.find(id="table-2").find_all("tr")[1].find_all("td")[-2].get_text()
    )

    dict_data["EPS_Q_gan_nhat_nam_truoc"] = EPS_Q_gan_nhat_nam_truoc
    dict_data["EPS_Q_gan_nhat_lien_ke_nam_truoc"] = EPS_Q_gan_nhat_lien_ke_nam_truoc

    # SAU click năm
    element = wd.find_element(
        By.XPATH, '//*[@id="finance-content"]/div/div/div[1]/div[1]/a[2]'
    )
    wd.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    soup = BSoup(wd.page_source, "html.parser")

    LNST_nam_gan_nhat = (
        soup.find(id="table-0").find_all("tr")[4].find_all("td")[-1].get_text()
    )
    LNST_nam_truoc = (
        soup.find(id="table-0").find_all("tr")[4].find_all("td")[-2].get_text()
    )
    LNST_nam_truoc_nua = (
        soup.find(id="table-0").find_all("tr")[4].find_all("td")[-3].get_text()
    )

    dict_data["LNST_nam_gan_nhat"] = LNST_nam_gan_nhat
    dict_data["LNST_nam_truoc"] = LNST_nam_truoc
    dict_data["LNST_nam_truoc_nua"] = LNST_nam_truoc_nua

    ROE_nam_gan_nhat = (
        soup.find(id="table-2").find_all("tr")[5].find_all("td")[-1].get_text()
    )
    ROE_nam_gan_nhat_lien_ke = (
        soup.find(id="table-2").find_all("tr")[5].find_all("td")[-2].get_text()
    )

    dict_data["ROE_nam_gan_nhat"] = ROE_nam_gan_nhat
    dict_data["ROE_nam_gan_nhat_lien_ke"] = ROE_nam_gan_nhat_lien_ke
    logger.info(
        "CRAWL REVENUE DATA OF STOCK %s FINISHED. DATA: %s", stock_code, dict_data
    )

    return dict_data


def solve(
    stock_code: str, cache_file: str = "data.json", tries: int = 3, delay: float = 5
):
    all_rating_data = retry_call(
        f=get_rating,
        fkwargs={"cache_file": cache_file},
        tries=tries,
        delay=delay,
        logger=logger,
    )
    stock_rating_data = all_rating_data.get(stock_code, dict())
    revenue_data = retry_call(
        f=get_revenue_data,
        fkwargs={"stock_code": stock_code},
        tries=tries,
        delay=tries,
        logger=logger,
    )
    data = {**stock_rating_data, **revenue_data}
    return data
