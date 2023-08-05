# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class UploadFaceVerifyImageReqImage(object):
    pass


@attr.s
class UploadFaceVerifyImageReq(object):
    open_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 用户应用标识, 与employee_id二选其一
    employee_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 用户租户标识, 与open_id二选其一
    image: typing.Union[str, bytes, io.BytesIO] = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 带有头像的人脸照片


@attr.s
class UploadFaceVerifyImageResp(object):
    face_uid: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 人脸图片用户Uid，需返回给应用小程序，作为小程序调起人脸识别接口的uid参数


def _gen_upload_face_verify_image_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=UploadFaceVerifyImageResp,
        scope="HumanAuth",
        api="UploadFaceVerifyImage",
        method="POST",
        url="https://open.feishu.cn/open-apis/face_verify/v1/upload_face_image",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        is_file=True,
    )
