from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import FastAPI, Response
import base64
import os
import json
from pydantic import BaseModel
import glob

class TimestampReq(BaseModel):
    timestamps: list[str]
    ch: int
    date: str

app = FastAPI()

base_path = os.environ["IMAGE_DIR"]
allowed_origin = os.environ["ALLOWED_ORIGIN"]

origins = [
    "http://localhost",
    "http://localhost:3001",
    allowed_origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/records")
async def get_records():
    records = []
    for record in os.listdir(base_path):
        if os.path.isdir(f"{base_path}/{record}"):
            availableChannels = []
            
            for channel in range(1, 9):
                if len(glob.glob(f'{base_path}/{record}/XVR_ch{channel}*.jpg')) > 0:
                    availableChannels.append(channel)
            
            recordData = {
                "date": record,
                "availableChannels": availableChannels
            }
            records.append(recordData)
            
            records.sort(key=lambda x: x["date"], reverse=True)
            
    return Response(json.dumps({"records": recordData}), 200)


@app.get("/frames-metadata")
async def get_frames_metadata(date: str, ch: str):
    #Add path whitelisting for security
    image_base_path = Path(f"{base_path}/{date}")
    file_timestamp_list = []
    
    reformat_date = date.replace("-", "")
    
    if image_base_path.exists():
        file_timestamp_list = [x.split("_")[2] for x in os.listdir(image_base_path) if f'ch{ch}_{reformat_date}' in x]
        file_timestamp_list.sort()
        
    return Response(json.dumps({"timestamps": file_timestamp_list, "total": len(file_timestamp_list), "ch": ch, "date": date}), 200)

@app.post("/frames")
async def get_frames(timestampReq: TimestampReq):
    image_b64_list = []
    
    if(len(timestampReq.timestamps) > 50):
        return Response(json.dumps({"error": "too many frames requested"}), 400)
    
    for timestamp in timestampReq.timestamps:
        #Add path whitelisting for security
        image_path = Path(f"{base_path}/{timestampReq.date}/XVR_ch{timestampReq.ch}_{timestamp}_E.jpg")
        if image_path.exists():
            with open(image_path, "rb") as image_file:
                base64_bytes = base64.b64encode(image_file.read())
                base64_string = base64_bytes.decode()
                image_b64_list.append(base64_string)
                
    return Response(json.dumps({"images": image_b64_list, "ch": timestampReq.ch, "date": timestampReq.date}), 200)