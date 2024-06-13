from typing import List, TypeVar, Type, Tuple, Optional
from ai_haley_kg_domain.model.KGInteraction import KGInteraction
from ai_haley_kg_domain.model.KGNode import KGNode
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.query.part_list import PartList
from vital_ai_vitalsigns.query.result_list import ResultList
from vital_ai_vitalsigns.service.vital_namespace import VitalNamespace
from vital_ai_vitalsigns.service.vital_service import VitalService
from vital_ai_vitalsigns.service.vital_service_status import VitalServiceStatus
from kgraphservice.part.kgframe_part import KGFramePart

G = TypeVar('G', bound=Optional[GraphObject])
KGN = TypeVar('KGN', bound=Optional[KGNode])
KGFP = TypeVar('KGFP', bound=Optional[KGFramePart])


# notes:
# define primary vector for kg objects and secondary vector
# for the type of the object
# use naming convention _vector and _type_vector
# see: https://weaviate.io/developers/weaviate/config-refs/schema/multi-vector


class KGraphService:
    def __init__(self, vital_service: VitalService):
        self.vital_service = vital_service

    def get_graph(self, graph_uri: str) -> VitalNamespace:
        return self.vital_service.get_graph(graph_uri)

    def list_graphs(self) -> List[VitalNamespace]:
        return self.vital_service.list_graphs()

    def check_create_graph(self, graph_uri: str) -> bool:
        return self.vital_service.check_create_graph(graph_uri)

    def create_graph(self, graph_uri: str) -> bool:
        return self.vital_service.create_graph(graph_uri)

    def delete_graph(self, graph_uri: str) -> bool:
        return self.vital_service.delete_graph(graph_uri)

    def purge_graph(self, graph_uri: str) -> bool:
        return self.vital_service.purge_graph(graph_uri)

    def get_graph_all_objects(self, graph_uri: str, limit=100, offset=0) -> ResultList:
        return self.vital_service.get_graph_all_objects(graph_uri, limit=limit, offset=offset)

    def insert_object(self, graph_uri: str, graph_object: G) -> VitalServiceStatus:
        return self.vital_service.insert_object(graph_uri, graph_object)

    def insert_object_list(self, graph_uri: str, graph_object_list: List[G]) -> VitalServiceStatus:
        return self.vital_service.insert_object_list(graph_uri, graph_object_list)

    def update_object(self, graph_object: G, graph_uri: str) -> VitalServiceStatus:
        return self.vital_service.update_object(graph_object, graph_uri)

    def update_object_list(self, graph_object_list: List[G], graph_uri: str) -> VitalServiceStatus:
        return self.vital_service.update_object_list(graph_object_list, graph_uri)

    def get_object(self, object_uri: str, graph_uri: str | None = None) -> G:
        return self.vital_service.get_object(object_uri, graph_uri)

    def get_object_list(self, object_uri_list: List[str], graph_uri: str | None = None) -> ResultList:
        return self.vital_service.get_object_list(object_uri_list, graph_uri)

    def delete_object(self, object_uri: str, graph_uri: str | None = None) -> VitalServiceStatus:
        return self.vital_service.delete_object(object_uri, graph_uri)

    def delete_object_list(self, object_uri_list: List[str], graph_uri: str | None = None) -> VitalServiceStatus:
        return self.vital_service.delete_object_list(object_uri_list, graph_uri)

    def filter_query(self, graph_uri: str, sparql_query: str) -> ResultList:
        return self.vital_service.filter_query(graph_uri, sparql_query)

    def query(self, graph_uri: str, sparql_query: str) -> ResultList:
        return self.vital_service.query(sparql_query, graph_uri)

    # Tuple[binding name, property uri]
    def query_construct(self, graph_uri: str, sparql_query: str, binding_list: List[Tuple[str, str]]) -> ResultList:
        pass

    def get_interaction_list(self, graph_uri: str, limit=100, offset=0) -> ResultList:
        pass

    def get_interaction_graph(self, graph_uri: str, interaction: KGInteraction, limit=100, offset=0) -> ResultList:
        pass

    def get_interaction_frames(self, graph_uri: str, interaction: KGInteraction, limit=100, offset=0) -> PartList:
        pass

    def get_interaction_nodes(self, graph_uri: str, interaction: KGInteraction, kgnode_type: Type[KGN], limit=100, offset=0) -> ResultList:
        pass

    def get_frame(self, graph_uri: str, frame_uri: str, limit=100, offset=0) -> KGFP:
        pass

    def get_frames(self, graph_uri: str, frame_uri_list: List[str], limit=100, offset=0) -> PartList:
        pass

    def get_frame_id(self, graph_uri: str, frame_id: str, limit=100, offset=0) -> KGFP:
        pass

    def get_frames_id(self, graph_uri: str, frame_id_list: List[str], limit=100, offset=0) -> PartList:
        pass

    def get_frames_root(self, graph_uri: str, root_uri: str, limit=100, offset=0) -> PartList:
        pass

    def get_graph_objects_type(self, graph_uri: str, class_uri: str, include_subclasses=True, limit=100, offset=0) -> ResultList:
        pass

    def get_graph_objects_tag(self, graph_uri: str, kg_graph_uri: str, limit=100, offset=0) -> ResultList:
        pass

    def delete_frame(self, graph_uri: str, frame_uri: str) -> VitalServiceStatus:
        pass

    def delete_frames(self, graph_uri: str, frame_uri_list: List[str]) -> VitalServiceStatus:
        pass

    def delete_frame_id(self, graph_uri: str, frame_id: str) -> VitalServiceStatus:
        pass

    def delete_frames_id(self, graph_uri: str, frame_id_list: List[str]) -> VitalServiceStatus:
        pass

    def delete_graph_objects_tag(self, graph_uri: str, kg_graph_uri: str) -> VitalServiceStatus:
        pass
