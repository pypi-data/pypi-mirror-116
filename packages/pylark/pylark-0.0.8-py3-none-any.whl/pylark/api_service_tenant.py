# Code generated by lark_sdk_gen. DO NOT EDIT.

import typing
from pylark.lark_request import Response

from pylark.api_service_tenant_tenant_get import (
    GetTenantReq,
    GetTenantResp,
    _gen_get_tenant_req,
)


if typing.TYPE_CHECKING:
    from lark import Lark


class LarkTenantService(object):
    cli: "Lark"

    def __init__(self, cli: "Lark"):
        self.cli = cli

    def get_tenant(
        self, request: GetTenantReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetTenantResp, Response]:
        return self.cli.raw_request(_gen_get_tenant_req(request, options))
