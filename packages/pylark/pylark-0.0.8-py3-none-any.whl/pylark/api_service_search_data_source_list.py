# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetSearchDataSourceListReq(object):
    view: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 回包数据格式，0-全量数据；1-摘要数据。,**注**：摘要数据仅包含"id"，"name"，"state"。, 示例值：0, 可选值有: `0`：全量数据, `1`：摘要数据
    page_token: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 分页标记，第一次请求不填，表示从头开始遍历；分页查询结果还有更多项时会同时返回新的 page_token，下次遍历可采用该 page_token 获取查询结果, 示例值："PxZFma9OIRhdBlT/dOYNiu2Ro8F2WAhcby7OhOijfljZ"
    page_size: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 分页大小, 示例值：10, 最大值：`50`


@attr.s
class GetSearchDataSourceListRespItem(object):
    id: str = attr.ib(default="", metadata={"req_type": "json"})  # 数据源的唯一标识
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # data_source的展示名称
    state: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 数据源状态，0-未上线，1-已上线, 可选值有: `0`：未上线, `1`：已上线
    description: str = attr.ib(default="", metadata={"req_type": "json"})  # 对于数据源的描述
    create_time: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 创建时间，使用Unix时间戳，单位为“秒”
    update_time: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 更新时间，使用Unix时间戳，单位为“秒”
    is_exceed_quota: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否超限


@attr.s
class GetSearchDataSourceListResp(object):
    has_more: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否还有更多项
    page_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 分页标记，当 has_more 为 true 时，会同时返回新的 page_token，否则不返回 page_token
    items: typing.List[GetSearchDataSourceListRespItem] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 数据源中的数据记录


def _gen_get_search_data_source_list_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetSearchDataSourceListResp,
        scope="Search",
        api="GetSearchDataSourceList",
        method="GET",
        url="https://open.feishu.cn/open-apis/search/v2/data_sources",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
