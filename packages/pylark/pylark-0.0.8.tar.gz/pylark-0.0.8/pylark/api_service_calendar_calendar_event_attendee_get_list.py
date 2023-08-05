# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetCalendarEventAttendeeListReqUserIDType(object):
    pass


@attr.s
class GetCalendarEventAttendeeListReq(object):
    user_id_type: GetCalendarEventAttendeeListReqUserIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 用户 ID 类型, 示例值："open_id", 可选值有: `open_id`：用户的 open id, `union_id`：用户的 union id, `user_id`：用户的 user id, 默认值: `open_id`, 当值为 `user_id`, 字段权限要求: 获取用户 userid
    page_token: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 分页标记，第一次请求不填，表示从头开始遍历；分页查询结果还有更多项时会同时返回新的 page_token，下次遍历可采用该 page_token 获取查询结果, 示例值："780TRhwXXXXX"
    page_size: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 分页大小, 示例值：10, 最大值：`100`
    calendar_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 日历 ID, 示例值："feishu.cn_xxxxxxxxxx@group.calendar.feishu.cn"
    event_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 日程 ID, 示例值："xxxxxxxxx_0"


@attr.s
class GetCalendarEventAttendeeListRespItemChatMember(object):
    rsvp_status: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 参与人RSVP状态, 可选值有: `needs_action`：参与人尚未回复状态，或表示会议室预约中, `accept`：参与人回复接受，或表示会议室预约成功, `tentative`：参与人回复待定, `decline`：参与人回复拒绝，或表示会议室预约失败, `removed`：参与人或会议室已经从日程中被移除
    is_optional: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 参与人是否为「可选参加」, 默认值: `false`
    display_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 参与人名称
    is_organizer: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 参与人是否为日程组织者
    is_external: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 参与人是否为外部参与人


@attr.s
class GetCalendarEventAttendeeListRespItemType(object):
    pass


@attr.s
class GetCalendarEventAttendeeListRespItem(object):
    type: GetCalendarEventAttendeeListRespItemType = attr.ib(
        factory=lambda: GetCalendarEventAttendeeListRespItemType(),
        metadata={"req_type": "json"},
    )  # 参与人类型, 可选值有: `user`：用户, `chat`：群组, `resource`：会议室, `third_party`：邮箱
    attendee_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 参与人ID
    rsvp_status: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 参与人RSVP状态, 可选值有: `needs_action`：参与人尚未回复状态，或表示会议室预约中, `accept`：参与人回复接受，或表示会议室预约成功, `tentative`：参与人回复待定, `decline`：参与人回复拒绝，或表示会议室预约失败, `removed`：参与人或会议室已经从日程中被移除
    is_optional: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 参与人是否为「可选参加」，无法编辑群参与人的此字段, 默认值: `false`
    is_organizer: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 参与人是否为日程组织者
    is_external: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 参与人是否为外部参与人；外部参与人不支持编辑
    display_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 参与人名称
    chat_members: typing.List[GetCalendarEventAttendeeListRespItemChatMember] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 群中的群成员，当type为Chat时有效；群成员不支持编辑
    user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 参与人的用户id，依赖于user_id_type返回对应的取值，当is_external为true时，此字段只会返回open_id或者union_id
    chat_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # chat类型参与人的群组chat_id
    room_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # resource类型参与人的会议室room_id
    third_party_email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # third_party类型参与人的邮箱


@attr.s
class GetCalendarEventAttendeeListResp(object):
    items: typing.List[GetCalendarEventAttendeeListRespItem] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 日程的参与者列表
    has_more: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否还有更多项
    page_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 分页标记，当 has_more 为 true 时，会同时返回新的 page_token，否则不返回 page_token


def _gen_get_calendar_event_attendee_list_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetCalendarEventAttendeeListResp,
        scope="Calendar",
        api="GetCalendarEventAttendeeList",
        method="GET",
        url="https://open.feishu.cn/open-apis/calendar/v4/calendars/:calendar_id/events/:event_id/attendees",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
