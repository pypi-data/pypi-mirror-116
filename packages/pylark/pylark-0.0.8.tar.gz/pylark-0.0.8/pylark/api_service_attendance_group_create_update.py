# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class CreateUpdateAttendanceGroupReqGroupNoNeedPunchSpecialDay(object):
    punch_day: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 打卡日期，格式 20190101
    shift_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 班次 ID


@attr.s
class CreateUpdateAttendanceGroupReqGroupNeedPunchSpecialDay(object):
    punch_day: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 打卡日期，格式 20190101
    shift_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 班次 ID


@attr.s
class CreateUpdateAttendanceGroupReqGroupFreePunchCfg(object):
    free_start_time: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 自由班制的打卡开始时间
    free_end_time: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 自由班制的打卡结束时间
    punch_day: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 打卡时间，格式 1111100
    work_day_no_punch_as_lack: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 工作日不打卡是否记为缺卡


@attr.s
class CreateUpdateAttendanceGroupReqGroupLocationLongitude(object):
    pass


@attr.s
class CreateUpdateAttendanceGroupReqGroupLocationLatitude(object):
    pass


@attr.s
class CreateUpdateAttendanceGroupReqGroupLocation(object):
    location_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 地址 ID
    location_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 地址名称，必选字段
    location_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 地址类型，1：GPS，2：Wifi，8：IP
    latitude: float = attr.ib(default=None, metadata={"req_type": "json"})  # 地址纬度
    longitude: float = attr.ib(default=None, metadata={"req_type": "json"})  # 地址经度
    ssid: str = attr.ib(default="", metadata={"req_type": "json"})  # Wi-Fi 名称
    bssid: str = attr.ib(default="", metadata={"req_type": "json"})  # Wi-Fi 的 MAC 地址
    map_type: int = attr.ib(default=0, metadata={"req_type": "json"})  # 地图类型，1：高德, 2：谷歌
    address: str = attr.ib(default="", metadata={"req_type": "json"})  # 地址名称
    ip: str = attr.ib(default="", metadata={"req_type": "json"})  # IP 地址
    feature: str = attr.ib(default="", metadata={"req_type": "json"})  # 额外信息，例如运营商信息
    gps_range: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # GPS 打卡的有效范围（默认300m）


@attr.s
class CreateUpdateAttendanceGroupReqGroupMachine(object):
    machine_sn: str = attr.ib(default="", metadata={"req_type": "json"})  # 考勤机序列号
    machine_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 考勤机名称


@attr.s
class CreateUpdateAttendanceGroupReqGroup(object):
    group_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 考勤组的 ID, 需要从获取用户打卡结果的接口中获取 groupId
    group_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 考勤组名称
    time_zone: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 时区，可参考时区列表 https://www.zeitverschiebung.net/cn/all-time-zones.html
    bind_dept_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 绑定的部门 ID
    except_dept_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 排除的部门 ID
    bind_user_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 绑定的用户 ID
    except_user_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 排除的用户 ID
    group_leader_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 考勤负责人 ID 列表，需至少存在一名考勤负责人
    punch_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 考勤方式，0：考勤组人员可在任意地点、任意网络环境下打卡，1：GPS 打卡，2：Wi-Fi 打卡，4：考勤机打卡，8：IP 打卡。位运算，累加可支持多种考勤方式，比如，3：支持 GPS 打卡和 Wi-Fi 打卡，7：支持 GPS 打卡、Wi-Fi 打卡和考勤机打卡
    allow_out_punch: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否允许外勤打卡
    allow_pc_punch: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否允许 PC 端打卡
    allow_remedy: bool = attr.ib(default=None, metadata={"req_type": "json"})  # 是否允许补卡
    remedy_limit: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否限制补卡次数
    remedy_limit_count: int = attr.ib(default=0, metadata={"req_type": "json"})  # 补卡次数
    remedy_period_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 补卡次数周期类型，0：自然月，1：自定义周期
    remedy_period_custom_date: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 补卡自定义周期每月起始日
    remedy_date_limit: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否限制补卡时间
    remedy_date_num: int = attr.ib(default=0, metadata={"req_type": "json"})  # 补卡时间
    show_cumulative_time: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否展示上班累计时长
    show_over_time: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否展示加班累计时长
    hide_staff_punch_time: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否隐藏员工打卡具体时间
    face_punch: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否开启人脸识别打卡
    face_punch_cfg: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 人脸识别打卡规则，1：每次打卡均需人脸识别，2：疑似作弊打卡时需要人脸识别
    face_downgrade: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 人脸识别失败时是否允许普通拍照打卡
    replace_basic_pic: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 人脸识别失败时是否允许替换基准图片
    machines: typing.List[CreateUpdateAttendanceGroupReqGroupMachine] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 考勤机列表
    locations: typing.List[CreateUpdateAttendanceGroupReqGroupLocation] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 地址列表
    group_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 考勤类型，0：固定班制，2：排班制，3：自由班制
    punch_day_shift_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 固定班制必须填，长度必须等于7
    free_punch_cfg: CreateUpdateAttendanceGroupReqGroupFreePunchCfg = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 配置自由班制
    calendar_id: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 国家法定节假日历 ID，0：不根据国家法定节假日历排休，1：中国，2：美国，3：日本，4：印度，5：新加坡，默认为 1，必选字段
    need_punch_special_days: typing.List[
        CreateUpdateAttendanceGroupReqGroupNeedPunchSpecialDay
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 必须打卡的特殊日期
    no_need_punch_special_days: typing.List[
        CreateUpdateAttendanceGroupReqGroupNoNeedPunchSpecialDay
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 无需打卡的特殊日期
    effect_now: bool = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 是否立即生效，默认为 false


@attr.s
class CreateUpdateAttendanceGroupReqEmployeeType(object):
    pass


@attr.s
class CreateUpdateAttendanceGroupReq(object):
    employee_type: CreateUpdateAttendanceGroupReqEmployeeType = attr.ib(
        factory=lambda: CreateUpdateAttendanceGroupReqEmployeeType(),
        metadata={"req_type": "query"},
    )  # 用户 ID 的类型，必选字段，可用值：【employee_id（员工的 employeeId），employee_no（员工工号）】
    dept_type: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 部门 ID 的类型，必选字段，可用值：【open_id（暂时只支持部门的 openid）】，示例值：“od-fcb45c28a45311afd441b8869541ece8”
    group: CreateUpdateAttendanceGroupReqGroup = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 考勤组


@attr.s
class CreateUpdateAttendanceGroupRespGroupNoNeedPunchSpecialDay(object):
    punch_day: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 打卡日期，格式 20190101
    shift_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 班次 ID


@attr.s
class CreateUpdateAttendanceGroupRespGroupNeedPunchSpecialDay(object):
    punch_day: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 打卡日期，格式 20190101
    shift_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 班次 ID


@attr.s
class CreateUpdateAttendanceGroupRespGroupFreePunchCfg(object):
    free_start_time: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 自由班制的打卡开始时间
    free_end_time: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 自由班制的打卡结束时间
    punch_day: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 打卡时间，格式 1111100
    work_day_no_punch_as_lack: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 工作日不打卡是否记为缺卡


@attr.s
class CreateUpdateAttendanceGroupRespGroupLocationLongitude(object):
    pass


@attr.s
class CreateUpdateAttendanceGroupRespGroupLocationLatitude(object):
    pass


@attr.s
class CreateUpdateAttendanceGroupRespGroupLocation(object):
    location_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 地址 ID
    location_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 地址名称
    location_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 地址类型，1：GPS，2：Wifi，8：IP
    latitude: float = attr.ib(default=None, metadata={"req_type": "json"})  # 地址纬度
    longitude: float = attr.ib(default=None, metadata={"req_type": "json"})  # 地址经度
    ssid: str = attr.ib(default="", metadata={"req_type": "json"})  # Wi-Fi 名称
    bssid: str = attr.ib(default="", metadata={"req_type": "json"})  # Wi-Fi 的 MAC 地址
    map_type: int = attr.ib(default=0, metadata={"req_type": "json"})  # 地图类型，1：高德，2：谷歌
    address: str = attr.ib(default="", metadata={"req_type": "json"})  # 地址名称
    ip: str = attr.ib(default="", metadata={"req_type": "json"})  # IP 地址
    feature: str = attr.ib(default="", metadata={"req_type": "json"})  # 额外信息，例如运营商信息
    gps_range: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # GPS 打卡的有效范围（默认300m）


@attr.s
class CreateUpdateAttendanceGroupRespGroupMachine(object):
    machine_sn: str = attr.ib(default="", metadata={"req_type": "json"})  # 考勤机序列号
    machine_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 考勤机名称


@attr.s
class CreateUpdateAttendanceGroupRespGroup(object):
    group_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 考勤组的 ID, 需要从获取用户打卡结果的接口中获取 groupId
    group_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 考勤组名称
    time_zone: str = attr.ib(default="", metadata={"req_type": "json"})  # 时区
    bind_dept_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 绑定的部门 ID
    except_dept_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 排除的部门 ID
    bind_user_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 绑定的用户 ID
    except_user_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 排除的用户 ID
    group_leader_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 考勤负责人 ID 列表，必选字段
    punch_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 考勤方式，0：考勤组人员可在任意地点、任意网络环境下打卡，1：GPS 打卡，2：Wi-Fi 打卡，4：考勤机打卡，8：IP 打卡。位运算，累加可支持多种考勤方式，比如，3：支持 GPS 打卡和 Wi-Fi 打卡，7：支持 GPS 打卡、Wi-Fi 打卡和考勤机打卡
    allow_out_punch: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否允许外勤打卡
    allow_pc_punch: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否允许 PC 端打卡
    allow_remedy: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否允许补卡
    remedy_limit: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否限制补卡次数
    remedy_limit_count: int = attr.ib(default=0, metadata={"req_type": "json"})  # 补卡次数
    remedy_period_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 补卡次数周期类型，0：自然月，1：自定义周期
    remedy_period_custom_date: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 补卡自定义周期每月起始日
    remedy_date_limit: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否限制补卡时间
    remedy_date_num: int = attr.ib(default=0, metadata={"req_type": "json"})  # 补卡时间
    show_cumulative_time: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否展示上班累计时长
    show_over_time: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否展示加班累计时长
    hide_staff_punch_time: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否隐藏员工打卡具体时间
    face_punch: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否开启人脸识别打卡
    face_punch_cfg: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 人脸识别打卡规则，1：每次打卡均需人脸识别，2：疑似作弊打卡时需要人脸识别
    face_downgrade: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 人脸识别失败时是否允许普通拍照打卡
    replace_basic_pic: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 人脸识别失败时是否允许替换基准图片
    machines: typing.List[CreateUpdateAttendanceGroupRespGroupMachine] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 考勤机列表
    gps_range: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # GPS 打卡的有效范围（不建议使用）
    locations: typing.List[CreateUpdateAttendanceGroupRespGroupLocation] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 地址列表
    group_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 考勤类型，0：固定班制，2：排班制，3：自由班制
    punch_day_shift_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 固定班制必须填
    free_punch_cfg: CreateUpdateAttendanceGroupRespGroupFreePunchCfg = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 配置自由班制
    calendar_id: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 国家法定节假日历 ID，0：不根据国家法定节假日历排休，1：中国，2：美国，3：日本，4：印度，5：新加坡，默认为 1
    need_punch_special_days: typing.List[
        CreateUpdateAttendanceGroupRespGroupNeedPunchSpecialDay
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 必须打卡的特殊日期
    no_need_punch_special_days: typing.List[
        CreateUpdateAttendanceGroupRespGroupNoNeedPunchSpecialDay
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 无需打卡的特殊日期
    work_day_no_punch_as_lack: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 自由班制下工作日不打卡是否记为缺卡


@attr.s
class CreateUpdateAttendanceGroupResp(object):
    group: CreateUpdateAttendanceGroupRespGroup = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 考勤组


def _gen_create_update_attendance_group_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=CreateUpdateAttendanceGroupResp,
        scope="Attendance",
        api="CreateUpdateAttendanceGroup",
        method="POST",
        url="https://open.feishu.cn/open-apis/attendance/v1/groups",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
