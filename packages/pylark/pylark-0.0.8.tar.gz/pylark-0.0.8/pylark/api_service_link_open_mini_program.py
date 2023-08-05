# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class OpenMiniProgramReq(object):
    app_id: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 小程序 appId(可从「开发者后台-凭证与基础信息」获取)
    mode: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # PC小程序启动模式，枚举值包括：<br>`sidebar-semi`：聊天的侧边栏打开<br>`appCenter`：工作台中打开<br>`window`：独立大窗口打开<br>`window-semi`：独立小窗口打开，3.33版本开始支持此模式
    path: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 需要跳转的页面路径，路径后可以带参数。也可以使用 path_android、path_ios、path_pc 参数对不同的客户端指定不同的path
    path_android: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 同 path 参数，Android 端会优先使用该参数，如果该参数不存在，则会使用 path 参数
    path_ios: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 同 path 参数，iOS 端会优先使用该参数，如果该参数不存在，则会使用 path 参数
    path_pc: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 同 path 参数，PC 端会优先使用该参数，如果该参数不存在，则会使用 path 参数
    bdp_launch_query: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 自定义启动参数。可通过 [getHostLaunchQuery](https://open.feishu.cn/document/uYjL24iN/ugzM4UjL4MDO14COzgTN) 接口取得
    min_lk_ver: str = attr.ib(
        default="", metadata={"req_type": "json"}
    )  # 指定 AppLink 协议能够兼容的最小飞书版本，使用三位版本号 x.y.z。如果当前飞书版本号小于min_lk_ver，打开该 AppLink 会显示为兼容页面


@attr.s
class OpenMiniProgramResp(object):
    pass


def _gen_open_mini_program_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=OpenMiniProgramResp,
        scope="AppLink",
        api="OpenMiniProgram",
        method="",
        url="https://applink.feishu.cn/client/mini_program/open",
        body=request,
        method_option=_new_method_option(options),
    )
