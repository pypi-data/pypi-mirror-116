# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class CreateMailGroupMemberReqType(object):
    pass


@attr.s
class CreateMailGroupMemberReqDepartmentIDType(object):
    pass


@attr.s
class CreateMailGroupMemberReqUserIDType(object):
    pass


@attr.s
class CreateMailGroupMemberReq(object):
    user_id_type: CreateMailGroupMemberReqUserIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 用户 ID 类型, 示例值："open_id", 可选值有: `open_id`：用户的 open id, `union_id`：用户的 union id, `user_id`：用户的 user id, 默认值: `open_id`, 当值为 `user_id`, 字段权限要求: 获取用户 userid
    department_id_type: CreateMailGroupMemberReqDepartmentIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 此次调用中使用的部门ID的类型, 示例值："open_department_id", 可选值有: `department_id`：以自定义department_id来标识部门, `open_department_id`：以open_department_id来标识部门
    mailgroup_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 邮件组ID或者邮件组地址, 示例值："xxxxxxxxxxxxxxx 或 test_mail_group@xxx.xx"
    email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 成员邮箱地址（当成员类型是EXTERNAL_USER/MAIL_GROUP/OTHER_MEMBER时有值）, 示例值："test_memeber@xxx.xx"
    user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 租户内用户的唯一标识（当成员类型是USER时有值）, 示例值："xxxxxxxxxx"
    department_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 租户内部门的唯一标识（当成员类型是DEPARTMENT时有值）, 示例值："xxxxxxxxxx"
    type: CreateMailGroupMemberReqType = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 成员类型, 示例值："USER", 可选值有: `USER`：内部用户, `DEPARTMENT`：部门, `COMPANY`：全员, `EXTERNAL_USER`：外部用户, `MAIL_GROUP`：邮件组, `OTHER_MEMBER`：内部成员


@attr.s
class CreateMailGroupMemberRespType(object):
    pass


@attr.s
class CreateMailGroupMemberResp(object):
    member_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 邮件组内成员唯一标识
    email: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 成员邮箱地址（当成员类型是EXTERNAL_USER/MAIL_GROUP/OTHER_MEMBER时有值）
    user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 租户内用户的唯一标识（当成员类型是USER时有值）
    department_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 租户内部门的唯一标识（当成员类型是DEPARTMENT时有值）
    type: CreateMailGroupMemberRespType = attr.ib(
        factory=lambda: CreateMailGroupMemberRespType(), metadata={"req_type": "json"}
    )  # 成员类型, 可选值有: `USER`：内部用户, `DEPARTMENT`：部门, `COMPANY`：全员, `EXTERNAL_USER`：外部用户, `MAIL_GROUP`：邮件组, `OTHER_MEMBER`：内部成员


def _gen_create_mail_group_member_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=CreateMailGroupMemberResp,
        scope="Mail",
        api="CreateMailGroupMember",
        method="POST",
        url="https://open.feishu.cn/open-apis/mail/v1/mailgroups/:mailgroup_id/members",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
