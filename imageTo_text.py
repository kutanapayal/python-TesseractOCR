from PIL import Image
import pytesseract
import os
import cv2 as cv
from fastapi import FastAPI, UploadFile, File
import uvicorn
from fastapi.encoders import jsonable_encoder

app=FastAPI()
@app.post("/Fetch_Text/")
async def image(*,preprocessing_method: str,image:UploadFile=File(...)):
    preprocess = preprocessing_method
    print(image.file)
    print(preprocess)
    
    try:
        os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        print(e)
    file_name=os.getcwd()+"/images/"+image.filename.replace(" ","-")

    with open(file_name,'wb+') as f:
        f.write(image.file.read())
        f.close()
    
    img = cv.imread(file_name)
#   cv.imshow('Image',img)   
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    if preprocess == "thresh":
        gray = cv.threshold(gray,0,255, cv.THRESH_BINARY|cv.THRESH_OTSU)[1]
    elif preprocess == "blur":
        gray = cv.medianBlur(gray,3)

#    cv.imshow('Gray',gray)

    file_name1=os.getcwd()+"/images/"+"processed_"+image.filename.replace(" ","-")
    cv.imwrite(file_name1,gray)

    text = pytesseract.image_to_string(file_name1)
#    cv.waitKey(0)

    file=jsonable_encoder({"Text --> ":text})
    return file

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)