# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class BatchDeleteBitableRecordReq(object):
    app_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # bitable app token, 示例值："appbcbWCzen6D8dezhoCH2RpMAh"
    table_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # table id, 示例值："tblsRc9GRRXKqhvW"
    records: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 删除的多条记录id列表


@attr.s
class BatchDeleteBitableRecordRespRecord(object):
    deleted: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否成功删除
    record_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 删除的记录 ID


@attr.s
class BatchDeleteBitableRecordResp(object):
    records: typing.List[BatchDeleteBitableRecordRespRecord] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 记录


def _gen_batch_delete_bitable_record_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=BatchDeleteBitableRecordResp,
        scope="Bitable",
        api="BatchDeleteBitableRecord",
        method="POST",
        url="https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_delete",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
