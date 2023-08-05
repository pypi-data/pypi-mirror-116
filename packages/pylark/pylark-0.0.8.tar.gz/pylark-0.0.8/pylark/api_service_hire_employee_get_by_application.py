# Code generated by lark_sdk_gen. DO NOT EDIT.

from pylark.lark_request import RawRequestReq, _new_method_option
import attr
import typing
import io


@attr.s
class GetHireEmployeeByApplicationReq(object):
    application_id: str = attr.ib(
        default="", metadata={"req_type": "query"}
    )  # 投递ID, 示例值："123"


@attr.s
class GetHireEmployeeByApplicationRespEmployee(object):
    id: str = attr.ib(default="", metadata={"req_type": "json"})  # 员工ID
    application_id: str = attr.ib(default="", metadata={"req_type": "json"})  # 投递ID
    onboard_status: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 入职状态, 可选值有: `1`：已入职, `2`：已离职
    conversion_status: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 转正状态, 可选值有: `1`：未转正, `2`：已转正
    onboard_time: int = attr.ib(default=0, metadata={"req_type": "json"})  # 实际入职时间
    expected_conversion_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 预期转正时间
    actual_conversion_time: int = attr.ib(
        default=0, metadata={"req_type": "json"}
    )  # 实际转正时间
    overboard_time: int = attr.ib(default=0, metadata={"req_type": "json"})  # 离职时间
    overboard_note: str = attr.ib(default="", metadata={"req_type": "json"})  # 离职原因


@attr.s
class GetHireEmployeeByApplicationResp(object):
    employee: GetHireEmployeeByApplicationRespEmployee = attr.ib(
        default=None, metadata={"req_type": "json"}
    )  # 员工信息


def _gen_get_hire_employee_by_application_req(request, options) -> RawRequestReq:
    return RawRequestReq(
        dataclass=GetHireEmployeeByApplicationResp,
        scope="Hire",
        api="GetHireEmployeeByApplication",
        method="GET",
        url="https://open.feishu.cn/open-apis/hire/v1/employees/get_by_application",
        body=request,
        method_option=_new_method_option(options),
        need_tenant_access_token=True,
    )
