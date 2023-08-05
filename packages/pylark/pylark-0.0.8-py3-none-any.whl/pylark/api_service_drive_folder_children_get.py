# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetDriveFolderChildrenReq(object):
    types: typing.List[str] = attr.ib(
        factory=lambda: [], metadata={"req_type": "query"}
    )  # 需要查询的文件类型，默认返回所有 children；types 可多选，可选类型有 doc、sheet、file、folder 。如 url?types=folder&types=sheet
    folder_token: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 文件夹的 token，获取方式见 [概述](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/files/guide/introduction)


@attr.s
class GetDriveFolderChildrenRespChildren(object):
    token: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件的 token
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件的标题
    type: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件的类型


@attr.s
class GetDriveFolderChildrenResp(object):
    parent_token: str = attr.ib(default="", metadata={"req_type": "json"})  # 文件夹的 token
    children: GetDriveFolderChildrenRespChildren = attr.ib(
        factory=lambda: GetDriveFolderChildrenRespChildren(),
        metadata={"req_type": "json"},
    )  # 文件夹的下的文件


def _gen_get_drive_folder_children_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetDriveFolderChildrenResp,
        scope="Drive",
        api="GetDriveFolderChildren",
        method="GET",
        url="https://open.feishu.cn/open-apis/drive/explorer/v2/folder/:folderToken/children",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
