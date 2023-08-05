# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class CreateDriveMemberPermissionReq(object):
    type: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 权限客体类型, 示例值："doc", 可选值有: `doc`：文档, `sheet`：电子表格, `file`：云空间文件, `wiki`：知识库节点（暂不支持）, `bitable`：多维表格, `docx`：文档
    need_notification: bool = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 添加权限后是否通知对方, 示例值：false, 默认值: `false`
    token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 权限客体token, 示例值："doccnBKgoMyY5OMbUG6FioTXuBe"
    member_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户类型，可选值有：, `email`: 飞书企业邮箱, `openid`: 开放平台ID, `openchat`: 开放平台群组, `opendepartmentid`: 开放平台部门ID, `userid`: 用户自定义ID, 示例值："openid"
    member_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户类型下的值, 示例值："ou_7dab8a3d3cdcc9da365777c7ad535d62"
    perm: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 需要增加的权限，可选值有：, `view`: 可阅读, `edit`: 可编辑, `full_access`: 所有权限, 示例值："view"


@attr.s
class CreateDriveMemberPermissionRespMember(object):
    member_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 用户类型，可选值有：, `email`: 飞书企业邮箱, `openid`: 开放平台ID, `openchat`: 开放平台群组, `opendepartmentid`: 开放平台部门ID, `userid`: 用户自定义ID
    member_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 用户类型下的值
    perm: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 需要增加的权限，可选值有：, `view`: 可阅读, `edit`: 可编辑, `full_access`: 所有权限


@attr.s
class CreateDriveMemberPermissionResp(object):
    member: CreateDriveMemberPermissionRespMember = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 本次添加权限的用户信息


def _gen_create_drive_member_permission_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=CreateDriveMemberPermissionResp,
        scope="Drive",
        api="CreateDriveMemberPermission",
        method="POST",
        url="https://open.feishu.cn/open-apis/drive/v1/permissions/:token/members",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
