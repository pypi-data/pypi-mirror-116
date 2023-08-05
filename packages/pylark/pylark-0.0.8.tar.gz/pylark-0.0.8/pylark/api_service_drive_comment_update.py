# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class UpdateDriveCommentReqContentElementPerson(object):
    user_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 回复 at联系人, 示例值："ou_cc19b2bfb93f8a44db4b4d6eab*****"


@attr.s
class UpdateDriveCommentReqContentElementDocsLink(object):
    url: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 回复 at云文档, 示例值："https://bytedance.feishu.cn/docs/doccnHh7U87HOFpii5u5G*****"


@attr.s
class UpdateDriveCommentReqContentElementTextRun(object):
    text: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 回复 普通文本, 示例值："comment text"


@attr.s
class UpdateDriveCommentReqContentElement(object):
    type: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 回复的内容元素, 示例值："text_run", 可选值有: `text_run`：普通文本, `docs_link`：at 云文档链接, `person`：at 联系人
    text_run: UpdateDriveCommentReqContentElementTextRun = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 文本内容
    docs_link: UpdateDriveCommentReqContentElementDocsLink = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 文本内容
    person: UpdateDriveCommentReqContentElementPerson = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 文本内容


@attr.s
class UpdateDriveCommentReqContent(object):
    elements: typing.List[UpdateDriveCommentReqContentElement] = attr.ib(
        factory=lambda: [], metadata={"req_type": "json"}
    )  # 回复的内容


@attr.s
class UpdateDriveCommentReqFileType(object):
    pass


@attr.s
class UpdateDriveCommentReq(object):
    file_type: UpdateDriveCommentReqFileType = attr.ib(
        factory=lambda: UpdateDriveCommentReqFileType(), metadata={"req_type": "query"}
    )  # 文档类型, 示例值："doc", 可选值有: `doc`：文档, `sheet`：表格, `file`：文件
    file_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 文档token, 示例值："doccnHh7U87HOFpii5u5G*****"
    comment_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 评论ID, 示例值："6916106822734578184"
    reply_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 回复ID, 示例值："6916106822734594568"
    content: UpdateDriveCommentReqContent = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 回复内容


@attr.s
class UpdateDriveCommentResp(object):
    pass


def _gen_update_drive_comment_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=UpdateDriveCommentResp,
        scope="Drive",
        api="UpdateDriveComment",
        method="PUT",
        url="https://open.feishu.cn/open-apis/drive/v1/files/:file_token/comments/:comment_id/replies/:reply_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
