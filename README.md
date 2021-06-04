# VaccineBot
Testing out vaccine bot for telegram


To find the states hit this api 
https://cdn-api.co-vin.in/api/v2/admin/location/states
parse the json. Its something like `{"state_id":16,"state_name":"Karnataka"}`

To find district code 
https://cdn-api.co-vin.in/api/v2/admin/location/districts/16
It will give response something like `{"district_id":270,"district_name":"Bagalkot"}`

Then your district code is **270** Same way you can find multiple distcrict codes
 In cowin_telegram_bot.py change the `odisha_khurda_cuttack_angul_dkl_ids` array with appropricate values

Open Telegram--> Serach for `@BotFather`--> Type `/newbot` 
Give a name to your bot, bot is created and you will be provided with an API Key

Then create a Telegram Group and add this bot to that

Thats it. Done.