# Code generated by lark_sdk_gen. DO NOT EDIT.

import typing
from pylark.lark_request import Response

from pylark.api_service_hire_job_get import (
    GetHireJobReq,
    GetHireJobResp,
    _gen_get_hire_job_req,
)
from pylark.api_service_hire_job_manager_get import (
    GetHireJobManagerReq,
    GetHireJobManagerResp,
    _gen_get_hire_job_manager_req,
)
from pylark.api_service_hire_talent_get import (
    GetHireTalentReq,
    GetHireTalentResp,
    _gen_get_hire_talent_req,
)
from pylark.api_service_hire_attachment_get import (
    GetHireAttachmentReq,
    GetHireAttachmentResp,
    _gen_get_hire_attachment_req,
)
from pylark.api_service_hire_attachment_preview_get import (
    GetHireAttachmentPreviewReq,
    GetHireAttachmentPreviewResp,
    _gen_get_hire_attachment_preview_req,
)
from pylark.api_service_hire_resume_sources_get import (
    GetHireResumeSourceReq,
    GetHireResumeSourceResp,
    _gen_get_hire_resume_source_req,
)
from pylark.api_service_hire_note_create import (
    CreateHireNoteReq,
    CreateHireNoteResp,
    _gen_create_hire_note_req,
)
from pylark.api_service_hire_note_update import (
    UpdateHireNoteReq,
    UpdateHireNoteResp,
    _gen_update_hire_note_req,
)
from pylark.api_service_hire_note_get import (
    GetHireNoteReq,
    GetHireNoteResp,
    _gen_get_hire_note_req,
)
from pylark.api_service_hire_note_list import (
    GetHireNoteListReq,
    GetHireNoteListResp,
    _gen_get_hire_note_list_req,
)
from pylark.api_service_hire_referral_get_by_application import (
    GetHireReferralByApplicationReq,
    GetHireReferralByApplicationResp,
    _gen_get_hire_referral_by_application_req,
)
from pylark.api_service_hire_job_process_list import (
    GetHireJobProcessListReq,
    GetHireJobProcessListResp,
    _gen_get_hire_job_process_list_req,
)
from pylark.api_service_hire_application_create import (
    CreateHireApplicationReq,
    CreateHireApplicationResp,
    _gen_create_hire_application_req,
)
from pylark.api_service_hire_application_terminate import (
    TerminateHireApplicationReq,
    TerminateHireApplicationResp,
    _gen_terminate_hire_application_req,
)
from pylark.api_service_hire_application_get import (
    GetHireApplicationReq,
    GetHireApplicationResp,
    _gen_get_hire_application_req,
)
from pylark.api_service_hire_application_list import (
    GetHireApplicationListReq,
    GetHireApplicationListResp,
    _gen_get_hire_application_list_req,
)
from pylark.api_service_hire_application_interview_list import (
    GetHireApplicationInterviewListReq,
    GetHireApplicationInterviewListResp,
    _gen_get_hire_application_interview_list_req,
)
from pylark.api_service_hire_offer_get_by_application import (
    GetHireOfferByApplicationReq,
    GetHireOfferByApplicationResp,
    _gen_get_hire_offer_by_application_req,
)
from pylark.api_service_hire_offer_schema_get import (
    GetHireOfferSchemaReq,
    GetHireOfferSchemaResp,
    _gen_get_hire_offer_schema_req,
)
from pylark.api_service_hire_transfer_onboard_by_application import (
    MakeHireTransferOnboardByApplicationReq,
    MakeHireTransferOnboardByApplicationResp,
    _gen_make_hire_transfer_onboard_by_application_req,
)
from pylark.api_service_hire_employee_update import (
    UpdateHireEmployeeReq,
    UpdateHireEmployeeResp,
    _gen_update_hire_employee_req,
)
from pylark.api_service_hire_employee_get_by_application import (
    GetHireEmployeeByApplicationReq,
    GetHireEmployeeByApplicationResp,
    _gen_get_hire_employee_by_application_req,
)
from pylark.api_service_hire_employee_get import (
    GetHireEmployeeReq,
    GetHireEmployeeResp,
    _gen_get_hire_employee_req,
)


if typing.TYPE_CHECKING:
    from lark import Lark


class LarkHireService(object):
    cli: "Lark"

    def __init__(self, cli: "Lark"):
        self.cli = cli

    def get_hire_job(
        self, request: GetHireJobReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireJobResp, Response]:
        return self.cli.raw_request(_gen_get_hire_job_req(request, options))

    def get_hire_job_manager(
        self, request: GetHireJobManagerReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireJobManagerResp, Response]:
        return self.cli.raw_request(_gen_get_hire_job_manager_req(request, options))

    def get_hire_talent(
        self, request: GetHireTalentReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireTalentResp, Response]:
        return self.cli.raw_request(_gen_get_hire_talent_req(request, options))

    def get_hire_attachment(
        self, request: GetHireAttachmentReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireAttachmentResp, Response]:
        return self.cli.raw_request(_gen_get_hire_attachment_req(request, options))

    def get_hire_attachment_preview(
        self, request: GetHireAttachmentPreviewReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireAttachmentPreviewResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_attachment_preview_req(request, options)
        )

    def get_hire_resume_source(
        self, request: GetHireResumeSourceReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireResumeSourceResp, Response]:
        return self.cli.raw_request(_gen_get_hire_resume_source_req(request, options))

    def create_hire_note(
        self, request: CreateHireNoteReq, options: typing.List[str] = None
    ) -> typing.Tuple[CreateHireNoteResp, Response]:
        return self.cli.raw_request(_gen_create_hire_note_req(request, options))

    def update_hire_note(
        self, request: UpdateHireNoteReq, options: typing.List[str] = None
    ) -> typing.Tuple[UpdateHireNoteResp, Response]:
        return self.cli.raw_request(_gen_update_hire_note_req(request, options))

    def get_hire_note(
        self, request: GetHireNoteReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireNoteResp, Response]:
        return self.cli.raw_request(_gen_get_hire_note_req(request, options))

    def get_hire_note_list(
        self, request: GetHireNoteListReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireNoteListResp, Response]:
        return self.cli.raw_request(_gen_get_hire_note_list_req(request, options))

    def get_hire_referral_by_application(
        self, request: GetHireReferralByApplicationReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireReferralByApplicationResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_referral_by_application_req(request, options)
        )

    def get_hire_job_process_list(
        self, request: GetHireJobProcessListReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireJobProcessListResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_job_process_list_req(request, options)
        )

    def create_hire_application(
        self, request: CreateHireApplicationReq, options: typing.List[str] = None
    ) -> typing.Tuple[CreateHireApplicationResp, Response]:
        return self.cli.raw_request(_gen_create_hire_application_req(request, options))

    def terminate_hire_application(
        self, request: TerminateHireApplicationReq, options: typing.List[str] = None
    ) -> typing.Tuple[TerminateHireApplicationResp, Response]:
        return self.cli.raw_request(
            _gen_terminate_hire_application_req(request, options)
        )

    def get_hire_application(
        self, request: GetHireApplicationReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireApplicationResp, Response]:
        return self.cli.raw_request(_gen_get_hire_application_req(request, options))

    def get_hire_application_list(
        self, request: GetHireApplicationListReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireApplicationListResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_application_list_req(request, options)
        )

    def get_hire_application_interview_list(
        self,
        request: GetHireApplicationInterviewListReq,
        options: typing.List[str] = None,
    ) -> typing.Tuple[GetHireApplicationInterviewListResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_application_interview_list_req(request, options)
        )

    def get_hire_offer_by_application(
        self, request: GetHireOfferByApplicationReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireOfferByApplicationResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_offer_by_application_req(request, options)
        )

    def get_hire_offer_schema(
        self, request: GetHireOfferSchemaReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireOfferSchemaResp, Response]:
        return self.cli.raw_request(_gen_get_hire_offer_schema_req(request, options))

    def make_hire_transfer_onboard_by_application(
        self,
        request: MakeHireTransferOnboardByApplicationReq,
        options: typing.List[str] = None,
    ) -> typing.Tuple[MakeHireTransferOnboardByApplicationResp, Response]:
        return self.cli.raw_request(
            _gen_make_hire_transfer_onboard_by_application_req(request, options)
        )

    def update_hire_employee(
        self, request: UpdateHireEmployeeReq, options: typing.List[str] = None
    ) -> typing.Tuple[UpdateHireEmployeeResp, Response]:
        return self.cli.raw_request(_gen_update_hire_employee_req(request, options))

    def get_hire_employee_by_application(
        self, request: GetHireEmployeeByApplicationReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireEmployeeByApplicationResp, Response]:
        return self.cli.raw_request(
            _gen_get_hire_employee_by_application_req(request, options)
        )

    def get_hire_employee(
        self, request: GetHireEmployeeReq, options: typing.List[str] = None
    ) -> typing.Tuple[GetHireEmployeeResp, Response]:
        return self.cli.raw_request(_gen_get_hire_employee_req(request, options))
