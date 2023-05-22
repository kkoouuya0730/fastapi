from logging import getLogger, config
import yaml
from inspect import signature
from enum import Enum
import functools
from fastapi.responses import JSONResponse
from requests.models import Response
import requests
from demo.models.todo import Todo
import socket


# ロガーの名前
APPLICATION_LOGGER = "ApplicationLogger"

logger = getLogger(APPLICATION_LOGGER)


class ApiName(Enum):
    """APIの種類を明示するclass"""

    # TodoAPI
    TODO = "todos"
    # UserAPI
    USER = "users"
    # ToneAPI
    DONE = "done"


def read_logger():
    """ロガーの設定を読み込む"""
    with open("/home/kkoouuya/python/fastapi/demo/log/conf.yaml") as file:
        read_data = file.read()
    yaml_data = yaml.safe_load(read_data)
    config.dictConfig(yaml_data)


def get_arg_value(func, args: tuple, name: str) -> any:
    # 関数シグネチャを取得
    sig = signature(func)
    keys = tuple(sig.parameters.keys())
    if name not in keys:
        raise Exception(f"this func is not contain {name}")
    return args[keys.index(name)]


# デコレーターの引数を受け取る
def start_and_end_logging(api_name: ApiName, id_name: str = "request_id"):

    # デコレート対象を受け取る
    def _start_and_end_logging(f):

        # デコレート対象の関数のメタ情報を返す
        @functools.wraps(f)
        # 前後の処理を実行する
        def _wapper(*args, **kwargs):
            if not isinstance(api_name, ApiName):
                e = Exception(f"api_nameの型はApiName型を想定していますが、{type(api_name)}です。")
                logger.warning(e)
                raise e
            id = get_arg_value(f, args, id_name)
            logger.info(f"[{id}][START] POST {api_name.value} API is called.")

            # デコレート対象の関数を実行
            result = f(*args, **kwargs)

            logger.info(f"[{id}][END] POST {api_name.value} API is called.")
            if not isinstance(result, (Todo, Response, JSONResponse)):
                e = Exception(f"{type(result)}: 戻り値の型が仕様と異なります。")
                logger.warning(e)
                raise e
            # if result.status_code == requests.codes.ok:
            #     logger.info(f"[{id}]POST {api_name.value} API Completed 200 OK.")
            return result

        return _wapper

    return _start_and_end_logging
