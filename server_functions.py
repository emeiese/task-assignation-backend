from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value


def resolve_problem(
    people,
    tasks,
    days,
    costs,
    min_assign_task,
    max_assign_task,
    max_total_assign,
    min_total_assign,
):
    """Solves the optimization problem (optimal assignation for each task)
    given the parameters, costs and restriction values.

    Args:
        people ([List[str]]): People to consider on the optimization
        tasks ([List[str]]): Tasks to consider on the optimization
        days ([List[str]]): Days or periods to consider on the optimization
        costs ([Dict[Dict[int]]]): Dictionary with the costs for each task for each human. Each key is a human name, while each subkey is a task.
        min_assign_task ([int]): Indicates the minimum number of assignations that a person must have on a task on a week or at the end of the periods.
        max_assign_task ([int|boolean]): Indicates the maximum number of assignations that a person can have on a task on a week or at the end of the periods. 
                                        If false, it means the user didn't specify this variable
        max_total_assign ([int|boolean]): Indicates the maximum number of total assignations that a person can have on a week or at the end of the periods.
                                        If false, it means the user didn't specify this variable
        min_total_assign ([int]): Indicates the minimum number of total assignations that a person must have on a week or at the end of the periods.

    Returns:
        [Dict]: Returns a dict with the optimum assignation, the status of the problem and the value of the optimization function.
    """
    print(max_total_assign, max_assign_task)
    if not max_assign_task:
        temp_max_assign_task = 1000
    else:
        temp_max_assign_task = max_assign_task

    if not max_total_assign:
        temp_max_total_assign = 1000
    else:
        temp_max_total_assign = max_total_assign

    dpt_tuples = []
    for d in days:
        for p in people:
            for t in tasks:
                dpt_tuples.append((d, p, t))

    day_task_tuples = []
    for d in days:
        for t in tasks:
            day_task_tuples.append((d, t))

    # Problem
    prob = LpProblem("Assignation_Problem", LpMinimize)

    # Variables
    assign = LpVariable.dicts(
        "assignation",
        ((day, person, task) for (day, person, task) in dpt_tuples),
        cat="Binary",
    )

    # Objective Function
    prob += lpSum(
        [
            assign[day, person, task] * costs[person][task]
            for (day, person, task) in dpt_tuples
        ]
    )

    # Rstrictions

    # No puede haber 1 persona en dos tareas el mismo día (si es que el número de tareas es menor al de personas).
    if len(tasks) <= len(people):
        for person in people:
            for day in days:
                prob += lpSum([assign[day, person, task] for task in tasks]) <= 1

    # Todos los días, cada turno debe estar asignado a 1 person (esto implica implícitamente que habrán m turnos asignados por día).
    for day in days:
        for task in tasks:
            prob += lpSum([assign[day, person, task] for person in people]) == 1

    # Restricciones de Justicia:

    # 1.Asignación mínima por tarea durante la semana para cada persona
    for task in tasks:
        for person in people:
            prob += (
                lpSum([assign[day, person, task] for day in days]) >= min_assign_task
            )

    # 2.Máximo de asignaciones en una semana, para una tarea, por persona
    for person in people:
        for task in tasks:
            prob += (
                lpSum([assign[day, person, task] for day in days]) <= temp_max_assign_task
            )

    # 3.Número de asignaciones mínimas por persona durante una semana:
    for person in people:
        prob += (
            lpSum([assign[day, person, task] for (day, task) in day_task_tuples])
            >= min_total_assign
        )

    # 4.Número de asignaciones máximas por persona durante una semana:
    for person in people:
        prob += (
            lpSum([assign[day, person, task] for (day, task) in day_task_tuples])
            <= temp_max_total_assign
        )

    print("-" * 50, "Resolviendo el problema", "-" * 50)
    prob.solve()
    status = LpStatus[prob.status]
    val = value(prob.objective)
    print("Status:", status)
    print("Value:", val)

    if status == "Optimal":
        final = {}
        for task in tasks:
            assignations = {}
            for day in days:
                for person in people:
                    aux = assign[(day, person, task)].varValue
                    if aux:
                        assignations[day] = person
            final[task] = assignations
    else:
        final = None

    return {
        "assignation": final,
        "status": status,
        "value": val,
        "names": people,
        "tasks": tasks,
        "days": days,
        "costs": costs,
        "min_assign_task": min_assign_task,
        "max_assign_task": max_assign_task,
        "min_total_assign": min_total_assign,
        "max_total_assign": max_total_assign,
    }
