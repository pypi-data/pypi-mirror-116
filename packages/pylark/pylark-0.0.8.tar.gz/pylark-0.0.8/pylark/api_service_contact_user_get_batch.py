# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class BatchGetUserReq(object):
    employee_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "query"}
    )  # 支持通过 open_id 或者 employee_id 查询用户信息，不支持混合两种 ID 进行查询，单次请求支持的最大用户数量为100
    open_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "query"}
    )  # 支持通过 open_id 或者 employee_id 查询用户信息，不支持混合两种 ID 进行查询，单次请求支持的最大用户数量为100


@attr.s
class BatchGetUserRespUserInfoCustomAttr(object):
    pass


@attr.s
class BatchGetUserRespUserInfo(object):
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户名
    name_py: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户名拼音
    en_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 英文名
    employee_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户的 employee_id，申请了"获取用户 user_id"权限的应用返回该字段
    employee_no: str = attr.ib(default="", metadata={"req_type": "json"})  # 工号
    open_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户的 open_id
    union_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户的 union_id
    status: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 用户状态，bit0(最低位): 1冻结，0未冻结；bit1:1离职，0在职；bit2:1未激活，0已激活
    employee_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 员工类型。1:正式员工；2:实习生；3:外包；4:劳务；5:顾问
    avatar_72: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户头像，72*72px
    avatar_240: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户头像，240*240px
    avatar_640: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户头像，640*640px
    avatar_url: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户头像，原始大小
    gender: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 性别，未设置不返回该字段。1:男；2:女
    email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户邮箱地址，已申请"获取用户邮箱"权限返回该字段
    mobile: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户手机号，已申请"获取用户手机号"权限的企业自建应用返回该字段
    description: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户个人签名
    country: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户所在国家
    city: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户所在城市
    work_station: str = attr.ib(default="", metadata={"req_type": "json"})  # 工位
    is_tenant_manager: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否是企业超级管理员
    join_time: int = attr.ib(default=0, metadata={"req_type": "json"})  # 入职时间，未设置不返回该字段
    update_time: int = attr.ib(default=0, metadata={"req_type": "json"})  # 更新时间
    leader_employee_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户直接领导的 employee_id，企业自建应用返回，应用商店应用申请了 employee_id 权限时才返回
    leader_open_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户直接领导的 open_id
    leader_union_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户直接领导的 union_id
    departments: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 用户所在部门自定义 ID列表，用户可能同时存在于多个部门
    open_departments: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 用户所在部门 openID 列表，用户可能同时存在于多个部门
    custom_attrs: BatchGetUserRespUserInfoCustomAttr = attr.ib(
        factory=lambda: BatchGetUserRespUserInfoCustomAttr(),
        metadata={"req_type": "json"},
    )  # 用户的自定义属性信息。<br>该字段返回的每一个属性包括自定义属性 ID 和自定义属性值。 <br>企业开放了自定义用户属性且为该用户设置了自定义属性的值，才会返回该字段


@attr.s
class BatchGetUserResp(object):
    user_infos: typing.List[BatchGetUserRespUserInfo] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 用户信息


def _gen_batch_get_user_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=BatchGetUserResp,
        scope="Contact",
        api="BatchGetUser",
        method="GET",
        url="https://open.feishu.cn/open-apis/contact/v1/user/batch_get",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
