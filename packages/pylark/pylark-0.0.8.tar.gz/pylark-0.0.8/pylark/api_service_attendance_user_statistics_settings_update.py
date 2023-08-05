# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class UpdateAttendanceUserStatisticsSettingsReqViewItemChildItem(object):
    code: str = attr.ib(default="", metadata={"req_type": "json"})  # 标题编号, 示例值："50101"
    value: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 开关字段,      , 可选值有: `0`：关闭, `1`：开启,非开关字段场景,  code = 51501  **可选值为1～6**


@attr.s
class UpdateAttendanceUserStatisticsSettingsReqViewItem(object):
    code: str = attr.ib(default="", metadata={"req_type": "json"})  # 编号, 示例值："501"
    title: str = attr.ib(default="", metadata={"req_type": "json"})  # 标题名称, 示例值："基本信息"
    child_items: typing.List[
        UpdateAttendanceUserStatisticsSettingsReqViewItemChildItem
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 子标题


@attr.s
class UpdateAttendanceUserStatisticsSettingsReqView(object):
    view_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 视图 ID, 示例值："TmpnNU5EQXpPVGN3TmpVMU16Y3lPVEEwTXl0dGIyNTBhQT09"
    stats_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 统计类型, 可选值有: `daily`：日度统计, `month`：月度统计
    user_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户 ID
    items: typing.List[UpdateAttendanceUserStatisticsSettingsReqViewItem] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 一级标题


@attr.s
class UpdateAttendanceUserStatisticsSettingsReqEmployeeType(object):
    pass


@attr.s
class UpdateAttendanceUserStatisticsSettingsReq(object):
    employee_type: UpdateAttendanceUserStatisticsSettingsReqEmployeeType = attr.ib(
        factory=lambda: UpdateAttendanceUserStatisticsSettingsReqEmployeeType(),
        metadata={"req_type": "query"},
    )  # 用户 ID 类型, 可选值有: `employee_id`：用户员工 ID, `employee_no`：用户员工工号
    user_stats_view_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 用户视图 ID, 示例值："TmpZNU5qTTJORFF6T1RnNU5UTTNOakV6TWl0dGIyNTBhQT09"
    view: UpdateAttendanceUserStatisticsSettingsReqView = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 统计视图


@attr.s
class UpdateAttendanceUserStatisticsSettingsRespViewItemChildItem(object):
    code: str = attr.ib(default="", metadata={"req_type": "json"})  # 标题编号
    value: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 是否开启,      , 可选值有: `0`：关闭, `1`：开启


@attr.s
class UpdateAttendanceUserStatisticsSettingsRespViewItem(object):
    code: str = attr.ib(default="", metadata={"req_type": "json"})  # 标题编码
    title: str = attr.ib(default="", metadata={"req_type": "json"})  # 标题名称
    child_items: typing.List[
        UpdateAttendanceUserStatisticsSettingsRespViewItemChildItem
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 子标题


@attr.s
class UpdateAttendanceUserStatisticsSettingsRespView(object):
    view_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 统计视图 ID, 示例值："TmpnNU5EQXpPVGN3TmpVMU16Y3lPVEEwTXl0dGIyNTBhQT09"
    stats_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 统计类型, 可选值有: `daily`：日度统计, `month`：月度统计
    user_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户 ID
    items: typing.List[UpdateAttendanceUserStatisticsSettingsRespViewItem] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 一级标题


@attr.s
class UpdateAttendanceUserStatisticsSettingsResp(object):
    view: UpdateAttendanceUserStatisticsSettingsRespView = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 用户视图


def _gen_update_attendance_user_statistics_settings_req(
    request, options
) -> RawRequestReq:
    return RawRequestReq(
        dataclass=UpdateAttendanceUserStatisticsSettingsResp,
        scope="Attendance",
        api="UpdateAttendanceUserStatisticsSettings",
        method="PUT",
        url="https://open.feishu.cn/open-apis/attendance/v1/user_stats_views/:user_stats_view_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
