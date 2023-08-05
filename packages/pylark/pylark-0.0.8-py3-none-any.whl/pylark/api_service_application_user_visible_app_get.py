# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetApplicationUserVisibleAppReq(object):
    page_token: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 分页起始位置标示，不填表示从头开始
    page_size: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 单页需求最大个数（最大 100），0 自动最大个数
    lang: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 优先展示的应用信息的语言版本（zh_cn：中文，en_us：英文，ja_jp：日文）
    open_id: str = attr.ib(default="", metadata={"req_type": "query"})  # 目标用户 open_id
    user_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 目标用户 user_id，与 open_id 至少给其中之一，user_id 优先于 open_id


@attr.s
class GetApplicationUserVisibleAppRespAppList(object):
    app_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 应用 ID
    primary_language: str = attr.ib(default="", metadata={"req_type": "json"})  # 应用首选语言
    app_name: str = attr.ib(default="", metadata={"req_type": "json"})  # 应用名称
    description: str = attr.ib(default="", metadata={"req_type": "json"})  # 应用描述
    avatar_url: str = attr.ib(default="", metadata={"req_type": "json"})  # 应用 icon
    app_scene_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 应用类型，0：企业自建应用；1：应用商店应用
    status: int = attr.ib(default=0, metadata={"req_type": "json"})  # 启停状态，0：停用；1：启用


@attr.s
class GetApplicationUserVisibleAppResp(object):
    page_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 下一个请求页应当给的起始位置
    page_size: int = attr.ib(default=0, metadata={"req_type": "json"})  # 本次请求实际返回的页大小
    total_count: int = attr.ib(default=0, metadata={"req_type": "json"})  # 可用的应用总数
    has_more: int = attr.ib(default=0, metadata={"req_type": "json"})  # 是否还有更多应用
    lang: str = attr.ib(default="", metadata={"req_type": "json"})  # 当前选择的版本语言
    app_list: GetApplicationUserVisibleAppRespAppList = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 应用列表


def _gen_get_application_user_visible_app_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetApplicationUserVisibleAppResp,
        scope="Application",
        api="GetApplicationUserVisibleApp",
        method="GET",
        url="https://open.feishu.cn/open-apis/application/v1/user/visible_apps",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
