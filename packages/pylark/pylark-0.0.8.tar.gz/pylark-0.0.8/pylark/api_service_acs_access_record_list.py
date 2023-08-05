# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetACSAccessRecordListReqUserIDType(object):
    pass


@attr.s
class GetACSAccessRecordListReq(object):
    page_size: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 分页大小, 示例值：100, 最大值：`500`
    page_token: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 分页标记，第一次请求不填，表示从头开始遍历；分页查询结果还有更多项时会同时返回新的 page_token，下次遍历可采用该 page_token 获取查询结果, 示例值："AQD9/Rn9eij9Pm39ED40/dk53s4Ebp882DYfFaPFbz00L4CMZJrqGdzNyc8BcZtDbwVUvRmQTvyMYicnGWrde9X56TgdBuS+JKiSIkdexPw="
    from_: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 记录开始时间，单位秒, 示例值：1624520521
    to: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 记录结束时间，单位秒，,时间跨度不能超过30天, 示例值：1624520521
    device_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 门禁设备 ID, 示例值："7091146989218002577"
    user_id_type: GetACSAccessRecordListReqUserIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 用户 ID 类型, 示例值："open_id", 可选值有: `open_id`：用户的 open id, `union_id`：用户的 union id, `user_id`：用户的 user id, 默认值: `open_id`,, 当值为 `user_id`, 字段权限要求: 获取用户 userid


@attr.s
class GetACSAccessRecordListRespItem(object):
    access_record_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 门禁记录 ID
    user_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 门禁记录所属用户 ID
    device_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 门禁设备 ID
    is_clock_in: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否是打卡
    access_time: str = attr.ib(default="", metadata={"req_type": "json"})  # 访问时间，单位秒
    access_type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 识别方式, 可选值有: `FA`：人脸识别方式
    access_data: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 识别相关数据，根据 access_type 不同，取值不同
    is_door_open: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否开门


@attr.s
class GetACSAccessRecordListResp(object):
    items: typing.List[GetACSAccessRecordListRespItem] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # -
    page_token: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 分页标记，当 has_more 为 true 时，会同时返回新的 page_token，否则不返回 page_token
    has_more: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否还有更多项


def _gen_get_acs_access_record_list_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetACSAccessRecordListResp,
        scope="ACS",
        api="GetACSAccessRecordList",
        method="GET",
        url="https://open.feishu.cn/open-apis/acs/v1/access_records",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
