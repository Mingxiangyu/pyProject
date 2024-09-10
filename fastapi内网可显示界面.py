import os
from typing import Union, List
from urllib.parse import urlparse

import pydantic
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse


async def document():
    return RedirectResponse(url="/docs")


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="HTTP status code")
    msg: str = pydantic.Field("success", description="HTTP status message")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


class ListDocsResponse(BaseResponse):
    data: List[dict] = pydantic.Field(..., description="List of document names")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": ["doc1.docx", "doc2.pdf", "doc3.txt"],
            }
        }


# 原文链接：https://blog.csdn.net/wenxingchen/article/details/129013509
def respSuccessJson(data: Union[list, dict, str] = None, msg: str = "Success"):
    """ 接口成功返回 """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'msg': msg,
            'data': data or {}
        }
    )


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


async def cli(audio_path: str, task_id: str):
    pass


def api_start(host, port):
    global app
    global local_doc_qa

    app = FastAPI()
    root = os.path.abspath(os.path.join(os.path.basename(__file__), "../.."))
    print(root)

    app.mount("/static", StaticFiles(directory=f"{root}/static"), name="static")
    # 允许跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.websocket("/local_doc_qa/stream-chat/{knowledge_base_id}")(stream_chat)

    app.get("/", response_model=BaseResponse)(document)

    app.post("/convert-text", response_model=BaseResponse)(cli)

    uvicorn.run(app, host=host, port=port)


"""
解决内网环境 FastAPI访问/docs接口文档显示空白、js/css无法加载
https://zhuanlan.zhihu.com/p/517645846?utm_id=0
https://blog.csdn.net/jaket5219999/article/details/135003381
"""
if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8000
    api_start(host, port)
