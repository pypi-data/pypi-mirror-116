# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class DeleteMeetingRoomBuildingReq(object):
    building_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 要删除的建筑ID


@attr.s
class DeleteMeetingRoomBuildingResp(object):
    pass


def _gen_delete_meeting_room_building_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=DeleteMeetingRoomBuildingResp,
        scope="MeetingRoom",
        api="DeleteMeetingRoomBuilding",
        method="POST",
        url="https://open.feishu.cn/open-apis/meeting_room/building/delete",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
