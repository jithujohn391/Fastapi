from fastapi import FastAPI,HTTPException,File,UploadFile
from model import User,Profile
from db import conn,cur
import psycopg2
from PIL import Image
import shutil
import os
app=FastAPI()
import base64
from fastapi.responses import Response,StreamingResponse,FileResponse
from io import BytesIO  
        
@app.post('/create_table')
def create_table():
    user_query="""
        CREATE TABLE Users(
        user_id INT ,
        full_name VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        password VARCHAR(100),
        phone VARCHAR(100),
        PRIMARY KEY(user_id));
    """
    
    profile_query="""
        CREATE TABLE Profile(
        profile_id INT,
        user_id INT,
        profile_picture varchar(1000000) NOT NULL,
        image_name varchar(100),
        PRIMARY KEY(profile_id),
        CONSTRAINT fk_user
            FOREIGN KEY(user_id) 
            REFERENCES Users(user_id)
            ON DELETE SET NULL
);
    """
    
    cur.execute(user_query)
    cur.execute(profile_query)
    conn.commit()
    return {'message':'table created successfully'}

@app.post('/insert')
async def insert_user_detail(user_detail:User):
    
    email_check_query = """
    SELECT EXISTS (SELECT 1 FROM Users WHERE email = %s);
    """
    phone_check_query = """
    SELECT EXISTS (SELECT 1 FROM Users WHERE phone = %s);
    """
    cur.execute(email_check_query, (user_detail.email,))
    email_exists = cur.fetchone()[0]
    cur.execute(phone_check_query,(str(user_detail.phone),))
    phone_exists = cur.fetchone()[0]
    if email_exists:
        return {"message":"email already exists"}
    elif phone_exists:
        return {"message":"phone number already exists"}
    else:

        query="""
            INSERT INTO users (user_id,full_name, email, password, phone) VALUES (%s, %s, %s, %s,%s) 
        """
        cur.execute(query,(user_detail.user_id,user_detail.full_name,user_detail.email,user_detail.password,user_detail.phone))       
        conn.commit()
        
        return {'userid':user_detail.user_id,'fullname':user_detail.full_name,
                'email':user_detail.email,'password':user_detail.password,
                'phone':user_detail.phone}

@app.post('/insert_profile')
async def insert_profile(profile_id:int,user_id:int,image: UploadFile = File(...)):
    
    image_data=await image.read()
    
    insert_query = """
            INSERT INTO profile (profile_id, user_id,profile_picture,image_name) VALUES (%s, %s, %s,%s);
        """
    cur.execute(insert_query,(profile_id,user_id,psycopg2.Binary(image_data),image.filename))
    conn.commit()
    cur.close()
    conn.close()
   
    return {'message':'inserted successfully','profileid':profile_id,'user':user_id,'img':image.filename}
    

@app.get('/getimage')
def get_image(image_id: int):
    query = """
        SELECT U.full_name,U.email,U.password,U.phone,P.profile_id,P.image_name,
        P.profile_picture FROM Users U
        INNER JOIN Profile P ON P.user_id = U.user_id
        WHERE U.user_id = %s;
    """
    cur.execute(query,(image_id,))
    image_data = cur.fetchone()
    img = bytes(image_data[5], encoding='utf-8')
    img_res = Response(img, media_type="image/jpeg")
    if image_data:
        # return StreamingResponse(BytesIO(img), media_type="image/jpeg")
        return {'name':image_data[0],'email':image_data[1],"password":image_data[2],'phone':image_data[3],'pid':image_data[4],'img_res':img_res}
        # return Response(img, media_type="image/jpeg") 
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
    




