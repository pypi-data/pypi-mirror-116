from AsteriskRealtimeData.domain.call.call_update_vo import CallUpdateVo
from AsteriskRealtimeData.application.call_service import CallService
from AsteriskRealtimeData.domain.call.call_vo import CallVo


class CallController:
    def create(self, call_vo: CallVo) -> CallVo:
        return CallService().create_call(call_vo)

    def update(self, call_update_vo: CallUpdateVo) -> CallVo:
        return CallService().update_call(call_update_vo)

    def list(self) -> list[dict]:
        calls = CallService().list_call()
        result: list = []

        for call in calls:
            result.append(call.as_dict())

        return result

    def get_by_call_linkedid(self, call_linkedid: str) -> dict:
        return CallService().get_call(call_linkedid).as_dict()

    def get_by_search_criteria(self, search_criteria: str) -> dict:
        return CallService().get_by_search_criteria(search_criteria).as_dict()

    def delete_by_call_linkedid(self, call_linkedid: str) -> dict:
        CallService().delete_call(call_linkedid)
