# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetCalendarReq(object):
    calendar_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 日历ID, 示例值："feishu.cn_xxxxxxxxxx@group.calendar.feishu.cn"


@attr.s
class GetCalendarRespRole(object):
    pass


@attr.s
class GetCalendarRespType(object):
    pass


@attr.s
class GetCalendarRespPermissions(object):
    pass


@attr.s
class GetCalendarResp(object):
    calendar_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 日历ID
    summary: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 日历标题, 最大长度：`255` 字符
    description: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 日历描述, 最大长度：`255` 字符
    permissions: GetCalendarRespPermissions = attr.ib(
        factory=lambda: GetCalendarRespPermissions(), metadata={"req_type": "json"}
    )  # 日历公开范围, 可选值有: `private`：私密, `show_only_free_busy`：仅展示忙闲信息, `public`：他人可查看日程详情
    color: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 日历颜色，颜色RGB值的int32表示。客户端展示时会映射到色板上最接近的一种颜色。仅对当前身份生效
    type: GetCalendarRespType = attr.ib(
        factory=lambda: GetCalendarRespType(), metadata={"req_type": "json"}
    )  # 日历类型, 可选值有: `unknown`：未知类型, `primary`：用户或应用的主日历, `shared`：由用户或应用创建的共享日历, `google`：用户绑定的谷歌日历, `resource`：会议室日历, `exchange`：用户绑定的Exchange日历
    summary_alias: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 日历备注名，修改或添加后仅对当前身份生效, 最大长度：`255` 字符
    is_deleted: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 对于当前身份，日历是否已经被标记为删除, 默认值: `false`
    is_third_party: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 当前日历是否是第三方数据；三方日历及日程只支持读，不支持写入, 默认值: `false`
    role: GetCalendarRespRole = attr.ib(
        factory=lambda: GetCalendarRespRole(), metadata={"req_type": "json"}
    )  # 当前身份对于该日历的访问权限, 可选值有: `unknown`：未知权限, `free_busy_reader`：游客，只能看到忙碌/空闲信息, `reader`：订阅者，查看所有日程详情, `writer`：编辑者，创建及修改日程, `owner`：管理员，管理日历及共享设置


def _gen_get_calendar_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetCalendarResp,
        scope="Calendar",
        api="GetCalendar",
        method="GET",
        url="https://open.feishu.cn/open-apis/calendar/v4/calendars/:calendar_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
