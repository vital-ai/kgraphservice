import os
from ai_haley_kg_domain.model.KGNode import KGNode
from vital_ai_vitalsigns.service.graph.memory_graph_service import MemoryGraphService
from vital_ai_vitalsigns.utils.uri_generator import URIGenerator
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from kgraphservice.mgr.kgraph_service_manager import KGraphServiceManager


def main():
    print('Test KGraph Service In-Memory')

    print('Ontologies Initializing...')
    vs = VitalSigns()
    print('Ontologies Initialized.')

    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    parent_directory = os.path.dirname(current_directory)

    test_file = 'test_data/test_graph-0.0.1.nt'

    file_path = os.path.join(parent_directory, test_file)
    file_path = os.path.normpath(file_path)
    file_path = os.path.normpath(file_path)
    file_path = str(file_path)

    print(f"Test File Path: {file_path}")

    kgraph_name = "test_kgraph"

    kgraphservice_manager = KGraphServiceManager()

    kgraph_service = kgraphservice_manager.add_kgraphservice_memory(kgraph_name)

    for mem_service in kgraphservice_manager.get_kgraphservice_memory_list():
        print(f"Memory Service Name: {mem_service}")

    test_graph_uri = "urn:test_graph"

    graph_uri_list = [test_graph_uri]

    created_graph = kgraph_service.create_graph(test_graph_uri)

    graph_list = kgraph_service.list_graphs()

    print(f"KGraph Graph Count: {len(graph_list)}")

    for graph in graph_list:
        print(f"Graph: {graph.graph_uri}")

    kgnode = KGNode()
    kgnode.URI = URIGenerator.generate_uri()
    kgnode.name = "Test Node"

    print(kgnode.to_rdf())

    status = kgraph_service.update_object_list([kgnode], test_graph_uri, upsert=True)

    print(f"Upsert Status: {status.get_message()}")

    if not status.get_status() == 0:
        print("Upsert Failed")
    else:
        print("Upsert Successful")

    result_list = kgraph_service.get_graph_all_objects(test_graph_uri, limit=100, offset=0)

    for re in result_list:
        g = re.graph_object
        print(g.to_json())

    vital_service = kgraph_service.vital_service
    graph_service = vital_service.graph_service

    if isinstance(graph_service, MemoryGraphService):

        export_status = graph_service.export_ntriples(test_graph_uri, file_path, overwrite=True)

        print(f"Export Successful: {export_status}")

        kgraph_service.purge_graph(test_graph_uri)

        graph_service.import_ntriples(test_graph_uri, file_path)


if __name__ == "__main__":
    main()
