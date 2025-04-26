import json

from tapepy.core import TAPE_STATS


def tape_stats(func_name=None):
    """
    Wyświetla statystyki dla wszystkich lub jednej funkcji.
    :param func_name: nazwa funkcji (str) lub None – wszystkie.
    """
    if func_name:
        stats = TAPE_STATS.get(func_name)
        if not stats:
            print(f"No stats for function '{func_name}'")
            return
        funcs = {func_name: stats}
    else:
        funcs = TAPE_STATS

    for name, st in funcs.items():
        print(f"=== STATISTICS for {name} ===")
        print(f"Duration       : {st['duration_s']:.6f} s")
        print(f"Total steps    : {st['total_steps']}")
        mcl = st["most_common_line"]
        if mcl:
            print(f"Hotspot line   : {mcl[0]} executed {mcl[1]} times")
        print("Locals usage   :")
        for var, cnt in st["locals_usage"]:
            print(f"  - {var}: {cnt} snapshots")
        print(f"Global changes : {st['global_changes']}")
        print()

def trace_history(var_name, filename="tape_log.json"):
    with open(filename) as f:
        steps = json.load(f)

    history = []
    last_value = object()  # sentinel

    for step_num, step in enumerate(steps, start=1):
        if step.get("type") != "line":
            continue

        value = None
        source = None
        previous_value = None

        # Sprawdzenie lokalnych zmiennych
        if var_name in step.get("locals", {}):
            value = step["locals"][var_name]
            source = "local"
            previous_value = step["locals"].get(var_name, None)
        # Sprawdzenie globalnych zmiennych
        elif var_name in step.get("globals", {}):
            value = step["globals"][var_name]
            source = "global"
            previous_value = step["globals"].get(var_name, None)

        # Jeśli zmiana wartości nastąpiła, zapisz do historii
        if value is not None and value != last_value:
            history.append({
                "step": step_num,  # Numer kroku
                "line": step["line"],
                "code": step["code"],
                "previous_value": previous_value,  # Wcześniejsza wartość
                "value": value,
                "source": source,
                "operation": "Assignment" if previous_value is None else "Modification"  # Rodzaj operacji
            })
            last_value = value

    if not history:
        print(f"No changes found for variable '{var_name}'.")
        return

    for entry in history:
        print(f"Step {entry['step']}: Line {entry['line']}: {entry['code']}")
        print(f"    {var_name} ({entry['source']}) = {entry['value']}")
        print(f"    Previous value: {entry['previous_value']}")
        print(f"    Operation: {entry['operation']}")
        print("-" * 40)