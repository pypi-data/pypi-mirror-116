# Code generated by lark_sdk_gen. DO NOT EDIT.

import logging

import requests
from typing import Tuple

from pylark.api_service_auth import LarkAuthService
from pylark.api_service_contact import LarkContactService
from pylark.api_service_message import LarkMessageService
from pylark.api_service_chat import LarkChatService
from pylark.api_service_bot import LarkBotService
from pylark.api_service_calendar import LarkCalendarService
from pylark.api_service_drive import LarkDriveService
from pylark.api_service_bitable import LarkBitableService
from pylark.api_service_meeting_room import LarkMeetingRoomService
from pylark.api_service_vc import LarkVCService
from pylark.api_service_application import LarkApplicationService
from pylark.api_service_mail import LarkMailService
from pylark.api_service_approval import LarkApprovalService
from pylark.api_service_helpdesk import LarkHelpdeskService
from pylark.api_service_admin import LarkAdminService
from pylark.api_service_human_auth import LarkHumanAuthService
from pylark.api_service_ai import LarkAIService
from pylark.api_service_attendance import LarkAttendanceService
from pylark.api_service_file import LarkFileService
from pylark.api_service_okr import LarkOKRService
from pylark.api_service_ehr import LarkEHRService
from pylark.api_service_tenant import LarkTenantService
from pylark.api_service_search import LarkSearchService
from pylark.api_service_hire import LarkHireService
from pylark.api_service_task import LarkTaskService
from pylark.api_service_acs import LarkACSService

from pylark._internal_log import logger
from pylark.lark_request import RawRequestReq, Response, RawRequestDataClass, Request


class Lark(object):
    app_id: str
    app_secret: str
    custom_url: str
    custom_secret: str

    auth: LarkAuthService
    ai: LarkAIService

    def __init__(
        self,
        app_id="",
        app_secret="",
        custom_url="",
        custom_secret="",
    ):
        # service

        self.auth = LarkAuthService(cli=self)
        self.contact = LarkContactService(cli=self)
        self.message = LarkMessageService(cli=self)
        self.chat = LarkChatService(cli=self)
        self.bot = LarkBotService(cli=self)
        self.calendar = LarkCalendarService(cli=self)
        self.drive = LarkDriveService(cli=self)
        self.bitable = LarkBitableService(cli=self)
        self.meeting_room = LarkMeetingRoomService(cli=self)
        self.vc = LarkVCService(cli=self)
        self.application = LarkApplicationService(cli=self)
        self.mail = LarkMailService(cli=self)
        self.approval = LarkApprovalService(cli=self)
        self.helpdesk = LarkHelpdeskService(cli=self)
        self.admin = LarkAdminService(cli=self)
        self.human_auth = LarkHumanAuthService(cli=self)
        self.ai = LarkAIService(cli=self)
        self.attendance = LarkAttendanceService(cli=self)
        self.file = LarkFileService(cli=self)
        self.okr = LarkOKRService(cli=self)
        self.ehr = LarkEHRService(cli=self)
        self.tenant = LarkTenantService(cli=self)
        self.search = LarkSearchService(cli=self)
        self.hire = LarkHireService(cli=self)
        self.task = LarkTaskService(cli=self)
        self.acs = LarkACSService(cli=self)

        self.app_id = app_id
        self.app_secret = app_secret
        self.custom_secret = custom_secret
        self.custom_url = custom_url

    def with_tenant(self, tenant_key: str):
        pass

    def raw_request(self, req: RawRequestReq) -> Tuple[RawRequestDataClass, Response]:
        logger.info("[lark] %s#%s call api", req.scope, req.api)

        req.headers = self.prepare_headers(req)

        return Request.raw_request(cli=self, req=req)

    def prepare_headers(self, req: RawRequestReq) -> dict:
        headers = {}
        if req.method != "GET":
            headers["Content-Type"] = "application/json; charset=utf-8"

        if req.need_user_access_token and req.method_option.user_access_token != "":
            headers["Authorization"] = "Bearer " + req.method_option.user_access_token
        elif req.need_tenant_access_token:
            res, _ = self.auth.get_tenant_access_token()
            headers["Authorization"] = "Bearer " + res.token

        if req.need_helpdesk_access_token:
            headers[
                "X-Lark-Helpdesk-Authorization"
            ] = ""  # base64.StdEncoding.EncodeToString([]byte(r.helpdeskID + ":" + r.helpdeskToken))

        return headers

    def do_request(self, request_parm: RawRequestReq, real_response) -> Response:
        response = Response()
        real_req = self.parse_request_param(request_parm)

        response.method = real_req["method"]
        response.url = real_req["url"]
        response.header = real_req["header"]

        logger.debug("[lark] request %s#%s, %s %s, header=%s, body=%s", "")

        return response

    def parse_request_param(self, req: RawRequestReq):
        return {"method": "", "url": "", "header": {}}
