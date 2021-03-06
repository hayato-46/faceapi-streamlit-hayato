import streamlit as st
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

st.title('年齢判別App')

st.write('Display Image')

imgs = Image.open('image.jpg')
st.image(imgs, use_column_width=True)




"""
##  機能
写真から顔を判別し、年齢・性別を判定します。
- 男性 male
- 女性 female

###  注意事項
- 人間のみ判別できます。
- 角度により判別できない可能性があります。

"""


subscription_key = '0de3e5b25b4642c699b437b6917e41a6'
assert subscription_key

face_api_url = 'https://20210301hayatoapp.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
        
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
        'detectionModel': 'detection_01',
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses',
        'returnFaceId': 'true'
    }

    res = requests.post(face_api_url, params=params,headers=headers, data=binary_img)
    results = res.json()
    

    for result in results:
        rect = result['faceRectangle']
        size = int(rect['width']/3)
        fnt = ImageFont.truetype('arial.ttf', size=size)
        gender = result['faceAttributes']['gender']
        age = result['faceAttributes']['age']
        intext = gender + ',' + str(int(age))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=3) 
        draw.text((rect['left']-size,rect['top']-size),intext,font=fnt, fill='red', spacing=10, align='right')
    st.image(img, caption='Uploaded Image.',use_column_width=True)

