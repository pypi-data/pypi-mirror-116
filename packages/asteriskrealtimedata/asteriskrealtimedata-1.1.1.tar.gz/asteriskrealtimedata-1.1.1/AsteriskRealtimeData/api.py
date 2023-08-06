from AsteriskRealtimeData.domain.call.call_update_vo import CallUpdateVo
from AsteriskRealtimeData.domain.queue_status.queue_status_update_vo import QueueStatusUpdateVo
from AsteriskRealtimeData.domain.peer.peer_update_vo import PeerUpdateVo
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_update_vo import MascaraIpaddressUpdateVo
from AsteriskRealtimeData.domain.pause_reason.pause_reason_update_vo import PauseReasonUpdateVo
from AsteriskRealtimeData.domain.call.call_vo import CallVo
from AsteriskRealtimeData.domain.queue_status.queue_status_vo import QueueStatusVo
from AsteriskRealtimeData.domain.peer.peer_vo import PeerVo
from AsteriskRealtimeData.domain.queue_member.queue_member_vo import QueueMemberVo
from AsteriskRealtimeData.domain.mascara_ipaddress.mascara_ipaddress_vo import MascaraIpaddressVo
from AsteriskRealtimeData.domain.pause_reason.pause_reasons_vo import PauseReasonVo
from AsteriskRealtimeData.infrastructure.api.pause_reason_controller import PauseReasonController
from AsteriskRealtimeData.infrastructure.api.mascara_ipaddress_controller import MascaraIpaddressController
from AsteriskRealtimeData.infrastructure.api.queue_member_controller import QueueMemberController
from AsteriskRealtimeData.infrastructure.api.peer_controller import PeerController
from AsteriskRealtimeData.infrastructure.api.queue_status_controller import QueueStatusController
from AsteriskRealtimeData.infrastructure.api.call_controller import CallController


class Api:
    class PauseReason:
        @staticmethod
        def create(pause_reason: PauseReasonVo):
            return PauseReasonController().create(pause_reason)

        @staticmethod
        def update(pause_reason: PauseReasonUpdateVo):
            return PauseReasonController().update(pause_reason)

        @staticmethod
        def list():
            return PauseReasonController().list()

        @staticmethod
        def get_by_pause_code(pause_code: str):
            return PauseReasonController().get_by_pause_code(pause_code)

        @staticmethod
        def get_by_search_criteria(search_criteria: dict):
            return PauseReasonController().get_by_search_criteria(search_criteria)

        @staticmethod
        def delete_by_pause_code(pause_code: str):
            PauseReasonController().delete_by_pause_code(pause_code)

    class MascaraIpaddress:
        @staticmethod
        def create(mascara_ipaddress: MascaraIpaddressVo):
            return MascaraIpaddressController().create(mascara_ipaddress)

        @staticmethod
        def update(mascara_ipaddress: MascaraIpaddressUpdateVo):
            return MascaraIpaddressController().update(mascara_ipaddress)

        @staticmethod
        def list():
            return MascaraIpaddressController().list()

        @staticmethod
        def get_by_ipaddress(mascara_ipaddress: str):
            return MascaraIpaddressController().get_by_ipaddress(mascara_ipaddress)

        @staticmethod
        def get_by_search_criteria(search_criteria: dict):
            return MascaraIpaddressController().get_by_search_criteria(search_criteria)

        @staticmethod
        def delete_by_ipaddress(mascara_ipaddress: str):
            MascaraIpaddressController().delete_by_ipaddress(mascara_ipaddress)

    class QueueMember:
        @staticmethod
        def create(queue_member: QueueMemberVo):
            return QueueMemberController().create(queue_member)

        @staticmethod
        def update(queue_member_update_vo: QueueStatusUpdateVo):
            return QueueMemberController().update(queue_member_update_vo)

        @staticmethod
        def list():
            return QueueMemberController().list()

        @staticmethod
        def get_by_peer(peer: str):
            return QueueMemberController().get_by_peer(peer)

        @staticmethod
        def get_by_search_criteria(search_criteria: dict):
            return QueueMemberController().get_by_search_criteria(search_criteria)

        @staticmethod
        def delete_by_peer(peer: str):
            QueueMemberController().delete_by_peer(peer)

    class Peer:
        @staticmethod
        def create(peer: PeerVo):
            return PeerController().create(peer)

        @staticmethod
        def update(peer: PeerUpdateVo):
            return PeerController().update(peer)

        @staticmethod
        def list():
            return PeerController().list()

        @staticmethod
        def get_by_peer(peer: str):
            return PeerController().get_by_peer(peer)

        @staticmethod
        def get_by_search_criteria(search_criteria: dict):
            return PeerController().get_by_search_criteria(search_criteria)

        @staticmethod
        def delete_by_peer(peer: str):
            PeerController().delete_by_peer(peer)

    class QueueStatus:
        @staticmethod
        def create(queue_status: QueueStatusVo):
            return QueueStatusController().create(queue_status)

        def update(queue_status_update_vo: QueueStatusUpdateVo):
            return QueueStatusController().update(queue_status_update_vo)

        @staticmethod
        def list():
            return QueueStatusController().list()

        @staticmethod
        def get_by_status_code(status_code: str):
            return QueueStatusController().get_by_status_code(status_code)

        @staticmethod
        def get_by_search_criteria(search_criteria: dict):
            return QueueStatusController().get_by_search_criteria(search_criteria)

        @staticmethod
        def delete_by_status_code(status_code: str):
            QueueStatusController().delete_by_status_code(status_code)

    class Call:
        @staticmethod
        def create(call: CallVo):
            return CallController().create(call)

        @staticmethod
        def update(call_update_vo: CallUpdateVo):
            return CallController().update(call_update_vo)

        @staticmethod
        def list():
            return CallController().list()

        @staticmethod
        def get_by_call_linkedid(call_linkedid: str):
            return CallController().get_by_call_linkedid(call_linkedid)

        @staticmethod
        def get_by_search_criteria(search_criteria: dict):
            return CallController().get_by_search_criteria(search_criteria)

        @staticmethod
        def delete_by_call_linkedid(call_linkedid: str):
            CallController().delete_by_call_linkedid(call_linkedid)
