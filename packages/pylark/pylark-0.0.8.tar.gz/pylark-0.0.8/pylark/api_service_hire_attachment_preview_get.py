# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetHireAttachmentPreviewReq(object):
    attachment_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 附件id, 示例值："11111"


@attr.s
class GetHireAttachmentPreviewResp(object):
    url: str = attr.ib(default="", metadata={"req_type": "json"})  # 预览链接


def _gen_get_hire_attachment_preview_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetHireAttachmentPreviewResp,
        scope="Hire",
        api="GetHireAttachmentPreview",
        method="GET",
        url="https://open.feishu.cn/open-apis/hire/v1/attachments/:attachment_id/preview",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
