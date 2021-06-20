from fastapi import FastAPI, Query, Body
from typing import List, Dict, Optional
from pydantic import BaseModel
from server.server_functions import resolve_problem
from math import floor, ceil
from fastapi.middleware.cors import CORSMiddleware

# uvicorn server.backend:app --reload

app = FastAPI()
origins = ["http://localhost:8080", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def return_options(min_value, max_value):
    d_options = {str(v): v for v in range(min_value, max_value + 1)}
    options = []
    for k, v in d_options.items():
        option = {}
        option["text"] = k
        option["value"] = v
        options.append(option)
    return options

class ProblemParams(BaseModel):
    names: List[str]
    tasks: List[str]
    days: List[str]
    costs: Dict[str, Dict[str, int]]
    min_assign_task: int = 1
    max_assign_task: int = 10000
    max_total_assign: int = 10000
    min_total_assign: int = 1

class ParamsLength(BaseModel):
    d: int
    t: int
    p: int
    

@app.get("/")
def read_root():
    return {"Init_message": "Wena' mundooo"}


@app.post("/getOptions/")
async def get_options(tasks: List[str] = Body(..., embed=True)):
    """Given the tasks list, returns a list of dictionaries with the options for the fronetend

    Args:
        tasks (List[str]): List of tasks

    Returns:
        [List[Dict]]: Lists with options
    """
    """ 
    size = len(tasks)
    d_options = {str(v): v for v in range(0, size + 1)}
    options = []
    for k, v in d_options.items():
        option = {}
        option["text"] = k
        option["value"] = v
        options.append(option)
    """
    options = return_options(0, len(tasks))
    return options


@app.post("/checkCosts/")
async def check_costs(costs: Dict[str, Dict[str, int]] = Body(..., embed=True)):
    """
    Chequea si los costos para cada persona entregados por el usuario son válidos
    """
    correctness = {}
    for human_name, tasks_costs in costs.items():
        s = sum(v for (k, v) in tasks_costs.items())
        if s != len(tasks_costs):
            correctness[human_name] = False
            return False
        else:
            correctness[human_name] = True
    return True

@app.post("/get_restriction_options")
async def get_restriction_options(params: ParamsLength):
    """Retorna diccionarios con las opciones posibles para las restricciones

    Args:
        d (int): cantidad total de días del problema 
        t (int): cantidad total de tareas del problema 
        p (int): cantidad total de personas del problema 

    Returns:
        [type]: [description]
    """
    # Mínimo y máximo de valores para asignar en la primera restricción
    #max_one = ceil(d / t)
    max_one = 10
    min_one = 1

    # Mínimo y máximo de valores para asignar en la segunda restricción
    max_two = 10
    min_two = 1

    # Mínimo y máximo de valores para asignar en la tercera restricción
    max_three = params.t * params.d
    min_three = floor((params.d * params.t) / params.p) + 1

    one_options = return_options(min_one, max_one)
    two_options = return_options(min_two, max_two)
    three_options = return_options(min_three, max_three)

    return {"1": one_options, "2": two_options, "3": three_options}


@app.post("/resolve/")
async def solve_problem(params: ProblemParams):
    """
    Resuelve el problema
    """
    return resolve_problem(params.names, params.tasks, params.days, params.costs, params.min_assign_task, params.max_assign_task, params.max_total_assign, params.min_total_assign)


# Se le entrega una lista al path de la forma:
# http://localhost:8000/items/?q=100&q=200
# Además, tendrá un valor por defecto, que será [1, 2] si se entrega http://localhost:8000/items/

# Los path params son los parámetros que van especificados entre {} al definir la ruta

# En este caso, estamos especificando que 'q' es un query param opcional,
# por lo que entregamos un valor por defecto

# Query(...) declara explícitamente que ese es un query parameter.
@app.get("/items/")
async def read_items(q: Optional[List[int]] = Query([1, 2], title="Query item", description="Buena los cabros, aquí una descripción")):
    query_items = {"q": q}
    return query_items
