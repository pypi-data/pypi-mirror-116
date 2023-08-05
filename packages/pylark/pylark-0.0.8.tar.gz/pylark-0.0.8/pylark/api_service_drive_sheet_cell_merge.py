# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class MergeSheetCellReq(object):
    spreadsheet_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # spreadsheet 的 token，获取方式见[在线表格开发指南](https://open.feishu.cn/document/ukTMukTMukTM/uATMzUjLwEzM14CMxMTN/overview)
    range_: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 查询范围，包含 sheetId 与单元格范围两部分，目前支持四种索引方式，详见 [在线表格开发指南](https://open.feishu.cn/document/ukTMukTMukTM/uATMzUjLwEzM14CMxMTN/overview)
    merge_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 可选三个类型，"MERGE_ALL"  将所选区域直接合并、"MERGE_ROWS"  将所选区域按行合并、"MERGE_COLUMNS"  将所选区域按列合并响应


@attr.s
class MergeSheetCellResp(object):
    spreadsheet_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # spreadsheet 的 token


def _gen_merge_sheet_cell_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=MergeSheetCellResp,
        scope="Drive",
        api="MergeSheetCell",
        method="POST",
        url="https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/:spreadsheetToken/merge_cells",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
