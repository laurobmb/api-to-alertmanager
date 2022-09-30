from fastapi import FastAPI,File, Form,Request,Depends
from fastapi.responses import HTMLResponse
import aiofiles as aiof
from typing import Any, Dict, AnyStr, List, Union
from starlette.routing import Host
import uvicorn,json,requests,os, logging

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

#app=FastAPI(title="api-alertmanager", docs_url = None, redoc_url = None)
app=FastAPI(title="api-alertmanager")

logname = 'log/fastapi.log'

logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logging.info("Running Api Alertmanager")

#logging.debug("Debug logging test...")
#logging.info("Program is working as expected")
#logging.warning("Warning, the program may not function properly")
#logging.error("The program encountered an error")
#logging.critical("The program crashed")

logger = logging.getLogger('APIalertmanager')

def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)
    return data


@app.get("/")
async def root():
    logging.info("Program is working as expected function root")
    return 'up'


@app.post("/api")
async def received_json(arbitrary_json: JSONStructure = None):

    if isinstance(arbitrary_json,dict):
        dict_001 = convert(arbitrary_json)

        if DEBUG == '1':
            print(type(dict_001))
            print(dict_001)

        logging.info("received_json: {}".format(dict_001))
        
        return {"received_data": dict_001}
    else:
        logging.error("The program encountered an error")
        return {"received_data": "error"}

if __name__ == '__main__':
    try:
        DEBUG = os.environ['DEBUG']
    except:
        DEBUG = 1
    
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

