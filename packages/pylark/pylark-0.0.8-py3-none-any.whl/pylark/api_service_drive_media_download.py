# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class DownloadDriveMediaReqRange(object):
    pass


@attr.s
class DownloadDriveMediaReq(object):
    extra: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 扩展信息, 示例值："[请参考-上传点类型及对应Extra说明](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/drive-v1/media/introduction)"
    file_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 文件标识符, 示例值："boxcnabCdefg12345"
    range: DownloadDriveMediaReqRange = attr.ib(
        factory=lambda: DownloadDriveMediaReqRange(),
        metadata={"req_type": "header", "header": "range"},
    )  # 指定文件下载部分，示例:bytes=0-1024


@attr.s
class DownloadDriveMediaRespFile(object):
    pass


@attr.s
class DownloadDriveMediaResp(object):
    file: typing.Union[str, bytes, io.BytesIO] = attr.ib(
        default=None, metadata={"resp_type": "header"}
    )
    filename: str = attr.ib(default="", metadata={"resp_type": "header"})  # 文件名


@attr.s
class DownloadDriveMediaResp(object):
    is_file: bool = attr.ib(factory=lambda: bool(), metadata={"resp_type": "header"})
    code: int = attr.ib(default=0, metadata={"resp_type": "header"})
    msg: str = attr.ib(default="", metadata={"resp_type": "header"})
    data: DownloadDriveMediaResp = attr.ib(
        default=None, metadata={"resp_type": "header"}
    )


def _gen_download_drive_media_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=DownloadDriveMediaResp,
        scope="Drive",
        api="DownloadDriveMedia",
        method="GET",
        url="https://open.feishu.cn/open-apis/drive/v1/medias/:file_token/download",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
