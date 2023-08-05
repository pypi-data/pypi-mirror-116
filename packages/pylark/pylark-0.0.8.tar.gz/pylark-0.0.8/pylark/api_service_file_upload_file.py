# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class UploadFileReqFile(object):
    pass


@attr.s
class UploadFileReqFileType(object):
    pass


@attr.s
class UploadFileReq(object):
    file_type: UploadFileReqFileType = attr.ib(
        factory=lambda: UploadFileReqFileType(), metadata={"req_type": "json"}
    )  # 文件类型, 示例值："mp4", 可选值有: `opus`：上传opus音频文件；,其他格式的音频文件，请转为opus格式后上传，转换方式可参考：ffmpeg -i  SourceFile.mp3 -acodec libopus -ac 1 -ar 16000 TargetFile.opus, `mp4`：上传mp4视频文件, `pdf`：上传pdf格式文件, `doc`：上传doc格式文件, `xls`：上传xls格式文件, `ppt`：上传ppt格式文件, `stream`：上传stream格式文件
    file_name: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 带后缀的文件名, 示例值："测试视频.mp4"
    duration: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 文件的时长(视频，音频),单位:毫秒, 示例值：3000
    file: typing.Union[str, bytes, io.BytesIO] = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 文件内容, 示例值：二进制文件


@attr.s
class UploadFileResp(object):
    file_key: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件的key


def _gen_upload_file_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=UploadFileResp,
        scope="File",
        api="UploadFile",
        method="POST",
        url="https://open.feishu.cn/open-apis/im/v1/files",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        is_file=True,
    )
