# Code generated by lark_sdk_gen. DO NOT EDIT.

import typing
from pylark.lark_request import Response

from pylark.api_service_application_is_user_admin import (
    IsApplicationUserAdminReq,
    IsApplicationUserAdminResp,
    _gen_is_application_user_admin_req,
)
from pylark.api_service_application_user_admin_scope_get import (
    GetApplicationUserAdminScopeReq,
    GetApplicationUserAdminScopeResp,
    _gen_get_application_user_admin_scope_req,
)
from pylark.api_service_application_app_visibility_get import (
    GetApplicationAppVisibilityReq,
    GetApplicationAppVisibilityResp,
    _gen_get_application_app_visibility_req,
)
from pylark.api_service_application_user_visible_app_get import (
    GetApplicationUserVisibleAppReq,
    GetApplicationUserVisibleAppResp,
    _gen_get_application_user_visible_app_req,
)
from pylark.api_service_application_app_list import (
    GetApplicationAppListReq,
    GetApplicationAppListResp,
    _gen_get_application_app_list_req,
)
from pylark.api_service_application_app_visibility_update import (
    UpdateApplicationAppVisibilityReq,
    UpdateApplicationAppVisibilityResp,
    _gen_update_application_app_visibility_req,
)
from pylark.api_service_application_app_admin_user_list import (
    GetApplicationAppAdminUserListReq,
    GetApplicationAppAdminUserListResp,
    _gen_get_application_app_admin_user_list_req,
)
from pylark.api_service_application_paid_scope_check_user import (
    CheckUserIsInApplicationPaidScopeReq,
    CheckUserIsInApplicationPaidScopeResp,
    _gen_check_user_is_in_application_paid_scope_req,
)
from pylark.api_service_application_order_list import (
    GetApplicationOrderListReq,
    GetApplicationOrderListResp,
    _gen_get_application_order_list_req,
)
from pylark.api_service_application_order_get import (
    GetApplicationOrderReq,
    GetApplicationOrderResp,
    _gen_get_application_order_req,
)
from pylark.api_service_application_usage_overview import (
    GetApplicationUsageOverviewReq,
    GetApplicationUsageOverviewResp,
    _gen_get_application_usage_overview_req,
)
from pylark.api_service_application_usage_trend import (
    GetApplicationUsageTrendReq,
    GetApplicationUsageTrendResp,
    _gen_get_application_usage_trend_req,
)
from pylark.api_service_application_usage_detail import (
    GetApplicationUsageDetailReq,
    GetApplicationUsageDetailResp,
    _gen_get_application_usage_detail_req,
)
from pylark.api_service_application_message_overview import (
    GetApplicationMessageOverviewReq,
    GetApplicationMessageOverviewResp,
    _gen_get_application_message_overview_req,
)
from pylark.api_service_application_message_trend import (
    GetApplicationMessageTrendReq,
    GetApplicationMessageTrendResp,
    _gen_get_application_message_trend_req,
)
from pylark.api_service_application_message_detail import (
    GetApplicationMessageDetailReq,
    GetApplicationMessageDetailResp,
    _gen_get_application_message_detail_req,
)


if typing.TYPE_CHECKING:
    from lark import Lark


class LarkApplicationService(object):
    cli: "Lark"

    def __init__(self, cli: "Lark"):
        self.cli = cli

    def is_application_user_admin(
        self, request: IsApplicationUserAdminReq, options: typing.List[str] = None
    ) -> typing.Tuple[IsApplicationUserAdminResp, Response]:
        return self.cli.raw_request(
            _gen_is_application_user_admin_req(request, options)
        )

    def get_application_user_admin_scope(
        self, request: GetApplicationUserAdminScopeReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationUserAdminScopeResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_user_admin_scope_req(request, options)
        )

    def get_application_app_visibility(
        self, request: GetApplicationAppVisibilityReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationAppVisibilityResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_app_visibility_req(request, options)
        )

    def get_application_user_visible_app(
        self, request: GetApplicationUserVisibleAppReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationUserVisibleAppResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_user_visible_app_req(request, options)
        )

    def get_application_app_list(
        self, request: GetApplicationAppListReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationAppListResp, Response]:
        return self.cli.raw_request(_gen_get_application_app_list_req(request, options))

    def update_application_app_visibility(
        self,
        request: UpdateApplicationAppVisibilityReq,
        options: typing.List[str] = None,
    ) -> typing.Tuple[UpdateApplicationAppVisibilityResp, Response]:
        return self.cli.raw_request(
            _gen_update_application_app_visibility_req(request, options)
        )

    def get_application_app_admin_user_list(
        self,
        request: GetApplicationAppAdminUserListReq,
        options: typing.List[str] = None,
    ) -> typing.Tuple[GetApplicationAppAdminUserListResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_app_admin_user_list_req(request, options)
        )

    def check_user_is_in_application_paid_scope(
        self,
        request: CheckUserIsInApplicationPaidScopeReq,
        options: typing.List[str] = None,
    ) -> typing.Tuple[CheckUserIsInApplicationPaidScopeResp, Response]:
        return self.cli.raw_request(
            _gen_check_user_is_in_application_paid_scope_req(request, options)
        )

    def get_application_order_list(
        self, request: GetApplicationOrderListReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationOrderListResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_order_list_req(request, options)
        )

    def get_application_order(
        self, request: GetApplicationOrderReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationOrderResp, Response]:
        return self.cli.raw_request(_gen_get_application_order_req(request, options))

    def get_application_usage_overview(
        self, request: GetApplicationUsageOverviewReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationUsageOverviewResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_usage_overview_req(request, options)
        )

    def get_application_usage_trend(
        self, request: GetApplicationUsageTrendReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationUsageTrendResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_usage_trend_req(request, options)
        )

    def get_application_usage_detail(
        self, request: GetApplicationUsageDetailReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationUsageDetailResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_usage_detail_req(request, options)
        )

    def get_application_message_overview(
        self,
        request: GetApplicationMessageOverviewReq,
        options: typing.List[str] = None,
    ) -> typing.Tuple[GetApplicationMessageOverviewResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_message_overview_req(request, options)
        )

    def get_application_message_trend(
        self, request: GetApplicationMessageTrendReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationMessageTrendResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_message_trend_req(request, options)
        )

    def get_application_message_detail(
        self, request: GetApplicationMessageDetailReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetApplicationMessageDetailResp, Response]:
        return self.cli.raw_request(
            _gen_get_application_message_detail_req(request, options)
        )
