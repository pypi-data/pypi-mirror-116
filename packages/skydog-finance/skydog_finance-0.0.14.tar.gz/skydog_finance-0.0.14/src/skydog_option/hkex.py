import re
from lxml import html
import requests
import pytz
from datetime import datetime, timedelta, date
import logging


def get_option(underlying: str, strike: float, expiry: date, otype: str):
    """
    underlying: underlying security ticker
    strike: strike price
    mdate: mature date
    otype: C for Call, P for Put
    """
    if underlying[-3:].lower() == ".hk":
        underlying = underlying[:-3]
    while len(underlying) < 5:
        underlying = "0" + underlying
    url = "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx"
    request_data = {
        "action": "ajax",
        "type": "list",
        "otype": otype,
        "underlying": underlying,
        "expiry": expiry.strftime("%Y-%m-%d"),
        "strike": strike,
        "page": 1,
    }
    logging.debug(request_data)
    option_list_res = requests.post(url, data=request_data)
    if not option_list_res.text:
        logging.warn("request error for %s %s %s", underlying, strike, expiry)
        return None
    dom = html.fromstring(option_list_res.text)
    # print(option_list_res.text)
    # return
    if len(dom.xpath("//tr/td[1]/a")) == 0:
        logging.warn("no option founded for %s %s %s",
                     underlying, strike, expiry)
        return None
    href = dom.xpath("//tr/td[1]/a")[0].attrib["href"]
    if len(re.split("=|&", href)) >= 2:
        oID = re.split("=|&", href)[1]
    else:
        logging.warn("no option founded for %s %s %s",
                     underlying, strike, expiry)
        return None

    url = 'https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx?oID=%s&ucode=%s' % (
        oID, underlying)
    resp = requests.get(url)
    dom = html.fromstring(resp.text)
    ele_date_time = dom.xpath('//*[@id="detail_page"]/div[1]')[0]
    logging.debug(ele_date_time)
    ma = re.search(
        r"Last Updated:(.*?)\(", ele_date_time.text.replace("\r\n", ""))
    logging.debug("url=%s", url)
    logging.debug("group(0)=%s,group(1)=%s", ma.group(0), ma.group(1).strip())
    if not ma.group(1).strip():
        logging.warn(
            "not price-info for %s at this moment, please check later", underlying)
        return None
    dt = datetime.strptime(ma.group(1).strip(), "%d/%m/%Y %H:%M")
    detail = {}
    detail["last_trade_date"] = dt.strftime("%Y-%m-%d")
    url = (
        "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx?action=csv&type=all&oID=%s&ucode=%s"
        % (oID, underlying)
    )
    content = requests.get(url).content.decode("utf-8-sig")
    # print(content)

    for line in content.split("\r\n"):
        arr = line.split(",")
        if len(arr) >= 2:
            key = arr[0]
            val = arr[1].strip()
            # val = float(val) / 100 if val != "-" else None
            # detail[key] = val
            logging.debug("k=%s, v=%s", key, val)
            if key.find("Last Traded Price") >= 0:
                if val == "-":
                    detail["last_trade_price"] = None
                    detail["last_trade_time"] = None
                else:
                    detail["last_trade_price"] = float(val)
                    detail["last_trade_time"] = key[-9:-1]
            if val=="-" or val=="N/A" or val=="":
                val = None
            if key == "Implied Volatility (%)":
                detail["iv"] = float(val) / 100 if val else None
            if key == "Theta (Daily)":
                detail["theta"] = float(val) if val else None
            if key == "Vega":
                detail["vega"] = float(val) if val else None
            if key == "Delta (%)":
                detail["delta"] = float(val)/100 if val else None
            if key == "Bid":
                detail["bid"] = float(val) if val else None
            if key == "Ask":
                detail["ask"] = float(val) if val else None
            if key == "Volume":
                detail["volume"] = float(val) if val else None
            if key == "High":
                detail["high"] = float(val) if val else None
            if key == "Low":
                detail["low"] = float(val) if val else None
            if key == "Price Change (% Change)":
                idx = val.find("(")
                if idx > 0 and detail["last_trade_price"]:
                    detail["open"] = round(
                        detail["last_trade_price"] - float(val[:idx]), 2)
                else:
                    detail["open"] = None
    # print(detail)
    # tz = pytz.timezone("Hongkong")
    # dt = datetime.now(tz)
    # if dt.hour < 9 or (dt.hour == 9 and dt.min < 30):
    #     dt = dt - timedelta(days=1)
    # detail["last_trade_date"] = dt.strftime("%Y-%m-%d")
    #"{}-{}-{}".format(dt.year, dt.month, dt.day)
    return detail


def history(underlying: str, strike: int, expiry: str, otype: str):
    url = "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx"
    request_data = {
        "action": "ajax",
        "type": "list",
        "otype": otype,
        "underlying": underlying,
        "expiry": expiry,
        "strike": strike,
        "page": 1,
    }
    option_list_res = requests.post(
        url, data=request_data, headers={
            "referer": "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        })
    dom = html.fromstring(option_list_res.text)
    href = dom.xpath("//tr/td[1]/a")[0].attrib["href"]
    oID = re.split("=|&", href)[1]

    # historical data: underlying_price vs option_price
    historical_data = {}
    for data_type in range(1, 4):
        url = (
            "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx?action=csv&type=%d&oID=%s&ucode=%s"
            % (data_type, oID, underlying)
        )
        content = requests.get(url).content.decode("utf-8-sig")
        first_empty_line_found = False
        header_line_found = False
        for line in content.split("\r\n"):
            if line == "":
                first_empty_line_found = True
                continue
            if not first_empty_line_found:
                continue
            if first_empty_line_found and not header_line_found:
                header_line_found = True
                headers = line.split(",")
                continue

            data_arr = line.split(",")
            trade_date = data_arr[0]
            if trade_date not in historical_data.keys():
                historical_data[trade_date] = {}
            if len(data_arr) != len(headers):
                # print(data_arr)
                break
            for i, attr_name in enumerate(headers):
                historical_data[trade_date][attr_name] = data_arr[i]

    historical_array = []
    for trade_date in historical_data:
        # print(historical_data[trade_date])
        historical_array.append(historical_data[trade_date])

    import pandas as pd

    df = pd.DataFrame(historical_array)
    print(df)
    return df

