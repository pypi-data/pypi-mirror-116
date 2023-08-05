# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class TransferApprovalInstanceReq(object):
    approval_code: str = attr.ib(default="", metadata={"req_type": "json"})  # 审批定义 Code
    instance_code: str = attr.ib(default="", metadata={"req_type": "json"})  # 审批实例 Code
    user_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 操作用户
    task_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 任务 ID
    comment: str = attr.ib(default="", metadata={"req_type": "json"})  # 意见
    transfer_user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 被转交人唯一 ID
    open_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户open_id <br>如果没有user_id，必须要有open_id
    transfer_open_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 被转交人open_id <br>如果没有transfer_user_id，必须要有transfer_open_id


@attr.s
class TransferApprovalInstanceResp(object):
    pass


def _gen_transfer_approval_instance_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=TransferApprovalInstanceResp,
        scope="Approval",
        api="TransferApprovalInstance",
        method="POST",
        url="https://www.feishu.cn/approval/openapi/v2/instance/transfer",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
