# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class StartHelpdeskServiceReq(object):
    human_service: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否直接进入人工(若appointed_agents填写了，该值为必填), 示例值：false
    appointed_agents: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 客服 open ids (获取方式参考[获取单个用户信息](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/get))，human_service需要为true
    open_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户 open id,(获取方式参考[获取单个用户信息](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/get)), 示例值："ou_7dab8a3d3cdcc9da365777c7ad535d62"
    customized_info: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 工单来源自定义信息，长度限制1024字符，如设置，[获取工单详情](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/helpdesk-v1/ticket/get)会返回此信息, 示例值："test customized info"


@attr.s
class StartHelpdeskServiceResp(object):
    chat_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 客服群open ID
    ticket_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 工单ID


def _gen_start_helpdesk_service_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=StartHelpdeskServiceResp,
        scope="Helpdesk",
        api="StartHelpdeskService",
        method="POST",
        url="https://open.feishu.cn/open-apis/helpdesk/v1/start_service",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_helpdesk_auth=True,
    )
