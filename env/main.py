from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from typing import Optional 
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Literal


app = FastAPI()


'''Introducton '''
@app.get('/')

async def root() : 
    return {'message':"Hello world"}

# @app.post('/')

# async def post():
#     return {'message':'hello from the post route'}

# @app.put('/')

# async def put():
#     return {'message': 'Hello from the put route'}

# # @app.get("/items")
# # async def list_items():
# #     return {"message":"list items route"}


@app.get("/items/{id_item}")
async def get_id_item(id_item, q : str | None = None):
    return {"item":id_item, "un query paramaters":q}

# @app.get("/users/me")
# async def current_user():
#     return {"message" : "this is the current user"}

# @app.get("/users/{user_id}")
# async def get_user_id (user_id : str):
#     return {"message" : user_id}


# # class FoorEnum (str, Enum) :
# #     fruits = "fruits"
# #     vegetables ="vegetables"
# #     dairy = "dairy"
    
# # @app.get("/foods/")

# # fake_items_db = [{"item_name":"Foo"}, {"item_name":"Bar"}, {"item_name" : "Baz"}]

# # @app.get("/items")
# # async def list_items(skip : int =0, limit : int = 10) : 
# #     return  fake_items_db[skip: skip + limit]

# @app.get("/items/{id_item}")
# async def get_item(id_item : str, q: str | None =  None, short:bool = False, test : str = None):
#     item = {"item_id" : id_item}
#     if q:
#         item.update({"q":q})
#     if not short :
#         item.update({
#             'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a.'
#         })
#     return [item, test]
# @app.get('/users/{user_id}/items/{item_id}')
# async def get_user_item (user_id : int, item_id:str, q:str | None = None, short : bool = False) : 
#     item = {"item_id" : item_id}
#     if q:
#         item.update({"q":q})
#     if not short :
#         item.update({
#             'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a.'
#         })
#     return item, user_id
'''Request Body'''
class Item(BaseModel) : 
    name : str
    description : str | None = None
    price : int 
    tax : float | None = None

@app.post('/item')

def create_item (item : Item) : 
    item_dict = item.dict()
    if item.tax : 
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    else :
        item.tax = 0
    return item_dict

# @app.put('/items/{item_id}')

# async def create_item_with_put (item_id : int, item:Item, q: str = None) :
#     item_dict = item.dict()
#     if q :
#         item_dict.update({"q":q})
#     return {"item_id " : item_id, **item_dict}


# @app.get('/items')
# async def read_items (q : str | None = Query(..., min_length=5, max_length=10)
#                       ) :
#     results = {"items" : [{"item_id":"Foo"}, {"item_id ":"Bar"}]}
#     if q : 
#         results.update({"q":q})
#     return results

# @app.get('/items_validation/{item_id}')
# async def read_items_validation (*, 
#                                  item_id : int = Path(..., title="the ID of the item get", gt=10), 
#                                  q : str | None = Query(None, alias="item_query")) :
#     results = {"item_id":item_id}
#     if q : 
#         results.update({'q':q})
#     return results
"""
Part 7 Bodey Multiple parameters 
"""

# class Item(BaseModel) : 
#     name : str
#     description : str | None = None
#     price : float
#     tax : float | None = None
# class User (BaseModel) :
#     username : str
#     full_name : str | None = None
# class Importance (BaseModel) :
#     importance : int
# @app.put("/items/{item_id}")
# async def update_item (
#     *,
#     item_id : int = Path(..., title="the ID of the item to get ", ge=0, le=150),
#     q : str | None = None,
#     item : Item | None = None,
#     user : User | None = None,
#     importance : str = Body(None)
# ) : 
#     results = {"item_id":item_id}
#     if q : 
#         results.update({'q':q})
#     if item : 
#         results.update({"item":item})
#     if user : 
#         results.update({"user":user})
#     if importance : 
#         results.update({"importance":importance})
#     return results

'''Part 8 -> Fields'''
class Item(BaseModel) :
    name : str
    description : str  | None = Field(None, title="the description of the idem", max_length=300 )
    price : float = Field(..., gt=0, description = "the price must be the greater" )
    tax : float | None = None

@app.put('/items/{item_id}')
async def update_item (item_id : int, item:Item = Body(..., embed=True)) :
    results = {"item_id":item_id, "item" : item}
    return results

'''Part 9 bodey Nested Model'''
# class Image(BaseModel) :
#     url : HttpUrl
#     name : str 

# class Item(BaseModel) : 
#     name : str 
#     description : str | None = None
#     price : float
#     tax : float | None = None
#     tags : list[str] = []
#     image : Image

# @app.put('/items/{item_id}')
# async def update_item (item_id : int, item:Item, q:str | None = None) :
#     results = {"item_id":item_id, "item" : item}
#     return results, q
# @app.post('/blahs')
# async def create_some_blahs (blahs : dict[int, float]) :
#     return blahs

'''Part 10 declare request example Data'''
# class Item (BaseModel) :
#     name : str 
#     description: str | None = None
#     price : float 
#     tax : float | None = None

#     class Config :
#         schema_extra = {
#             "example" : {
#                 "name":"foo",
#                 "description": "A very nice item ",
#                 "price":16.25,
#                 "tax": 1.67
#             },
#         }
# @app.put('/items/{item_id}')
# async def update_item(item_id : int, item : Item ):
#     results = {"item_id":item_id, "item" : item}
#     return results 
'''Part  11 Extra data types '''
# @app.put('/items.{item_id}')
# async def reads_item (item_id : UUID , start_date : datetime | None = Body(None)):
#     return {"item_id":item_id, "start_date" : start_date}

'''Part 12 cookkies and Header Parameters '''
# @app.get('/items')
# async def read_items (cookie_id : str | None = Cookie(None),
#                       accept_encoding : str | None = Header(None),
#                       sec_ch_ua: str | None = Header(None),
#                       user_agent : str | None = Header(None)
# ) : 
#     return {"cookie_id " : cookie_id, "accept_encoding":accept_encoding, "sec_ch_ua": sec_ch_ua, "User-Agent":user_agent}

'''Part 13  Model'''

# class Item(BaseModel):
#     name : str 
#     description : str | None = None
#     price : float
#     tax : float = 10.5
#     tags : list[str] = []

# items = {
#     "foo": {"name":"Foo", "price":50.2},
#     "bar":{"name":"Bar", "description":"The bartenders", "price":62,"tax":20.2},
#     "baz":{"name":"Baz", "description":None, "price":50.2,"tax":10.5,"tags":[]},

# }

# @app.get('/items/{item_id}', response_model=Item,  response_model_exclude_unset=True,)
# async def read_item (item_id :Literal["foo","bar","baz"]) :
#     return items[item_id]

# @app.get('/items/{item_id}/public', response_model=Item,  response_model_include={"name","price"})
# async def read_item (item_id :Literal["foo","bar","baz"]) :
#     return items[item_id]

# @app.post('/items/', response_model=Item)
# async def create_item(item : Item):
#     return item
# class UserBase(BaseModel):
#     username : str
#     email : EmailStr
#     full_name : str | None = None


# class UserIn(UserBase):
#     password : str
    
# class UserOut(UserBase):
#     pass                                                                                  


# @app.post('/user/', response_model=UserOut)
# async def create_user (user : UserIn):
#     return user

'''Part 14 Extra Model'''
class UserIn(BaseModel):
    name : str
    password : str
    full_name: str | None = None
    email : EmailStr

class UserOut(BaseModel):
    username : str
    email : EmailStr
    full_name: str | None = None

class UserInBD(BaseModel):
    name : str
    password : str
    full_name: str | None = None
    email : EmailStr

def fake_password_hasser(raw_password : str) :
    return f"supersecret{raw_password}"

def fake_save_user(user_in : UserIn) :
    hashed_password = fake_password_hasser(user_in.password)
    user_in_db = UserInBD(**user_in.dict(), hashed_password=hashed_password)
    print(type(user_in_db))
    print('Userin.dict', user_in.dict())
    print("user saved ")
    return user_in_db

@app.post('/user/', response_model=UserOut)
async def create_user(user_in : UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

