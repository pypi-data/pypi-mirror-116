# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetAttendanceShiftByIDReq(object):
    shift_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 班次 ID，示例值："6919358778597097404"


@attr.s
class GetAttendanceShiftByIDRespRestTimeRule(object):
    rest_begin_time: str = attr.ib(default="", metadata={"req_type": "json"})  # 休息开始时间
    rest_end_time: str = attr.ib(default="", metadata={"req_type": "json"})  # 休息结束时间


@attr.s
class GetAttendanceShiftByIDRespLateOffLateOnRule(object):
    late_off_minutes: int = attr.ib(default=0, metadata={"req_type": "json"})  # 晚走多长时间
    late_on_minutes: int = attr.ib(default=0, metadata={"req_type": "json"})  # 晚到多长时间


@attr.s
class GetAttendanceShiftByIDRespPunchTimeRule(object):
    on_time: str = attr.ib(default="", metadata={"req_type": "json"})  # 上班时间
    off_time: str = attr.ib(default="", metadata={"req_type": "json"})  # 下班时间
    late_minutes_as_late: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 晚到多长时间记为迟到
    late_minutes_as_lack: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 晚到多长时间记为缺卡
    on_advance_minutes: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 最早可提前多长时间打上班卡
    early_minutes_as_early: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 早走多长时间记为早退
    early_minutes_as_lack: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 早走多长时间记为缺卡
    off_delay_minutes: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 最晚可延后多长时间打下班卡


@attr.s
class GetAttendanceShiftByIDResp(object):
    shift_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 班次 ID
    shift_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 班次名称
    punch_times: int = attr.ib(default=0, metadata={"req_type": "json"})  # 打卡次数
    is_flexible: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否弹性打卡
    flexible_minutes: int = attr.ib(default=0, metadata={"req_type": "json"})  # 弹性打卡时间
    no_need_off: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否下班免打卡
    punch_time_rule: GetAttendanceShiftByIDRespPunchTimeRule = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 打卡规则
    late_off_late_on_rule: GetAttendanceShiftByIDRespLateOffLateOnRule = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 晚走晚到规则
    rest_time_rule: GetAttendanceShiftByIDRespRestTimeRule = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 休息时间规则


def _gen_get_attendance_shift_by_id_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetAttendanceShiftByIDResp,
        scope="Attendance",
        api="GetAttendanceShiftByID",
        method="GET",
        url="https://open.feishu.cn/open-apis/attendance/v1/shifts/:shift_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
