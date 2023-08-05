# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class UnsubscribeHelpdeskEventReqEvent(object):
    type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 事件类型, 示例值："helpdesk.ticket_message"
    subtype: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 事件子类型, 示例值："ticket_message.created_v1"


@attr.s
class UnsubscribeHelpdeskEventReq(object):
    events: typing.List[UnsubscribeHelpdeskEventReqEvent] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # event list to unsubscribe


@attr.s
class UnsubscribeHelpdeskEventResp(object):
    pass


def _gen_unsubscribe_helpdesk_event_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=UnsubscribeHelpdeskEventResp,
        scope="Helpdesk",
        api="UnsubscribeHelpdeskEvent",
        method="POST",
        url="https://open.feishu.cn/open-apis/helpdesk/v1/events/unsubscribe",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_helpdesk_auth=True,
    )
