# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetMessageFileReq(object):
    type: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 资源类型，可选"image, file“； image对应消息中的 图片资源。  file对应消息中的 文件、音频、视频资源, 示例值："image,"
    message_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 待查询资源对应的消息ID, 示例值："om_dc13264520392913993dd051dba21dcf"
    file_key: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 待查询资源的key, 示例值："file_456a92d6-c6ea-4de4-ac3f-7afcf44ac78g"


@attr.s
class GetMessageFileRespFile(object):
    pass


@attr.s
class GetMessageFileResp(object):
    file: typing.Union[str, bytes, io.BytesIO] = attr.ib(
        default=None, metadata={"req_type": "json"}
    )


@attr.s
class GetMessageFileResp(object):
    is_file: bool = attr.ib(factory=lambda: bool(), metadata={"req_type": "json"})
    code: int = attr.ib(default=0, metadata={"req_type": "json"})
    msg: str = attr.ib(default="", metadata={"req_type": "json"})
    data: GetMessageFileResp = attr.ib(default=None, metadata={"req_type": "json"})


def _gen_get_message_file_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetMessageFileResp,
        scope="Message",
        api="GetMessageFile",
        method="GET",
        url="https://open.feishu.cn/open-apis/im/v1/messages/:message_id/resources/:file_key",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
