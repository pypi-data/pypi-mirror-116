# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetDriveFileMetaReqRequestDocs(object):
    docs_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 文件的 token，获取方式见[概述](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/files/guide/introduction)
    docs_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 文件类型  <br>1) "doc": 飞书文档<br>2) "sheet": 飞书电子表格 <br>3) "bitable": 飞书多维表格<br>4) "mindnote": 飞书思维笔记 <br>5) "file": 飞书文件


@attr.s
class GetDriveFileMetaReq(object):
    request_docs: GetDriveFileMetaReqRequestDocs = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 请求文档，一次不超过200个


@attr.s
class GetDriveFileMetaRespDocsMetas(object):
    docs_token: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件token
    docs_type: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件类型
    title: str = attr.ib(default="", metadata={"req_type": "json"})  # 标题
    owner_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件拥有者
    create_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 创建时间（Unix时间戳）
    latest_modify_user: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 最后编辑者
    latest_modify_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 最后编辑时间（Unix时间戳）


@attr.s
class GetDriveFileMetaResp(object):
    docs_metas: GetDriveFileMetaRespDocsMetas = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 文件元数据


def _gen_get_drive_file_meta_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetDriveFileMetaResp,
        scope="Drive",
        api="GetDriveFileMeta",
        method="POST",
        url="https://open.feishu.cn/open-apis/suite/docs-api/meta",
        body=request,
        method_option=_new_method_option(options),
        need_user_access_token=True,
    )
