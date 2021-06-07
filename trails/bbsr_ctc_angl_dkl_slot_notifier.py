import requests
from datetime import datetime
import schedule
import time

BASE_COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
DISTRICTS_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
all_odisha_districts = [446, 457, 445]
# 446 Khurda 457 Cuttack 458 Dhenkanal 571 Angul
# all_odisha_districts = [445, 448, 447, 472, 454, 468, 457, 473, 458, 467, 449, 459, 460, 474, 464, 450, 461, 455, 446,
#                         451, 469, 456, 470, 462, 465, 463, 471, 452, 466, 453]
is_for_eighteen_plus = True
is_for_second_dosage = True
telegram_api_url = "https://api.telegram.org/bot1832543686:AAFgdgcpIOkNeIBWe07jxwVG5uNW1FJX5N4/sendMessage?chat_id=@__group_id__&parse_mode=HTML&text="
telegram_group_id = "bbsr_ctc_dkl_angl_covid"
# dev starts
# telegram_api_url = "https://api.telegram.org/bot1853183766:AAGzzexG-1c_use4m0G_9IrV0B9Lq53Bkx0/sendMessage?chat_id=@__group_id__&parse_mode=HTML&text="
# telegram_group_id = "odisha_covishild_18_plus"
# dev ends here
last_message = ""
all_districts = [None] * 100

last_send_messages = [None] * len(all_odisha_districts)
district_vs_stock = [None] * len(all_odisha_districts)


def fetch_data_from_cowin(index, district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = BASE_COWIN_URL + query_params
    print(final_url)
    response = requests.get(final_url)
    # print(response.text)
    try:
        extract_availability_data(response, index, district_id)
    except Exception as e:
        print(e)


def fetch_data_for_me():
    for index, district_id in enumerate(all_odisha_districts):
        fetch_data_from_cowin(index, district_id)


def extract_availability_data(response, index, district_id):
    response_json = response.json()
    message = ""

    total_slots = 0

    for center in response_json["centers"]:
        for session in center["sessions"]:
            if is_for_eighteen_plus:
                if session["min_age_limit"] == 18 and session["available_capacity_dose1"] > 0:
                    print(center["center_id"], center["name"])
                    print("Available Dosage {}".format(session["available_capacity_dose1"]) + " For Age {}".format(
                        session["min_age_limit"]))
                    total_slots = session["available_capacity"]
                    message += build_message(center, session)
            else:
                if session["min_age_limit"] > 18 and session["available_capacity_dose1"] > 0:
                    message += build_message(center, session)

    # print(message)
    global last_message
    last_message = last_send_messages[index]
    if last_message != message:
        print("Last message is not equal to message {} at {}".format(last_message, datetime.now().strftime("%H:%M")))
        last_send_messages[index] = message
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
    forty_five_plus = "4️⃣5️⃣➕"
    eighteen_plus = "1️⃣8️⃣➕"
    age = session["min_age_limit"]
    age_text = eighteen_plus if age == 18 else forty_five_plus
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
                age_text,
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
    final_telegram_url = telegram_api_url.replace("__group_id__", telegram_group_id)
    final_telegram_url_with_message = final_telegram_url + message
    response = requests.get(final_telegram_url_with_message)
    print(response.text)


def fetchDistrits(state_id):
    json_string = {
        "districts": [{"district_id": 445, "district_name": "Angul"},
                      {"district_id": 448, "district_name": "Balangir"},
                      {"district_id": 447, "district_name": "Balasore"},
                      {"district_id": 472, "district_name": "Bargarh"},
                      {"district_id": 454, "district_name": "Bhadrak"},
                      {"district_id": 468, "district_name": "Boudh"},
                      {"district_id": 457, "district_name": "Cuttack"},
                      {"district_id": 473, "district_name": "Deogarh"},
                      {"district_id": 458, "district_name": "Dhenkanal"},
                      {"district_id": 467, "district_name": "Gajapati"},
                      {"district_id": 449, "district_name": "Ganjam"},
                      {"district_id": 459, "district_name": "Jagatsinghpur"},
                      {"district_id": 460, "district_name": "Jajpur"},
                      {"district_id": 474, "district_name": "Jharsuguda"},
                      {"district_id": 464, "district_name": "Kalahandi"},
                      {"district_id": 450, "district_name": "Kandhamal"},
                      {"district_id": 461, "district_name": "Kendrapara"},
                      {"district_id": 455, "district_name": "Kendujhar"},
                      {"district_id": 446, "district_name": "Khurda"},
                      {"district_id": 451, "district_name": "Koraput"},
                      {"district_id": 469, "district_name": "Malkangiri"},
                      {"district_id": 456, "district_name": "Mayurbhanj"},
                      {"district_id": 470, "district_name": "Nabarangpur"},
                      {"district_id": 462, "district_name": "Nayagarh"},
                      {"district_id": 465, "district_name": "Nuapada"},
                      {"district_id": 463, "district_name": "Puri"},
                      {"district_id": 471, "district_name": "Rayagada"},
                      {"district_id": 452, "district_name": "Sambalpur"},
                      {"district_id": 466, "district_name": "Subarnapur"},
                      {"district_id": 453, "district_name": "Sundargarh"}]}
    for districts in json_string.values():
        for i, district in enumerate(districts):
            all_districts[i] = district["district_id"]
            fetch_data_from_cowin(index=i, district_id=district["district_id"])


if __name__ == "__main__":
    schedule.every(3).seconds.do(lambda: fetch_data_for_me())
    while True:
        schedule.run_pending()
        time.sleep(5)
