# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class StartVCMeetingRecordingReq(object):
    meeting_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 会议ID（视频会议的唯一标识，视频会议开始后才会产生）, 示例值："6911188411932033028"
    timezone: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 录制文件时间显示使用的时区[-12,12], 示例值：8


@attr.s
class StartVCMeetingRecordingResp(object):
    pass


def _gen_start_vc_meeting_recording_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=StartVCMeetingRecordingResp,
        scope="VC",
        api="StartVCMeetingRecording",
        method="PATCH",
        url="https://open.feishu.cn/open-apis/vc/v1/meetings/:meeting_id/recording/start",
        body=request,
        method_option=_new_method_option(options),
        need_user_access_token=True,
    )
