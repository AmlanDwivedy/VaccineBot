import requests
from datetime import datetime
import schedule
import time
import schedule
import time

BASE_COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
odisha_khurda_cuttack_angul_dkl_ids = [294]
is_for_eighteen_plus = True
telegram_api_url = "https://api.telegram.org/bot1832543686:AAFgdgcpIOkNeIBWe07jxwVG5uNW1FJX5N4/sendMessage?chat_id=@__group_id__&text="
group_id_forty_five = "bbsr_ctc_dkl_angl_covid"
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
    for center in response_json["centers"]:
        for session in center["sessions"]:
            if is_for_eighteen_plus:
                if session["min_age_limit"] == 18 and session["available_capacity_dose1"] > 0:
                    print(center["center_id"], center["name"])
                    print("Available Dosage {}".format(session["available_capacity_dose1"]) + " For Age {}".format(
                        session["min_age_limit"]))
                    message += build_message(center, session)

            else:
                if session["min_age_limit"] > 18 and session["available_capacity_dose1"] > 0:
                    if session["vaccine"] != "COVISHIELD":
                        continue
                    message += build_message(center, session)
    # print(message)
    global last_message
    if last_message != message:
        print("Last message is not equal to message")
        last_message = message
    else:
        print("Last message is  equal to message")
        return
    if len(message) > 0:
        message += "\nYou can join the Odisha Covishield 18+ channel https://t.me/odisha_covishild_18_plus. And for feedback use this group https://t.me/OdishaVaccineFeedback. Share it with more people".format(
            now.strftime("%H:%m"))
        send_telegram_message(message)
    else:
        print("No Slots available at {}".format(datetime.now().strftime("%H:%M")))
    #     send_telegram_message(
    #         "No slots available now. Last checked at {}. You can join the Odisha Covaxine 18+ channel https://t.me/odisha_vovaxine_18_plus".format(
    #             datetime.now().strftime("%H:%m")))


def build_message(center, session):
    return "{} ,{} , {} " \
           "\nAge: {} " \
           "\n{} " \
           "\n{}" \
           "\nQuantity {} [D1:{} ,D2:{}] \n \n " \
           "..............." \
           "\n " \
        .format(center["name"]
                , center["district_name"]
                , center["pincode"]
                , session["min_age_limit"],
                session["vaccine"],
                center["fee_type"],
                session["available_capacity"],
                session[
                    "available_capacity_dose1"],
                session[
                    "available_capacity_dose2"])


def send_telegram_message(message):
    final_telegram_url = telegram_api_url.replace("__group_id__", group_id_forty_five)
    final_telegram_url_with_message = final_telegram_url + message
    response = requests.get(final_telegram_url_with_message)
    print(response.text)


if __name__ == "__main__":
    schedule.every(3).seconds.do(lambda: fetch_data_for_me())
    while True:
        schedule.run_pending()
        time.sleep(2)
