# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetUserReqDepartmentIDType(object):
    pass


@attr.s
class GetUserReqUserIDType(object):
    pass


@attr.s
class GetUserReq(object):
    user_id_type: GetUserReqUserIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 用户 ID 类型, 示例值："open_id", 可选值有: `open_id`：用户的 open id, `union_id`：用户的 union id, `user_id`：用户的 user id, 默认值: `open_id`,, 当值为 `user_id`, 字段权限要求: 获取用户 userid
    department_id_type: GetUserReqDepartmentIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 此次调用中使用的部门ID的类型, 示例值："open_department_id", 可选值有: `department_id`：以自定义department_id来标识部门, `open_department_id`：以open_department_id来标识部门, 默认值: `open_department_id`
    user_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 用户ID，需要与查询参数中的user_id_type类型保持一致。, 示例值："ou_7dab8a3d3cdcc9da365777c7ad535d62"


@attr.s
class GetUserRespUserCustomAttrValueGenericUser(object):
    id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户的user_id
    type: int = attr.ib(default=0, metadata={"req_type": "json"})  # 用户类型    1：用户


@attr.s
class GetUserRespUserCustomAttrValue(object):
    text: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 字段类型为 TEXT 时该参数定义字段值，字段类型为 HREF 时该参数定义网页标题
    url: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 字段类型为 HREF 时，该参数定义默认 URL
    pc_url: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 字段类型为 HREF 时，该参数定义PC端 URL
    option_value: str = attr.ib(default="", metadata={"req_type": "json"})  # 选项值
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 名称
    picture_url: str = attr.ib(default="", metadata={"req_type": "json"})  # 图片链接
    generic_user: GetUserRespUserCustomAttrValueGenericUser = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 字段类型为 GENERIC_USER 时，该参数定义引用人员


@attr.s
class GetUserRespUserCustomAttr(object):
    type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 自定义字段类型   , `TEXT`, `HREF`, `ENUMERATION`, `PICTURE_ENUM`, `GENERIC_USER`
    id: str = attr.ib(default="", metadata={"req_type": "json"})  # 自定义字段ID
    value: GetUserRespUserCustomAttrValue = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 自定义字段取值


@attr.s
class GetUserRespUserOrder(object):
    department_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 排序信息对应的部门ID
    user_order: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 用户在其直属部门内的排序，数值越大，排序越靠前
    department_order: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 用户所属的多个部门间的排序，数值越大，排序越靠前


@attr.s
class GetUserRespUserStatus(object):
    is_frozen: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否暂停
    is_resigned: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否离职
    is_activated: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否激活


@attr.s
class GetUserRespUserAvatar(object):
    avatar_72: str = attr.ib(default="", metadata={"req_type": "json"})  # 72*72像素头像链接
    avatar_240: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 240*240像素头像链接
    avatar_640: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 640*640像素头像链接
    avatar_origin: str = attr.ib(default="", metadata={"req_type": "json"})  # 原始头像链接


@attr.s
class GetUserRespUser(object):
    union_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户的union_id
    user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 租户内用户的唯一标识, 字段权限要求:  获取用户 user ID
    open_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户的open_id
    name: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户名, 最小长度：`1` 字符,**字段权限要求（满足任一）**：, 获取用户基本信息, 以应用身份访问通讯录（历史版本）
    en_name: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 英文名,**字段权限要求（满足任一）**：, 获取用户基本信息, 以应用身份访问通讯录（历史版本）
    email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 邮箱, 字段权限要求:  获取用户邮箱信息
    mobile: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 手机号, 字段权限要求:  获取用户手机号
    mobile_visible: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 手机号码可见性，true 为可见，false 为不可见，目前默认为 true。不可见时，组织员工将无法查看该员工的手机号码
    gender: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 性别, 可选值有: `0`：保密, `1`：男, `2`：女,**字段权限要求（满足任一）**：, 获取用户性别, 以应用身份访问通讯录（历史版本）
    avatar: GetUserRespUserAvatar = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 用户头像信息,**字段权限要求（满足任一）**：, 获取用户基本信息, 以应用身份访问通讯录（历史版本）
    status: GetUserRespUserStatus = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 用户状态,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    department_ids: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 用户所属部门的ID列表,**字段权限要求（满足任一）**：, 获取用户组织架构信息, 以应用身份访问通讯录（历史版本）
    leader_user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户的直接主管的用户ID,**字段权限要求（满足任一）**：, 获取用户组织架构信息, 以应用身份访问通讯录（历史版本）
    city: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 城市,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    country: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 国家或地区,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    work_station: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 工位,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    join_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 入职时间,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    is_tenant_manager: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否是租户管理员,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    employee_no: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 工号,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    employee_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 员工类型，可选值有：, 1：正式员工, 2：实习生, 3：外包, 4：劳务, 5：顾问   ,同时可读取到自定义员工类型的 int 值，可通过下方接口获取到该租户的自定义员工类型的名称   ,[获取人员类型](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/employee_type_enum/list),**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    orders: typing.List[GetUserRespUserOrder] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 用户排序信息,**字段权限要求（满足任一）**：, 获取用户组织架构信息, 以应用身份访问通讯录（历史版本）
    custom_attrs: typing.List[GetUserRespUserCustomAttr] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 自定义字段,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    enterprise_email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 企业邮箱，请先确保已在管理后台启用飞书邮箱服务,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）
    job_title: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 职务,**字段权限要求（满足任一）**：, 获取用户雇佣信息, 以应用身份访问通讯录（历史版本）


@attr.s
class GetUserResp(object):
    user: GetUserRespUser = attr.ib(default=None, metadata={"req_type": "json"})  # 用户信息


def _gen_get_user_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetUserResp,
        scope="Contact",
        api="GetUser",
        method="GET",
        url="https://open.feishu.cn/open-apis/contact/v3/users/:user_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
