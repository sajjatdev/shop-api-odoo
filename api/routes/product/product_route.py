import dbm
from fastapi import APIRouter
from rpc.rcp_connection import rcpModel, rpcConnection,password,db

productRoute=APIRouter()


@productRoute.get("/product/list")
def product_list():
     uid=rpcConnection()
     model=rcpModel()

     product_data=model.execute_kw(db, uid, password, 'product.template', 'search_read', [[]],{'order':'id desc'})
     
     return product_data
      
