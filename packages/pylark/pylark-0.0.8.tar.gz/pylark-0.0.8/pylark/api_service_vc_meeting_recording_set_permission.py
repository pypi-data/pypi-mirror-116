# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class SetVCPermissionMeetingRecordingReqPermissionObject(object):
    id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 授权对象ID, 示例值："ou_3ec3f6a28a0d08c45d895276e8e5e19b"
    type: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 授权对象类型, 示例值：1, 可选值有: `1`：用户授权, `2`：群组授权, `3`：租户内授权（id字段不填）, `4`：公网授权（id字段不填）
    permission: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 权限, 示例值：1, 可选值有: `1`：查看


@attr.s
class SetVCPermissionMeetingRecordingReqUserIDType(object):
    pass


@attr.s
class SetVCPermissionMeetingRecordingReq(object):
    user_id_type: SetVCPermissionMeetingRecordingReqUserIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 用户 ID 类型, 示例值："open_id", 可选值有: `open_id`：用户的 open id, `union_id`：用户的 union id, `user_id`：用户的 user id, 默认值: `open_id`,, 当值为 `user_id`, 字段权限要求: 获取用户 userid
    meeting_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 会议ID（视频会议的唯一标识，视频会议开始后才会产生）, 示例值："6911188411932033028"
    permission_objects: typing.List[
        SetVCPermissionMeetingRecordingReqPermissionObject
    ] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 授权对象列表


@attr.s
class SetVCPermissionMeetingRecordingResp(object):
    pass


def _gen_set_vc_permission_meeting_recording_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=SetVCPermissionMeetingRecordingResp,
        scope="VC",
        api="SetVCPermissionMeetingRecording",
        method="PATCH",
        url="https://open.feishu.cn/open-apis/vc/v1/meetings/:meeting_id/recording/set_permission",
        body=request,
        method_option=_new_method_option(options),
        need_user_access_token=True,
    )
