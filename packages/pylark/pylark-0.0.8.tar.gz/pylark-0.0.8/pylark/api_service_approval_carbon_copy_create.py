# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class CreateApprovalCarbonCopyReq(object):
    approval_code: str = attr.ib(default="", metadata={"req_type": "json"})  # 审批定义 code
    instance_code: str = attr.ib(default="", metadata={"req_type": "json"})  # 审批实例 code
    user_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 发起抄送的人的 user_id
    open_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 发起抄送的人的 open_id，如果传了 user_id 则优先使用 user_id，二者不能同时为空
    cc_user_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 被抄送人的 user_id 列表
    cc_open_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 被抄送人的 open_id 列表，与 cc_user_ids 不可同时为空
    comment: str = attr.ib(default="", metadata={"req_type": "json"})  # 抄送留言


@attr.s
class CreateApprovalCarbonCopyResp(object):
    pass


def _gen_create_approval_carbon_copy_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=CreateApprovalCarbonCopyResp,
        scope="Approval",
        api="CreateApprovalCarbonCopy",
        method="POST",
        url="https://www.feishu.cn/approval/openapi/v2/instance/cc",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
