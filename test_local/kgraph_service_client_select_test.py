from ai_haley_kg_domain.model.KGEntity import KGEntity
from ai_haley_kg_domain.model.properties.Property_hasKGraphDescription import Property_hasKGraphDescription
from vital_ai_vitalsigns.metaql.query.query_builder import QueryBuilder, AndConstraintList, PropertyConstraint, \
    ConstraintType, ClassConstraint

from vital_ai_vitalsigns.vitalsigns import VitalSigns
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


if __name__ == "__main__":
    main()
