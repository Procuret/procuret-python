"""
Procuret Python
Human Headine Module
author: hugh@blinkybeach.com
"""
from procuret.data.codable import Codable, CodingDefinition as CD


class HumanHeadline(Codable):

    coding_map = {
        'agent_id': CD(int),
        'full_name': CD(str)
    }

    def __init__(
        self,
        agent_id: int,
        full_name: str
    ) -> None:

        self._agent_id = agent_id
        self._full_name = full_name

        return

    full_name = property(lambda s: s._full_name)
    agent_id = property(lambda s: s._agent_id)
