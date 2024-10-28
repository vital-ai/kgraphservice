import json
from typing import List
from ai_haley_kg_domain.model.KGEntity import KGEntity
from ai_haley_kg_domain.model.KGFrame import KGFrame
from ai_haley_kg_domain.model.KGSlot import KGSlot
from ai_haley_kg_domain.model.properties.Property_hasEntitySlotValue import Property_hasEntitySlotValue
from ai_haley_kg_domain.model.properties.Property_hasKGSlotType import Property_hasKGSlotType
from ai_haley_kg_domain.model.properties.Property_hasKGraphDescription import Property_hasKGraphDescription
from vital_ai_vitalsigns.metaql.arc.metaql_arc import ARC_TRAVERSE_TYPE_PROPERTY
from vital_ai_vitalsigns.metaql.query.query_builder import QueryBuilder, Arc, AndConstraintList, PropertyConstraint, \
    ConstraintType, ClassConstraint, OrConstraintList, PropertyPathList, AndArcList, MetaQLPropertyPath, NodeBind, \
    EdgeBind, PathBind, OrArcList, SolutionBind, GraphQuery
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.ontology.ontology import Ontology
from vital_ai_vitalsigns.service.graph.virtuoso_service import VirtuosoGraphService
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from vital_ai_vitalsigns_core.model.properties.Property_hasName import Property_hasName


class DictEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)


def main():

    print('Test MetaQL Graph Query')

    vs = VitalSigns()

    print("VitalSigns Initialized")

    config = vs.get_config()

    wordnet_graph_uri = 'http://vital.ai/graph/wordnet-frames-graph-1'

    gq = (
        QueryBuilder.graph_query(
            offset=0,
            limit=10,
            resolve_objects=True
        )
        .graph_uri(wordnet_graph_uri)
        .arc(
            Arc()
            .node_bind(NodeBind(name="frame"))
            .constraint_list(
                AndConstraintList()
                .node_constraint(
                    ClassConstraint(
                        clazz=KGFrame.get_class_uri()
                    )
                )
            )
            .arc_list(
                OrArcList()
                .arc_list(
                    AndArcList()
                    .arc(
                        Arc()
                        .node_bind(NodeBind(name="source_slot"))
                        .edge_bind(EdgeBind(name="source_slot_edge"))
                        .constraint_list(
                            AndConstraintList()
                            .node_constraint(
                                PropertyConstraint(
                                    property=Property_hasKGSlotType.get_uri(),
                                    comparator=ConstraintType.EQUAL_TO,
                                    value="urn:hasSourceEntity"
                                )
                            )
                            .node_constraint(
                                ClassConstraint(
                                    clazz=KGSlot.get_class_uri(),
                                    include_subclasses=True
                                )
                            )
                        )
                        .arc(
                            Arc(arc_traverse_type=ARC_TRAVERSE_TYPE_PROPERTY)
                            .solution_bind(SolutionBind(name="entity"))
                            .node_bind(NodeBind(name="source_entity"))  # source_entity
                            .path_bind(PathBind(name="source_entity_path"))
                            .property_path_list(
                                PropertyPathList()
                                .property_path(
                                    MetaQLPropertyPath(
                                        property_uri=Property_hasEntitySlotValue.get_uri()
                                    )
                                )
                            )
                            .constraint_list(
                                OrConstraintList()
                                .node_constraint(
                                    PropertyConstraint(
                                        property=Property_hasKGraphDescription.get_uri(),
                                        comparator=ConstraintType.STRING_CONTAINS,
                                        value="happy"
                                    )
                                )
                                .node_constraint(
                                    PropertyConstraint(
                                        property=Property_hasName.get_uri(),
                                        comparator=ConstraintType.STRING_CONTAINS,
                                        value="happy"
                                    )
                                )
                            )
                            .constraint_list(
                                AndConstraintList()
                                .node_constraint(
                                    ClassConstraint(
                                        clazz=KGEntity.get_class_uri()
                                    )
                                )
                            )
                        )
                    )
                    .arc(
                        Arc()
                        .node_bind(NodeBind(name="destination_slot"))
                        .edge_bind(EdgeBind(name="destination_slot_edge"))
                        .constraint_list(
                            AndConstraintList()
                            .node_constraint(
                                PropertyConstraint(
                                    property=Property_hasKGSlotType.get_uri(),
                                    comparator=ConstraintType.EQUAL_TO,
                                    value="urn:hasDestinationEntity"
                                )
                            )
                            .node_constraint(
                                ClassConstraint(
                                    clazz=KGSlot.get_class_uri(),
                                    include_subclasses=True
                                )
                            )
                        )
                        .arc(
                            Arc(arc_traverse_type=ARC_TRAVERSE_TYPE_PROPERTY)
                            .node_bind(NodeBind(name="destination_entity"))
                            .path_bind(PathBind(name="destination_entity_path"))
                            .property_path_list(
                                PropertyPathList()
                                .property_path(
                                    MetaQLPropertyPath(
                                        property_uri=Property_hasEntitySlotValue.get_uri()
                                    )
                                )
                            )
                            .constraint_list(
                                AndConstraintList()
                                .node_constraint(
                                    ClassConstraint(
                                        clazz=KGEntity.get_class_uri()
                                    )
                                )
                            )
                        )
                    )
                )
                .arc_list(
                    AndArcList()
                    .arc(
                        Arc()
                        .node_bind(NodeBind(name="source_slot"))
                        .edge_bind(EdgeBind(name="source_slot_edge"))
                        .constraint_list(
                            AndConstraintList()
                            .node_constraint(
                                PropertyConstraint(
                                    property=Property_hasKGSlotType.get_uri(),
                                    comparator=ConstraintType.EQUAL_TO,
                                    value="urn:hasSourceEntity"
                                )
                            )
                            .node_constraint(
                                ClassConstraint(
                                    clazz=KGSlot.get_class_uri(),
                                    include_subclasses=True
                                )
                            )
                        )
                        .arc(
                            Arc(arc_traverse_type=ARC_TRAVERSE_TYPE_PROPERTY)
                            .node_bind(NodeBind(name="source_entity"))
                            .path_bind(PathBind(name="source_entity_path"))
                            .property_path_list(
                                PropertyPathList()
                                .property_path(
                                    MetaQLPropertyPath(
                                        property_uri=Property_hasEntitySlotValue.get_uri()
                                    )
                                )
                            )
                            .constraint_list(
                                AndConstraintList()
                                .node_constraint(
                                    ClassConstraint(
                                        clazz=KGEntity.get_class_uri()
                                    )
                                )
                            )
                        )
                    )
                    .arc(
                        Arc()
                        .node_bind(NodeBind(name="destination_slot"))
                        .edge_bind(EdgeBind(name="destination_slot_edge"))
                        .constraint_list(
                            AndConstraintList()
                            .node_constraint(
                                PropertyConstraint(
                                    property=Property_hasKGSlotType.get_uri(),
                                    comparator=ConstraintType.EQUAL_TO,
                                    value="urn:hasDestinationEntity"
                                )
                            )
                            .node_constraint(
                                ClassConstraint(
                                    clazz=KGSlot.get_class_uri(),
                                    include_subclasses=True
                                )
                            )
                        )
                        .arc(
                            Arc(arc_traverse_type=ARC_TRAVERSE_TYPE_PROPERTY)
                            .solution_bind(SolutionBind(name="entity"))
                            .node_bind(NodeBind(name="destination_entity"))  # destination_entity
                            .path_bind(PathBind(name="destination_entity_path"))
                            .property_path_list(
                                PropertyPathList()
                                .property_path(
                                    MetaQLPropertyPath(
                                        property_uri=Property_hasEntitySlotValue.get_uri()
                                    )
                                )
                            )
                            .constraint_list(
                                OrConstraintList()
                                .node_constraint(
                                    PropertyConstraint(
                                        property=Property_hasKGraphDescription.get_uri(),
                                        comparator=ConstraintType.STRING_CONTAINS,
                                        value="happy"
                                    )
                                )
                                .node_constraint(
                                    PropertyConstraint(
                                        property=Property_hasName.get_uri(),
                                        comparator=ConstraintType.STRING_CONTAINS,
                                        value="happy"
                                    )
                                )
                            )
                            .constraint_list(
                                AndConstraintList()
                                .node_constraint(
                                    ClassConstraint(
                                        clazz=KGEntity.get_class_uri()
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        .build()
    )

    graph_query_json = json.dumps(gq, indent=4)

    print(f"Query JSON:\n{graph_query_json}")

    vitalservice_manager = vs.get_vitalservice_manager()

    vitalservice_name_list = vitalservice_manager.get_vitalservice_list()

    for vitalservice_name in vitalservice_name_list:
        print(vitalservice_name)

    vitalservice = vitalservice_manager.get_vitalservice("local_service")

    graph_list = vitalservice.list_graphs()

    for g in graph_list:
        print(f"Graph URI: {g.get_namespace()}")

    metaql_class = gq.get('metaql_class', None)

    if metaql_class == "GraphQuery":
        print("Query is a GraphQuery")

    if metaql_class == "SelectQuery":
        print("Query is a SelectQuery")

    metaql_result = vitalservice.metaql_graph_query(
        graph_query=gq
    )

    # print(metaql_result)

    binding_list = metaql_result.get_binding_list()

    print(f"Binding List: {binding_list}")

    result_object_list = metaql_result.get_result_object_list()

    object_map = {}

    for go in result_object_list:
        print(f"Result Object: {go.to_json()}")
        uri = str(go.URI)
        object_map[uri] = go

    rl = metaql_result.get_result_list()

    for re in rl:
        print(f"ResultElement: {re}")
        go:GraphObject = re.graph_object
        print(f"ResultElement GraphMatch GO: {go.to_json(pretty_print=False)}")

        for b in binding_list:
            b_uri = str(go[b])
            bind_object: GraphObject = object_map.get(b_uri, None)
            if bind_object:
                print(f"Binding: {b} => {bind_object.to_json(pretty_print=False)}")
            else:
                print(f"Binding: {b} => URI: {b_uri}")


if __name__ == "__main__":
    main()
