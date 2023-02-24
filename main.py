from fastapi import FastAPI, Form
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient


from passlib.context import CryptContext
from dotenv import load_dotenv
from dotenv import dotenv_values
import os
from fastapi.staticfiles import StaticFiles



templates = Jinja2Templates(directory="templates")
MONGO_URI = MongoClient("mongodb+srv://subbareddy:subbareddy123@cluster0.yjrvgmv.mongodb.net/test")

db = MONGO_URI['scmxpert']

app = FastAPI()
load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")






class User(BaseModel):
    name:  str
    email: str
    password: str
    confirmPassword: str


class Createshipment(BaseModel):

  invoicenumber: int
  containernumber: int
  shipmentdescription: str
  routedetails: str
  goodstype: str
  expecteddelivaryDate: str
  device: str
  pONumber: int
  Delivarnumber: int
  nDCNumber: int
  batchID: int
  serialNumberofGoods: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)





@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login")
def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/forgotpassword")
def index(request: Request):
    return templates.TemplateResponse("forgetpassword.html", {"request": request})


@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse, name="register")
async def register(request: Request, Name: str = Form(...), Email: str = Form(...),  Password: str = Form(...), Confirm_Password: str = Form(...)):
    hashed_password = hash_password(Password)
    data = User(name=Name, email=Email, password=hashed_password,
                confirmPassword=hashed_password)
    users = db["users"].find_one({"email": Email})
    try:
        if not users:
            new_register = db['users'].insert_one(dict(data))
            return templates.TemplateResponse("register.html", {'request': request, "message": "User was created successfully"})
    except Exception as e:
        print(e)
    return templates.TemplateResponse("register.html", {"request": request, "message": "user already exists"})


@app.get("/Dashborad")
def register(request: Request):
    return templates.TemplateResponse("Dashborad.html", {"request": request})


@app.post("/Dashborad", response_class=HTMLResponse)
def login_page(request: Request, Email: str = Form(...), Password: str = Form(...)):
    mycoll = db['users']
    users = mycoll.find_one({"email": Email})
    # confirm_password=verify_password
    try:
        if not users:
            return templates.TemplateResponse("login.html", {'request': request, "message":"User was not registered"})
        else:
            # if users and users["password"]==confirm_password:
            if verify_password(Password, users['password']):
                # if verify_password(Password,users['Password']):
                return templates.TemplateResponse("Dashborad.html", {'request': request})
            else:
                return templates.TemplateResponse("login.html", {'request': request,"message":"password did not match"})
    except Exception as e:
        print(e)


@app.get("/createshipment")
def index(request: Request):
    return templates.TemplateResponse("createshipment.html", {"request": request})


@app.post("/createshipment", response_class=HTMLResponse,name="createshipment")
async def create_createshipment(request: Request, Shipment_invoicenumber: int = Form(...), Container_Number: int = Form(...), Shipment_Description: str = Form(...), Route_Details: str = Form(...), Goods_Type: str = Form(...), Expected_Delivary_Date: str = Form(...), Device: str = Form(...), PO_Number: int = Form(...), Delivary_Number: int = Form(...), NDC_Number: int = Form(...), Batch_ID: int = Form(...), Serial_Number_of_Goods: int = Form(...)):
    shipdata = Createshipment(invoicenumber=Shipment_invoicenumber, containernumber=Container_Number, shipmentdescription=Shipment_Description, routedetails=Route_Details, goodstype=Goods_Type,
                              expecteddelivaryDate=Expected_Delivary_Date, device=Device, pONumber=PO_Number, Delivarnumber=Delivary_Number, nDCNumber=NDC_Number, batchID=Batch_ID, serialNumberofGoods=Serial_Number_of_Goods)
    # newregister = shipment_collection.insert_one(dict(shipdata))
    # return templates.TemplateResponse("createshipment.html", {"request": request})
    shipment_invoice = db['Shipment'].find_one({"invoicenumber":Shipment_invoicenumber})
    # print(shipment_invoice)
    if not shipment_invoice:
        shipment = db['Shipment'].insert_one(dict( shipdata))
        return templates.TemplateResponse("createshipment.html", {"request": request,"message":"Shipment was created"})
    else:
        return templates.TemplateResponse("createshipment.html", {"request": request,"message":"Shipment was already exits"})



@app.get('/DeviceData', response_class=HTMLResponse, name="DeviceData")
async def createshipment(request: Request):
    createshipment = []

    createshipment_all = db["Device_data"].find({})
    print(createshipment_all)
    print("show data")
    for i in createshipment_all:
        createshipment.append(i)
        print(createshipment_all)

    return templates.TemplateResponse("DeviceData.html", {"request": request, "createshipment": createshipment})
