import requests
from datetime import datetime
import schedule
import time

BASE_COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
odisha_khurda_cuttack_angul_dkl_ids = [446]
is_for_eighteen_plus = False
is_for_second_dosage = True
telegram_api_url = "https://api.telegram.org/bot1832543686:AAFgdgcpIOkNeIBWe07jxwVG5uNW1FJX5N4/sendMessage?chat_id=@__group_id__&parse_mode=HTML&text="
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
        if center["name"] == "APOLLO HOSPITALS BBSR CVC":
            ss = center["sessions"]
            len(ss)
            # print("Center:{}".format(center))
            # print("Sessions: {}".format(center["sessions"]))
            for s in ss:
                if is_for_second_dosage and s["min_age_limit"] == 18:
                    message += build_message(center, s)
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
        print("Last message is not equal to message {} at {}".format(last_message, datetime.now().strftime("%H:%M")))
        last_message = message
    else:
        print("Last message is  equal to message at {}".format(datetime.now().strftime("%H:%M")))
        return
    # print(message)
    if len(message) > 0:
        send_telegram_message(message)
    else:
        print("No Slots available at {}".format(datetime.now().strftime("%H:%M")))


def build_message(center, session):
    vaccine_fee = ""
    try:
        fees = center["vaccine_fees"]
        for fee in fees:
            vaccine_fee += fee["vaccine"] + ": ₹" + fee["fee"]
    except  Exception as e:
        print(e)

    date_time_string = session["date"]
    date_time_obj = datetime.strptime(date_time_string, "%d-%m-%Y")
    date_text = date_time_obj.strftime("%d %b, %Y")
    text = "District+: <b>{}</b>\n" \
           "Age:<b>{}</b>\n" \
           "Pincode:<b>{}</b>\n" \
           "📍 <b><i>{}</i></b> 📍" \
           "\nDate: <b>{}</b>" \
           "\n💉Vaccine: <code><b>{}</b></code>" \
           "\nFee: <b>{} " \
           "\n{}</b>" \
           "\n<strong>Total {} Slots <code>[1st Dosage:{},2nd Dosage:{}]</code></strong>" \
           "\n\n" \
        .format(center["district_name"],
                session["min_age_limit"],
                center["pincode"],
                center["name"] + ", " + center["address"],
                date_text,
                session["vaccine"],
                center["fee_type"],
                vaccine_fee,
                session["available_capacity"],
                session["available_capacity_dose1"],
                session["available_capacity_dose2"])
    print(text)
    return text


def send_telegram_message(message):
    # if True:
    #     return
    final_telegram_url = telegram_api_url.replace("__group_id__", group_id_forty_five)
    final_telegram_url_with_message = final_telegram_url + message
    response = requests.get(final_telegram_url_with_message)
    print(response.text)


if __name__ == "__main__":
    schedule.every(3).seconds.do(lambda: fetch_data_for_me())
    while True:
        schedule.run_pending()
        time.sleep(2)
