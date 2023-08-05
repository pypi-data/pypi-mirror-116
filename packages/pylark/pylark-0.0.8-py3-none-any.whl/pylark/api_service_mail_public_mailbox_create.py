# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class CreatePublicMailboxReq(object):
    email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 公共邮箱地址, 示例值："test_public_mailbox@xxx.xx"
    name: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 公共邮箱名称, 示例值："test public mailbox"


@attr.s
class CreatePublicMailboxResp(object):
    public_mailbox_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 公共邮箱唯一标识
    email: str = attr.ib(default="", metadata={"req_type": "json"})  # 公共邮箱地址
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 公共邮箱名称


def _gen_create_public_mailbox_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=CreatePublicMailboxResp,
        scope="Mail",
        api="CreatePublicMailbox",
        method="POST",
        url="https://open.feishu.cn/open-apis/mail/v1/public_mailboxes",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
