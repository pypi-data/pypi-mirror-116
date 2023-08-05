# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class DeleteBitableRecordReq(object):
    app_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # bitable app token, 示例值："appbcbWCzen6D8dezhoCH2RpMAh"
    table_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # table id, 示例值："tblsRc9GRRXKqhvW"
    record_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 单条记录的Id, 示例值："recpCsf4ME"


@attr.s
class DeleteBitableRecordResp(object):
    deleted: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否成功删除
    record_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 删除的记录 ID


def _gen_delete_bitable_record_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=DeleteBitableRecordResp,
        scope="Bitable",
        api="DeleteBitableRecord",
        method="DELETE",
        url="https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/:record_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
