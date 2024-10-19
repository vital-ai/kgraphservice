import json

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from vital_ai_vitalsigns.service.graph.virtuoso_service import VirtuosoGraphService
from vital_ai_vitalsigns.service.vital_service import VitalService
from vital_ai_vitalsigns.vitalsigns import VitalSigns

from kgraphservice.rest.impl.kgraphservice_rest_impl import KGraphServiceRESTImpl

app = FastAPI()

vs = VitalSigns()

config = vs.get_config()

vitalservice_config = config.vitalservice_list[0]

virtuoso_username = vitalservice_config.graph_database.username
virtuoso_password = vitalservice_config.graph_database.password
virtuoso_endpoint = vitalservice_config.graph_database.endpoint

virtuoso_graph_service = VirtuosoGraphService(
    username=virtuoso_username,
    password=virtuoso_password,
    endpoint=virtuoso_endpoint
)

vital_service = VitalService(
    vitalservice_name=vitalservice_config.name,
    vitalservice_namespace=vitalservice_config.namespace,
    graph_service=virtuoso_graph_service,
)

rest_impl = KGraphServiceRESTImpl(
    vitalservice=vital_service
)


class DictEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/kgraphservice")
async def handle_kgraphservice_request(request: Request):

    request_data = await request.json()

    print(request_data)

    response = rest_impl.handle_request(request_data)

    # print(response)

    json_response = json.dumps(response, cls=DictEncoder)

    return JSONResponse(content=json_response )


def run_app(*, host: str = "0.0.0.0", port:int = 6008):
    uvicorn.run(app, host=host, port=port)

