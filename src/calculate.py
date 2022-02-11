data = {
    "stock_code": "SSI",
    "RS_rating": "92",
    "AD_rating": "A+",
    "EPS_rating": "27",
    "SMR_rating": "A",
    "composite_rating": "93",
    "tien_cao_homnay": "45,050",
    "tien_thap_homnay": "43,200",
    "tien_thap_52T": "20,000",
    "tien_cao_52T": "55,900",
    "doanh_thu_quy_gan_nhat": "7,292,477",
    "doanh_thu_quy_gan_nhat_lien_ke": "4,366,801",
    "EPS_hom_nay": "1,955",
    "EPS_Q_gan_nhat": "3,651.00",
    "EPS_Q_gan_nhat_lien_ke": "2,178.00",
    "EPS_Q_gan_nhat_nam_truoc": "2,372.00",
    "EPS_Q_gan_nhat_lien_ke_nam_truoc": "1,826.00",
    "LNST_nam_gan_nhat": "2,671,974",
    "LNST_nam_truoc": "1,255,932",
    "LNST_nam_truoc_nua": "907,097",
    "ROE_nam_gan_nhat": "22.49",
    "ROE_nam_gan_nhat_lien_ke": "13.05",
}

assign = {
    1: range(0, 25),
    2: range(25, 50),
    3: range(50, 75),
    4: range(75, 100),
    5: range(100, 500),
}


def format_value(data: dict) -> dict:
    for key, value in data.items():
        try:
            data[key] = float(value.replace(",", ""))
        except Exception:
            pass

    return data


def calculate_index(data: dict) -> dict:
    data = format_value(data)
    EPS = data["EPS_Q_gan_nhat"] / data["EPS_Q_gan_nhat_nam_truoc"]
    LNST = data["LNST_nam_gan_nhat"] / data["LNST_nam_truoc"]
    ROE = data["ROE_nam_gan_nhat"] / data["ROE_nam_gan_nhat_lien_ke"]
    EPS_rating = data["EPS_rating"]
    AD_rating = data["AD_rating"]
    RS_rating = data["RS_rating"]
    SMR_rating = data["SMR_rating"]
    PRICE = data["tien_cao_homnay"] / data["tien_cao_52T"]
    REVENUE = data["doanh_thu_quy_gan_nhat"] / data["doanh_thu_quy_gan_nhat_lien_ke"]

    return {
        "EPS": (EPS - 1) * 100,
        "LNST": (LNST - 1) * 100,
        "ROE": (ROE - 1) * 100,
        "EPS_rating": EPS_rating,
        "AD_rating": AD_rating,
        "RS_rating": RS_rating,
        "SMR_rating": SMR_rating,
        "PRICE": (PRICE - 1) * 100,
        "REVENUE": (REVENUE - 1) * 100,
    }
