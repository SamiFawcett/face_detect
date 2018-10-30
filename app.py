import requests
import urllib
import json
from io import BytesIO
from PIL import Image, ImageDraw

face = requests.get("https://randomuser.me/api")
face_results = face.json()
img_url = face_results["results"][0]["picture"]["large"]
url = "https://api-us.faceplusplus.com/facepp/v3/detect"
params = {
			'api_key': "k8Lnv0BMRcOXpSL_7cdwbG7hZvE0OiID",	
			'api_secret': "aiSUoZtV3TAiH3dVQkNHngLnqgzpL44k",
			'image_url': img_url
		}
	
response = requests.post(url, params)
results = response.json()
face_results = results["faces"]
face_token = face_results[0]["face_token"]

url = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
params = {
			'api_key': "k8Lnv0BMRcOXpSL_7cdwbG7hZvE0OiID",
			'api_secret': "aiSUoZtV3TAiH3dVQkNHngLnqgzpL44k",
			'face_tokens': face_token,
			'return_landmark': 2,
			'return_attributes': 'emotion,beauty,mouthstatus'
		}
response = requests.post(url, params)
results = response.json()
image = requests.get(img_url)
background = Image.new("RGB", (512, 512), "black")
im = Image.open(BytesIO(image.content))
background.paste(Image.open(BytesIO(image.content)), (100, 100))	
draw = ImageDraw.Draw(im)
r = 5
for coord in results["faces"][0]["landmark"]:
	x = results["faces"][0]["landmark"][coord]["x"]
	y = results["faces"][0]["landmark"][coord]["y"]
	draw.point((x,y))
width, height = background.size
max_confidence = results["faces"][0]["attributes"]["emotion"]["happiness"]
#default emotion
emotion_selected = 'happiness'
for emotion in results["faces"][0]["attributes"]["emotion"]:
	if(results["faces"][0]["attributes"]["emotion"][emotion] > max_confidence):
		emotion_selected = emotion
print(results["faces"][0]["attributes"])
ImageDraw.Draw(background).text((width//2, height - 50), "Emotion: " + emotion_selected ,fill="white")
ImageDraw.Draw(background).text((width//2 - width//3, height - 70), "Beauty Score: " + str(results["faces"][0]["attributes"]["beauty"]) ,fill="white")
background.paste(im, (300, 100))
background.show()
