# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class DeleteSearchDataSourceReq(object):
    data_source_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 数据源的唯一标识, 示例值："6953903108179099667"


@attr.s
class DeleteSearchDataSourceResp(object):
    pass


def _gen_delete_search_data_source_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=DeleteSearchDataSourceResp,
        scope="Search",
        api="DeleteSearchDataSource",
        method="DELETE",
        url="https://open.feishu.cn/open-apis/search/v2/data_sources/:data_source_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
