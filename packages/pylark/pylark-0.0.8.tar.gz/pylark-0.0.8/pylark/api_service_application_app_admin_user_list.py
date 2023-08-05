# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetApplicationAppAdminUserListReq(object):
    pass


@attr.s
class GetApplicationAppAdminUserListRespUserOpenID(object):
    user_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 某管理员的user_id
    union_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 某管理员的union_id


@attr.s
class GetApplicationAppAdminUserListRespUser(object):
    open_id: GetApplicationAppAdminUserListRespUserOpenID = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 某管理员的open_id


@attr.s
class GetApplicationAppAdminUserListResp(object):
    user_list: typing.List[GetApplicationAppAdminUserListRespUser] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 管理员列表


def _gen_get_application_app_admin_user_list_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetApplicationAppAdminUserListResp,
        scope="Application",
        api="GetApplicationAppAdminUserList",
        method="GET",
        url="https://open.feishu.cn/open-apis/user/v4/app_admin_user/list",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
