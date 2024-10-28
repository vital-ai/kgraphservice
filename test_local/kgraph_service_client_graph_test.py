import json
from ai_haley_kg_domain.model.KGEntity import KGEntity
from ai_haley_kg_domain.model.KGFrame import KGFrame
from ai_haley_kg_domain.model.KGSlot import KGSlot
from ai_haley_kg_domain.model.properties.Property_hasEntitySlotValue import Property_hasEntitySlotValue
from ai_haley_kg_domain.model.properties.Property_hasKGSlotType import Property_hasKGSlotType
from ai_haley_kg_domain.model.properties.Property_hasKGraphDescription import Property_hasKGraphDescription
from vital_ai_vitalsigns.metaql.arc.metaql_arc import ARC_TRAVERSE_TYPE_PROPERTY
from vital_ai_vitalsigns.metaql.query.query_builder import QueryBuilder, AndConstraintList, PropertyConstraint, \
    ConstraintType, ClassConstraint, Arc, OrConstraintList, NodeBind, EdgeBind, PathBind, PropertyPathList, \
    MetaQLPropertyPath, AndArcList, OrArcList, SolutionBind
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from vital_ai_vitalsigns_core.model.properties.Property_hasName import Property_hasName
from kgraphservice.kgraph_service_rest import KGraphServiceREST


def main():

    print('Test KGraphService Graph Query Client Test')

    vs = VitalSigns()

    print("VitalSigns Initialized")

    kgraphservice_rest = KGraphServiceREST()

    kgraph_list = kgraphservice_rest.list_kgraphs()

    for kgraph in kgraph_list:
        print(kgraph)

    wordnet_graph_uri = 'http://vital.ai/graph/wordnet-frames-graph-1'

    gq = (
        QueryBuilder.graph_query(
            offset=0,
            limit=100,
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

    print(gq)

    graph_query_json = json.dumps(gq, indent=4)

    print(f"Query JSON:\n{graph_query_json}")

    metaql_result = kgraphservice_rest.metaql_graph_query(graph_query=gq)

    print(metaql_result)

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
        go: GraphObject = re.graph_object
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
