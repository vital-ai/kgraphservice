from typing import List, Optional, TypeVar
from ai_haley_kg_domain.model.KGFrame import KGFrame
from ai_haley_kg_domain.model.KGSlot import KGSlot
from vital_ai_vitalsigns.collection.graph_collection import GraphCollection
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from kgraphservice.part.kgnode_part import KGNodePart

G = TypeVar('G', bound=Optional[GraphObject])


class KGFramePart(KGNodePart):

    def __init__(self, *, data: List[G] = [], score: float = 1.0,
                 base: G = None,
                 in_edge: G = None,
                 graph_collection: GraphCollection | None = None):

        super().__init__(data=data, score=score,
                         base=base,
                         in_edge=in_edge,
                         graph_collection=graph_collection)

    def get_kgslots(self) -> List[KGSlot]:
        kgframe = self.get_kgframe()
        # todo check if frame exists
        # enforce slots connected to this frame

        return [item for item in self if isinstance(item, KGSlot)]

    def get_kgframe(self) -> Optional[KGFrame]:
        kg_frames = [item for item in self if isinstance(item, KGFrame)]
        if len(kg_frames) == 1:
            return kg_frames[0]
        return None



