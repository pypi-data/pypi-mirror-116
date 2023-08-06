import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.resource_list import NDSList
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import NDS, Filter1, LengthRange, NDSFilter, NDSItems

logger = logging.getLogger(__name__)


class NDSEventsAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

    def list(
        self,
        hole_start: Optional[LengthRange] = None,
        hole_end: Optional[LengthRange] = None,
        probabilities: Optional[List[int]] = None,
        severities: Optional[List[int]] = None,
        wellbore_external_ids: Optional[List[str]] = None,
        limit: Optional[int] = 100,
    ) -> NDSList:
        """
        Get NDS events that matches the filter

        @param hole_start - range of hole start in desired NDS events
        @param hole_end - range of hole end in desired NDS events
        @param probabilities - list of interested probabilities
        @param severities - list of interested severities
        @param wellbore_external_ids - list of interested wellbore external ids
        @return: NDSList object
        """

        def request(cursor):
            nds_filter = NDSFilter(
                filter=Filter1(
                    hole_start=hole_start,
                    hole_end=hole_end,
                    probabilities=probabilities,
                    severities=severities,
                    wellbore_external_ids=wellbore_external_ids,
                ),
                cursor=cursor,
            )

            path: str = self._get_path("/nds/list")
            response: Response = self.client.post(url_path=path, json=nds_filter.json())
            nds_items: NDSItems = NDSItems.parse_raw(response.text)
            return nds_items

        items = cursor_multi_request(
            get_cursor=self._get_cursor, get_items=self._get_items, limit=limit, request=request
        )
        return NDSList(items)

    def risk_types(self) -> List[str]:
        """
        Get all NDS risk types

        @return: list of NDS risk types
        """
        return self._string_items_from_route("nds/risktypes")

    @staticmethod
    def _get_items(nds_items: NDSItems) -> List[NDS]:
        items: List[NDS] = nds_items.items  # For mypy
        return items

    @staticmethod
    def _get_cursor(nds_items: NDSItems) -> Optional[str]:
        next_cursor: Optional[str] = nds_items.next_cursor  # For mypy
        return next_cursor
