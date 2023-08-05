# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetChatReqUserIDType(object):
    pass


@attr.s
class GetChatReq(object):
    user_id_type: GetChatReqUserIDType = attr.ib(
        default=None, metadata={"req_type": "query"}
    )  # 用户 ID 类型, 示例值："open_id", 可选值有: `open_id`：用户的 open id, `union_id`：用户的 union id, `user_id`：用户的 user id, 默认值: `open_id`, 当值为 `user_id`, 字段权限要求: 获取用户 userid
    chat_id: str = attr.ib(
        default="", metadata={"req_type": "path"}
    )  # 群 ID, 示例值："oc_a0553eda9014c201e6969b478895c230"


@attr.s
class GetChatRespModerationPermission(object):
    pass


@attr.s
class GetChatRespMembershipApproval(object):
    pass


@attr.s
class GetChatRespLeaveMessageVisibility(object):
    pass


@attr.s
class GetChatRespJoinMessageVisibility(object):
    pass


@attr.s
class GetChatRespChatType(object):
    pass


@attr.s
class GetChatRespOwnerIDType(object):
    pass


@attr.s
class GetChatRespEditPermission(object):
    pass


@attr.s
class GetChatRespAtAllPermission(object):
    pass


@attr.s
class GetChatRespShareCardPermission(object):
    pass


@attr.s
class GetChatRespAddMemberPermission(object):
    pass


@attr.s
class GetChatRespI18nNames(object):
    zh_cn: str = attr.ib(default="", metadata={"req_type": "json"})  # 中文名
    en_us: str = attr.ib(default="", metadata={"req_type": "json"})  # 英文名
    ja_jp: str = attr.ib(default="", metadata={"req_type": "json"})  # 日文名


@attr.s
class GetChatResp(object):
    avatar: str = attr.ib(default="", metadata={"req_type": "json"})  # 群头像 URL
    name: str = attr.ib(default="", metadata={"req_type": "json"})  # 群名称
    description: str = attr.ib(default="", metadata={"req_type": "json"})  # 群描述
    i18n_names: GetChatRespI18nNames = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 群国际化名称
    add_member_permission: GetChatRespAddMemberPermission = attr.ib(
        factory=lambda: GetChatRespAddMemberPermission(), metadata={"req_type": "json"}
    )  # 群成员添加权限(all_members/only_owner)
    share_card_permission: GetChatRespShareCardPermission = attr.ib(
        factory=lambda: GetChatRespShareCardPermission(), metadata={"req_type": "json"}
    )  # 群分享权限(allowed/not_allowed)
    at_all_permission: GetChatRespAtAllPermission = attr.ib(
        factory=lambda: GetChatRespAtAllPermission(), metadata={"req_type": "json"}
    )  # at 所有人权限(all_members/only_owner)
    edit_permission: GetChatRespEditPermission = attr.ib(
        factory=lambda: GetChatRespEditPermission(), metadata={"req_type": "json"}
    )  # 群编辑权限(all_members/only_owner)
    owner_id_type: GetChatRespOwnerIDType = attr.ib(
        factory=lambda: GetChatRespOwnerIDType(), metadata={"req_type": "json"}
    )  # 群主 ID 的类型(open_id/user_id/union_id)，群主是机器人时，不返回该字段。
    owner_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 群主 ID，群主是机器人时，不返回该字段。
    chat_mode: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 群模式(group/topic/p2p)
    chat_type: GetChatRespChatType = attr.ib(
        factory=lambda: GetChatRespChatType(), metadata={"req_type": "json"}
    )  # 群类型(private/public)
    chat_tag: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 优先级最高的一个群tag(inner/tenant/department/edu/meeting/customer_service)
    join_message_visibility: GetChatRespJoinMessageVisibility = attr.ib(
        factory=lambda: GetChatRespJoinMessageVisibility(),
        metadata={"req_type": "json"},
    )  # 入群消息可见性(only_owner/all_members/not_anyone)
    leave_message_visibility: GetChatRespLeaveMessageVisibility = attr.ib(
        factory=lambda: GetChatRespLeaveMessageVisibility(),
        metadata={"req_type": "json"},
    )  # 出群消息可见性(only_owner/all_members/not_anyone)
    membership_approval: GetChatRespMembershipApproval = attr.ib(
        factory=lambda: GetChatRespMembershipApproval(), metadata={"req_type": "json"}
    )  # 加群审批(no_approval_required/approval_required)
    moderation_permission: GetChatRespModerationPermission = attr.ib(
        factory=lambda: GetChatRespModerationPermission(), metadata={"req_type": "json"}
    )  # 发言权限(all_members/only_owner/moderator_list)


def _gen_get_chat_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetChatResp,
        scope="Chat",
        api="GetChat",
        method="GET",
        url="https://open.feishu.cn/open-apis/im/v1/chats/:chat_id",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
        need_user_access_token=True,
    )
