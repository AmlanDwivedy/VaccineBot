import requests
from datetime import datetime
import schedule
import time

BASE_COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
odisha_khurda_cuttack_angul_dkl_ids = [446, 457, 445, 458]
is_for_eighteen_plus = True
telegram_api_url = "https://api.telegram.org/bot1856792170:AAFWhmxfVsHEpaSlaQlXKj6adNHPK54GG5Q/sendMessage?chat_id=@__group_id__&text="
telegram_group_id = "odisha_vovaxine_18_plus"
last_message = ""


def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = BASE_COWIN_URL + query_params
    print(final_url)
    response = requests.get(final_url)
    # print(response.text)
    try:
        extract_availability_data(response)
    except Exception as e:
        print(e)


def fetch_data_for_me():
    for district_id in odisha_khurda_cuttack_angul_dkl_ids:
        fetch_data_from_cowin(district_id)


def extract_availability_data(response):
    response_json = response.json()
    message = ""
    i = 0
    for center in response_json["centers"]:
        i = i + 1
        if i > 5:
            continue
        for session in center["sessions"]:
            if session["vaccine"] != "COVAXIN":
                continue
            if is_for_eighteen_plus:
                if session["min_age_limit"] == 18 and session["available_capacity_dose1"] > 0:
                    print(center["center_id"], center["name"])
                    print("Available Dosage {}".format(session["available_capacity_dose1"]) + " For Age {}".format(
                        session["min_age_limit"]))
                    message += build_message(center, session)
            else:
                if session["min_age_limit"] > 18 and session["available_capacity_dose1"] > 0:
                    message += build_message(center, session)

    global last_message
    if last_message != message:
        print("Last message is not equal to message {} at {}".format(last_message,datetime.now().strftime("%H:%M")))
        last_message = message
    else:
        print("Last message is  equal to message at {}".format(datetime.now().strftime("%H:%M")))
        return
    # print(message)
    if len(message) > 0:
        message += "\nYou can join the Odisha Covishield 18+ channel https://t.me/odisha_covishild_18_plus. And for feedback use this group https://t.me/OdishaVaccineFeedback".format(
            now.strftime("%H:%m"))
        send_telegram_message(message)
    else:
        # send_telegram_message("No slots available now. Last checked at {}. You can join the Odisha Covishield 18+ channel https://t.me/odisha_covishild_18_plus. And for feedback use this group https://t.me/OdishaVaccineFeedback".format(now.strftime("%H:%m")))
        print("No Slots available at {}".format(datetime.now().strftime("%H:%M")))


def build_message(center, session):
    return "{} ,{} , {} " \
           "\nAge: {} " \
           "\n{} " \
           "\n{}" \
           "\n{}"\
           "\nQuantity {} [D1:{} ,D2:{}] \n \n " \
           "...." \
           "\n " \
        .format(center["name"]
                , center["district_name"]
                , center["pincode"]
                , session["min_age_limit"],
                session["vaccine"],
                center["fee_type"],
                session["date"],
                session["available_capacity"],
                session[
                    "available_capacity_dose1"],
                session[
                    "available_capacity_dose2"])


def send_telegram_message(message):
    final_telegram_url = telegram_api_url.replace("__group_id__", telegram_group_id)
    final_telegram_url_with_message = final_telegram_url + message
    response = requests.get(final_telegram_url_with_message)
    print(response.text)


if __name__ == "__main__":
    schedule.every(5).seconds.do(lambda: fetch_data_for_me())
    while True:
        schedule.run_pending()
        time.sleep(5)
