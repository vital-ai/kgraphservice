import os
from datetime import datetime

from ai_haley_kg_domain.model.Edge_hasKGChatInteractionEventNode import Edge_hasKGChatInteractionEventNode
from ai_haley_kg_domain.model.Edge_hasKGChatInteractionEventSuccessor import Edge_hasKGChatInteractionEventSuccessor
from ai_haley_kg_domain.model.KGChatBotMessage import KGChatBotMessage
from ai_haley_kg_domain.model.KGChatInteractionEvent import KGChatInteractionEvent
from ai_haley_kg_domain.model.KGChatUserMessage import KGChatUserMessage
from ai_haley_kg_domain.model.KGNode import KGNode
from vital_ai_vitalsigns.service.graph.memory_graph_service import MemoryGraphService
from vital_ai_vitalsigns.utils.uri_generator import URIGenerator
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from kgraphservice.mgr.kgraph_service_manager import KGraphServiceManager


def main():
    print('Test KGraph Chat Message')

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

    # define chat event

    # event are within a graph
    # but should they be associated with other source, like room?

    # decide on timestamp property to use

    room_uri = "urn:room_123"

    event_1 = KGChatInteractionEvent()
    event_1.URI = URIGenerator.generate_uri()
    # event_1.objectCreationTime = datetime.now()

    user_message_1 = KGChatUserMessage()
    user_message_1.URI = URIGenerator.generate_uri()
    user_message_1.kGRoomURI = room_uri
    # user_message_1.objectCreationTime = datetime.now()

    edge_message_1 = Edge_hasKGChatInteractionEventNode()
    edge_message_1.URI = URIGenerator.generate_uri()
    edge_message_1.edgeSource = event_1.URI
    edge_message_1.edgeDestination = user_message_1.URI

    event_2 = KGChatInteractionEvent()
    event_2.URI = URIGenerator.generate_uri()
    # event_2.objectCreationTime = datetime.now()

    bot_message_2 = KGChatBotMessage()
    bot_message_2.URI = URIGenerator.generate_uri()
    bot_message_2.kGRoomURI = room_uri

    bot_message_2.objectCreationTime = datetime.now()

    edge_message_2 = Edge_hasKGChatInteractionEventNode()
    edge_message_2.URI = URIGenerator.generate_uri()
    edge_message_2.edgeSource = event_2.URI
    edge_message_2.edgeDestination = bot_message_2.URI

    edge_successor_1 = Edge_hasKGChatInteractionEventSuccessor()
    edge_successor_1.URI = URIGenerator.generate_uri()
    edge_successor_1.edgeSource = event_1.URI
    edge_successor_1.edgeDestination = event_2.URI


    # insert

    # query

    # get uri of components

    # delete

    # confirm delete via uris

    # insert again as #A

    # insert another as successor #B

    # insert another as successor #C

    # insert another in between #A and #B as #D

    # confirm order A,D,B,C

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