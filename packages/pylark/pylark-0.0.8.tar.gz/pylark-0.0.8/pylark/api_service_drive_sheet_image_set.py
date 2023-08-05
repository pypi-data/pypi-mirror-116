# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class SetSheetValueImageReqImage(object):
    pass


@attr.s
class SetSheetValueImageReq(object):
    spreadsheet_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # spreadsheet的token，获取方式见[在线表格开发指南](https://open.feishu.cn/document/ukTMukTMukTM/uATMzUjLwEzM14CMxMTN/overview)
    range_: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 查询范围  range=<sheetId>!<开始格子>:<结束格子> 如：xxxx!A1:D5，详见[在线表格开发指南](https://open.feishu.cn/document/ukTMukTMukTM/uATMzUjLwEzM14CMxMTN/overview)。此处限定为一个格子，如: xxxx!A1:A1
    image: typing.List[SetSheetValueImageReqImage] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 需要写入的图片二进制流，支持  "PNG", "JPEG", "JPG", "GIF", "BMP", "JFIF", "EXIF", "TIFF", "BPG", "WEBP", "HEIC" 等图片格式
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 写入的图片名字


@attr.s
class SetSheetValueImageResp(object):
    spreadsheet_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # spreadsheet 的 token


def _gen_set_sheet_value_image_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=SetSheetValueImageResp,
        scope="Drive",
        api="SetSheetValueImage",
        method="POST",
        url="https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:spreadsheetToken/values_image",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
