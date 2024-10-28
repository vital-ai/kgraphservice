import json
from typing import List

from vital_ai_vitalsigns.metaql.metaql_builder import MetaQLBuilder
from vital_ai_vitalsigns.metaql.metaql_parser import MetaQLParser
from vital_ai_vitalsigns.metaql.metaql_status import OK_STATUS_TYPE
from vital_ai_vitalsigns.metaql.query.query_builder import QueryBuilder, Arc, AndConstraintList, PropertyConstraint, \
    ConstraintType, ClassConstraint, OrConstraintList, PropertyPathList, AndArcList, MetaQLPropertyPath, NodeBind, \
    EdgeBind, PathBind
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.model.VITAL_Edge import VITAL_Edge
from vital_ai_vitalsigns.model.VITAL_Node import VITAL_Node
from vital_ai_vitalsigns.ontology.ontology import Ontology
from vital_ai_vitalsigns.service.graph.virtuoso.virtuoso_metaql_impl import VirtuosoMetaQLImpl
from vital_ai_vitalsigns.service.graph.virtuoso_service import VirtuosoGraphService
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from vital_ai_vitalsigns_core.model.properties.Property_hasName import Property_hasName


class DictEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)


def main():

    print('Test MetaQL Graph Builder')

    vs = VitalSigns()

    print("VitalSigns Initialized")

    config = vs.get_config()

    print(config)

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

    graph_query_json = json.dumps(gq, indent=4)

    print(f"Query JSON:\n{graph_query_json}")

    metaql_query_dict = json.loads(graph_query_json)

    metaql_graph_query = MetaQLParser.parse_metaql_dict(metaql_query_dict)

    print(f"Reparsed Query:\n{json.dumps(metaql_graph_query, indent=4)}")

    namespace = "VITALTEST"

    ontology_list: List[Ontology] = []

    # add resolving graph objects true/false into query

    sparql_string = VirtuosoMetaQLImpl.generate_graph_query_sparql(
        namespace=namespace,
        graph_query=metaql_graph_query,
        namespace_list=ontology_list
    )

    print(f"Graph Query SPARQL:\n{sparql_string}")

    vitalservice_config = config.vitalservice_list[0]

    virtuoso_username = vitalservice_config.graph_database.username
    virtuoso_password = vitalservice_config.graph_database.password
    virtuoso_endpoint = vitalservice_config.graph_database.endpoint

    virtuoso_graph_service = VirtuosoGraphService(
        username=virtuoso_username,
        password=virtuoso_password,
        endpoint=virtuoso_endpoint
    )

    graph_list = virtuoso_graph_service.list_graphs()

    for g in graph_list:
        print(f"Graph URI: {g.get_graph_uri()}")

    metaql_result = virtuoso_graph_service.metaql_graph_query(
        namespace=namespace,
        graph_query=metaql_graph_query,
        namespace_list=ontology_list
    )

    # print(f"MetaQL Result:\n{json.dumps(metaql_result, cls=DictEncoder, indent=4)}")

    print(metaql_result)

    rl = metaql_result.get_result_list()

    result_list = []

    for r in rl:
        result_element = MetaQLBuilder.build_result_element(
            graph_object=r.graph_object,
            score=r.score
        )
        result_list.append(result_element)

    metaql_result_list = MetaQLBuilder.build_result_list(
        offset=metaql_result.get_offset(),
        limit=metaql_result.get_limit(),
        result_count=len(metaql_result.get_result_list()),
        total_result_count=metaql_result.get_total_result_count(),
        binding_list=metaql_result.get_binding_list(),
        result_list=result_list,
        result_object_list=metaql_result.get_result_object_list(),
    )

    status = OK_STATUS_TYPE

    metaql_status = MetaQLBuilder.build_status(
        status_type=status
    )

    metaql_response = MetaQLBuilder.build_response(
        result_status=metaql_status,
        result_list=metaql_result_list
    )

    print(metaql_response)

    status = OK_STATUS_TYPE

    metaql_status = MetaQLBuilder.build_status(
        status_type=status
    )

    metaql_response = MetaQLBuilder.build_response(
        result_status=metaql_status,
        result_list=metaql_result_list
    )

    # print(metaql_response)

    metaql_response_json = json.dumps(metaql_response, cls=DictEncoder, indent=4)

    print(metaql_response_json)

    metaql_response_dict = json.loads(metaql_response_json)

    # print(metaql_response_dict)

    metaql_response_parsed = MetaQLParser.parse_metaql_dict(metaql_response_dict)

    # print(metaql_response_parsed)

    metaql_result_list = metaql_response_parsed['result_list']

    binding_list = metaql_result_list['binding_list']

    print(f"Binding List: {binding_list}")

    result_object_list = metaql_result_list['result_object_list']

    object_map = {}

    for go in result_object_list:
        print(f"Result Object: {go.to_json()}")
        uri = str(go.URI)
        object_map[uri] = go

    result_list = metaql_result_list['result_list']

    for re in result_list:
        print(f"ResultElement: {re}")
        go:GraphObject = re["graph_object"]
        print(f"ResultElement GraphMatch GO: {go.to_json(pretty_print=False)}")
        for b in binding_list:
            b_uri = str(go[b])
            bind_object: GraphObject = object_map[b_uri]
            print(f"Binding: {b} : {bind_object.to_json(pretty_print=False)}")


if __name__ == "__main__":
    main()
