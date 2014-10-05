import fitbit
import ConfigParser
import forecastio
import requests
#Load Settings
parser = ConfigParser.SafeConfigParser()
parser.read('config.ini')
con_key = parser.get('Login Parameters', 'C_KEY')
con_sec = parser.get('Login Parameters', 'C_SECRET')
client_key = parser.get('Login Parameters','CL_KEY')
client_secret = parser.get('Login Parameters','CL_SECRET')
user = parser.get('Login Parameters', 'USER_ID')
weather_api = parser.get('Other API Keys', 'WEATHER')
yo_api = parser.get('Other API Keys','YO')
#open file which contains last steps amount
steps_file = open('steps.txt', 'r+')
previous_steps = int(steps_file.read())
steps_file.close()
#WEATHER
def get_weather():
	forecast = forecastio.load_forecast(weather_api, 42.3591473,-71.09677909999999)
	weather_now = forecast.currently().summary
	return weather_now
#SET UP YO
def post_yo():
	requests.post("https://api.justyo.co/yoall/", data={'api_token': yo_api, 'username': 'SARAHACKMIT'})
#set up the fitbit api here and grab activity data
#Set up unathorized client
unauth_client = fitbit.Fitbit(con_key,con_sec, system='en_US')
# You'll have to gather the user keys on your own, or try ./fitbit/gather_keys_cli.py <con_key> <con_sec> for development
fit = fitbit.Fitbit(con_key, con_sec, resource_owner_key=client_key, resource_owner_secret=client_secret)
current_activity = fit.recent_activities(user_id=user, qualifier='')
#get the current activity
steps = current_activity['lifetime']['total']['steps']
weather = get_weather()
print weather
#putzing around: essentially I'd want this to send a Yo if it was raining, but today it's not raining!!!
if weather == 'Partly Cloudy' and steps >= previous_steps + 100:
	print "You're moving and the weather is bad so i'll warn ya with a Yo"
	post_yo()
else:
	print "You haven't really moved so you're probably not going outside...."

save_steps = str(steps)
steps_file = open('steps.txt', 'r+')
steps_file.write(save_steps)
steps_file.close()