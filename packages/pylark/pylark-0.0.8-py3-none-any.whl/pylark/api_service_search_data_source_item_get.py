# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetSearchDataSourceItemReq(object):
    data_source_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 数据源的id, 示例值："service_ticket"
    item_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 数据记录的唯一标识, 示例值："01010111"


@attr.s
class GetSearchDataSourceItemRespItemContent(object):
    format: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 内容的格式, 可选值有: `html`：html格式, `plaintext`：纯文本格式
    content_data: str = attr.ib(default="", metadata={"req_type": "json"})  # 全文数据


@attr.s
class GetSearchDataSourceItemRespItemMetadata(object):
    title: str = attr.ib(default="", metadata={"req_type": "json"})  # 该条数据记录对应的标题
    source_url: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 该条数据记录对应的跳转url
    create_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 数据项的创建时间。Unix 时间，单位为秒
    update_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 数据项的更新时间。Unix 时间，单位为秒


@attr.s
class GetSearchDataSourceItemRespItemACL(object):
    access: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 权限类型，优先级：Deny > Allow。默认为全员不可见，即 deny。, 可选值有: `allow`：允许访问, `deny`：禁止访问
    value: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 设置的权限值，例如 userID 、groupID，依赖 type 描述。,**注**：在 type 为 user 且 access 为 allow 时，可填 "everyone" 来表示该数据项对全员可见。
    type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 权限值类型, 可选值有: `user`：访问权限控制中指定用户可以访问或拒绝访问该条数据, `group`：访问权限控制中指定用户组可以访问或拒绝访问该条数据


@attr.s
class GetSearchDataSourceItemRespItem(object):
    id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # item 在 datasource 中的唯一标识
    acl: GetSearchDataSourceItemRespItemACL = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # item 的访问权限控制
    metadata: GetSearchDataSourceItemRespItemMetadata = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # item 的元信息
    structured_data: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 结构化数据（以 json 字符串传递），这些字段是搜索结果的展示字段（title字段无须在此另外指定）；目前支持的key为：, summary：搜索结果的摘要；, icon_url：搜索结果的icon地址；, footer：搜索结果的脚注
    content: GetSearchDataSourceItemRespItemContent = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 非结构化数据，如文档文本，飞书搜索会用来做召回


@attr.s
class GetSearchDataSourceItemResp(object):
    item: GetSearchDataSourceItemRespItem = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 数据项实例


def _gen_get_search_data_source_item_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetSearchDataSourceItemResp,
        scope="Search",
        api="GetSearchDataSourceItem",
        method="GET",
        url="https://open.feishu.cn/open-apis/search/v2/data_sources/:data_source_id/items/:item_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
