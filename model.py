from pydantic import BaseModel

class User(BaseModel):
    user_id:int
    full_name:str
    email:str
    password:str
    phone:int
    
class Profile(BaseModel):
    profile_id:int
    user_id:int
    # profile_pic:str