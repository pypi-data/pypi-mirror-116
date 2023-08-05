# Code generated by lark_sdk_gen. DO NOT EDIT.

import typing
from pylark.lark_request import Response

from pylark.api_service_human_auth_face_verify_get_auth_result import (
    GetFaceVerifyAuthResultReq,
    GetFaceVerifyAuthResultResp,
    _gen_get_face_verify_auth_result_req,
)
from pylark.api_service_human_auth_face_verify_upload_image import (
    UploadFaceVerifyImageReq,
    UploadFaceVerifyImageResp,
    _gen_upload_face_verify_image_req,
)
from pylark.api_service_human_auth_face_verify_crop_image import (
    CropFaceVerifyImageReq,
    CropFaceVerifyImageResp,
    _gen_crop_face_verify_image_req,
)
from pylark.api_service_human_auth_identity import (
    CreateIdentityReq,
    CreateIdentityResp,
    _gen_create_identity_req,
)


if typing.TYPE_CHECKING:
    from lark import Lark


class LarkHumanAuthService(object):
    cli: "Lark"

    def __init__(self, cli: "Lark"):
        self.cli = cli

    def get_face_verify_auth_result(
        self, request: GetFaceVerifyAuthResultReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetFaceVerifyAuthResultResp, Response]:
        return self.cli.raw_request(
            _gen_get_face_verify_auth_result_req(request, options)
        )

    def upload_face_verify_image(
        self, request: UploadFaceVerifyImageReq, options: typing.List[str] = None
    ) -> typing.Tuple[UploadFaceVerifyImageResp, Response]:
        return self.cli.raw_request(_gen_upload_face_verify_image_req(request, options))

    def crop_face_verify_image(
        self, request: CropFaceVerifyImageReq, options: typing.List[str] = None
    ) -> typing.Tuple[CropFaceVerifyImageResp, Response]:
        return self.cli.raw_request(_gen_crop_face_verify_image_req(request, options))

    def create_identity(
        self, request: CreateIdentityReq, options: typing.List[str] = None
    ) -> typing.Tuple[CreateIdentityResp, Response]:
        return self.cli.raw_request(_gen_create_identity_req(request, options))
