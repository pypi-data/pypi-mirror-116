# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class CreateSheetReq(object):
    title: str = attr.ib(default="", metadata={"req_type": "json"})  # 表格标题, 示例值："title"
    folder_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 文件夹token, 示例值："fldcnMsNb*****hIW9IjG1LVswg"


@attr.s
class CreateSheetRespSpreadsheet(object):
    title: str = attr.ib(default="", metadata={"req_type": "json"})  # 表格标题
    folder_token: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件夹token
    url: str = attr.ib(default="", metadata={"req_type": "json"})  # 文档url
    spreadsheet_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 表格token


@attr.s
class CreateSheetResp(object):
    spreadsheet: CreateSheetRespSpreadsheet = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 表格


def _gen_create_sheet_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=CreateSheetResp,
        scope="Drive",
        api="CreateSheet",
        method="POST",
        url="https://open.feishu.cn/open-apis/sheets/v3/spreadsheets",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
