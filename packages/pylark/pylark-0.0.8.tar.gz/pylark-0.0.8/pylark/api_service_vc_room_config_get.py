# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetVCRoomConfigReq(object):
    scope: int = attr.ib(
        default=0, metadata={"req_type": "query"}
    )  # 查询节点范围, 示例值：5, 可选值有: `1`：租户, `2`：国家/地区, `3`：城市, `4`：建筑, `5`：楼层, `6`：会议室
    country_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 国家/地区ID scope为2，3时需要此参数, 示例值："086"
    district_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 城市ID scope为3时需要此参数, 示例值："001"
    building_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 建筑ID scope为4，5时需要此参数, 示例值："22"
    floor_name: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 楼层 scope为5时需要此参数, 示例值："4"
    room_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 会议室ID scope为6时需要此参数, 示例值："6383786266263"


@attr.s
class GetVCRoomConfigRespDigitalSignageMaterial(object):
    id: str = attr.ib(default="", metadata={"req_type": "json"})  # 素材ID
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 素材名称
    material_type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 素材类型, 可选值有: `1`：图片, `2`：视频, `3`：GIF
    url: str = attr.ib(default="", metadata={"req_type": "json"})  # 素材url
    duration: int = attr.ib(default=0, metadata={"req_type": "json"})  # 播放时长（单位sec）
    cover: str = attr.ib(default="", metadata={"req_type": "json"})  # 素材封面url
    md5: str = attr.ib(default="", metadata={"req_type": "json"})  # 素材文件md5


@attr.s
class GetVCRoomConfigRespDigitalSignage(object):
    enable: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否开启数字标牌功能
    mute: bool = attr.ib(
        factory=lambda: bool(), metadata={"req_type": "json"}
    )  # 是否静音播放
    start_display: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 日程会议开始前n分钟结束播放
    stop_display: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 会议结束后n分钟开始播放
    materials: typing.List[GetVCRoomConfigRespDigitalSignageMaterial] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 素材列表


@attr.s
class GetVCRoomConfigResp(object):
    room_background: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 飞书会议室背景图
    display_background: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 飞书签到板背景图
    digital_signage: GetVCRoomConfigRespDigitalSignage = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 飞书会议室数字标牌


def _gen_get_vc_room_config_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetVCRoomConfigResp,
        scope="VC",
        api="GetVCRoomConfig",
        method="GET",
        url="https://open.feishu.cn/open-apis/vc/v1/room_configs/query",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
