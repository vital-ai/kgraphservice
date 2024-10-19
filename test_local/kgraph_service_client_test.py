from ai_haley_kg_domain.model.KGEntity import KGEntity
from ai_haley_kg_domain.model.properties.Property_hasKGraphDescription import Property_hasKGraphDescription
from vital_ai_vitalsigns.metaql.query.query_builder import QueryBuilder, AndConstraintList, PropertyConstraint, \
    ConstraintType, ClassConstraint, Arc, OrConstraintList, NodeBind, EdgeBind, PathBind, PropertyPathList, \
    MetaQLPropertyPath, AndArcList
from vital_ai_vitalsigns.model.VITAL_Edge import VITAL_Edge
from vital_ai_vitalsigns.model.VITAL_Node import VITAL_Node
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from vital_ai_vitalsigns_core.model.properties.Property_hasName import Property_hasName
from kgraphservice.kgraph_service_rest import KGraphServiceREST


def main():

    print('Test KGraphService Client')

    vs = VitalSigns()

    print("VitalSigns Initialized")

    kgraphservice_rest = KGraphServiceREST()

    kgraph_list = kgraphservice_rest.list_kgraphs()

    for kgraph in kgraph_list:
        print(kgraph)

    sq = (
        QueryBuilder.select_query(
            offset=0,
            limit=100
        )
        .graph_uri("http://vital.ai/graph/wordnet-frames-graph-1")
        .constraint_list(
            AndConstraintList()
            .node_constraint(
                PropertyConstraint(
                    property=Property_hasKGraphDescription.get_uri(),
                    comparator=ConstraintType.STRING_CONTAINS,
                    value="happy"
                )
            )
            .node_constraint(
                ClassConstraint(
                    clazz=KGEntity.get_class_uri()
                )
            )
        )
        .build()
    )

    print(sq)

    metaql_sq_query_results = kgraphservice_rest.metaql_select_query(select_query=sq)

    print(metaql_sq_query_results)

    result_list = metaql_sq_query_results.get_result_list()

    count = 0

    for re in result_list:
        graph_object = re.graph_object
        score = re.score
        uri = graph_object.URI
        name = graph_object.name
        count += 1

        print(f"({count}) GraphObject (score={score}): Name: {str(name)}, URI: {str(uri)} | {graph_object}")

    gq = (
        QueryBuilder.graph_query(
            limit=100,
            offset=0,
            resolve_objects=True
        )
        .graph_uri("urn:123")
        .arc(
            Arc()
            .constraint_list(
                OrConstraintList()
                .node_constraint(
                    PropertyConstraint(
                        property=Property_hasName.get_uri(),
                        comparator=ConstraintType.STRING_CONTAINS,
                        value="Alfred"
                    )
                )
                .node_constraint(
                    ClassConstraint(
                        clazz=VITAL_Node.get_class_uri()
                    )
                )
            )
            .node_bind(NodeBind(name="node1"))
            .edge_bind(EdgeBind(name="edge1"))
            .path_bind(PathBind(name="path1"))
            .arc(
                Arc()
                .constraint_list(
                    AndConstraintList()
                    .node_constraint(
                        PropertyConstraint(
                            property=Property_hasName.get_uri(),
                            comparator=ConstraintType.STRING_CONTAINS,
                            value="Betty"
                        )
                    )
                    .edge_constraint(
                        ClassConstraint(
                            clazz=VITAL_Edge.get_class_uri()
                        )
                    )
                )
                .property_path_list(
                    PropertyPathList()
                    .property_path(
                        MetaQLPropertyPath(
                            property_uri=Property_hasName.get_uri(),
                        )
                    )
                )
                .arc_list(
                    AndArcList()
                    .arc(
                        Arc()
                        .node_bind(NodeBind(name="node2"))
                        .edge_bind(EdgeBind(name="edge2"))
                        .path_bind(PathBind(name="path2"))
                        .constraint_list(
                            AndConstraintList()
                            .node_constraint(
                                PropertyConstraint(
                                    property=Property_hasName.get_uri(),
                                    comparator=ConstraintType.STRING_CONTAINS,
                                    value="David"
                                )
                            )
                            .node_constraint(
                                ClassConstraint(
                                    clazz=VITAL_Node.get_class_uri()
                                )
                            )
                        )
                    )
                )
                .arc(
                    Arc()
                    .constraint_list(
                        AndConstraintList()
                        .node_constraint(
                            PropertyConstraint(
                                property=Property_hasName.get_uri(),
                                comparator=ConstraintType.STRING_CONTAINS,
                                value="Charles"
                            )
                        )
                        .node_constraint(
                            ClassConstraint(
                                clazz=VITAL_Node.get_class_uri()
                            )
                        )
                    )
                )
            )
        )
        .build()
    )

    # print(gq)

    # metaql_gq_query_results = kgraphservice_rest.metaql_graph_query(graph_query=gq)

    # print(metaql_gq_query_results)


if __name__ == "__main__":
    main()
