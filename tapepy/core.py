import sys
import json
import linecache
import time
import types
from collections import Counter
import functools

from tapepy.utils import is_serializable

TAPE_STATS = {}

def tape(name=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log = []
            prev_globals = {}

            start = time.perf_counter()

            def tracer(frame, event, arg):
                if frame.f_code.co_name == func.__name__ and event == "line":
                    lineno = frame.f_lineno
                    code_line = linecache.getline(frame.f_code.co_filename, lineno).strip()
                    locals_copy = frame.f_locals.copy()
                    globals_copy = frame.f_globals.copy()

                    locals_copy = {k: v for k, v in locals_copy.items()  if is_serializable(v)}
                    globals_copy = {k: v for k, v in globals_copy.items() if is_serializable(v)}


                    changed_globals = {
                        k: v for k, v in globals_copy.items()
                        if not k.startswith("__") and (k not in prev_globals or prev_globals[k] != v)
                    }
                    prev_globals.update(changed_globals)

                    log.append({
                        "type": "line",
                        "line": lineno,
                        "code": code_line,
                        "locals": locals_copy,
                        "globals": changed_globals
                    })
                return tracer

            sys.settrace(tracer)
            result = func(*args, **kwargs)
            sys.settrace(None)

            end = time.perf_counter()

            log.append({"type": "return", "value": result})

            safe_name = name if isinstance(name, str) else func.__name__
            filename = f"tape_{safe_name}.json" if name else "tape_log.json"

            with open(filename, "w") as f:
                json.dump(log, f, indent=2)

                lines = [step["line"] for step in log if step.get("type") == "line"]
                locals_counter = Counter(
                    var
                    for step in log if step.get("type") == "line"
                    for var in step["locals"].keys()
                )
                globals_changes = sum(len(step.get("globals", {})) for step in log)

                TAPE_STATS[func.__name__] = {
                    "duration_s": end - start,
                    "total_steps": len(lines),
                    "most_common_line": Counter(lines).most_common(1)[0] if lines else None,
                    "locals_usage": locals_counter.most_common(),
                    "global_changes": globals_changes,
                }

            return result
        return wrapper

    if callable(name):
        return decorator(name)

    return decorator

def replay(filename="tape_log.json", line_filter=None, var_filter=None, range_filter=None):
    """
    Replays the execution steps from a JSON log with optional filters.

    :param filename: Path to the JSON file containing execution logs.
    :param line_filter: List of line numbers to filter the logs by (optional).
    :param var_filter: Variable name or dictionary to filter the logs by (optional).
    :param range_filter: Tuple with start and end line numbers to filter logs by a range (optional).
    """

    if line_filter is not None and not isinstance(line_filter, list):
        line_filter = [line_filter]

    if range_filter is not None and not isinstance(range_filter, tuple):
        raise ValueError("range_filter must be a tuple (start_line, end_line)")

    with open(filename) as f:
        steps = json.load(f)

    for step in steps:
        if step.get("type") == "return":
            print(f"RETURN: {step['value']}")
            print("=" * 40)
            continue

        if line_filter and step['line'] not in line_filter:
            continue

        if range_filter and not (range_filter[0] <= step['line'] <= range_filter[1]):
            continue

        if var_filter:
            if isinstance(var_filter, dict):
                for var, val in var_filter.items():
                    if var not in step['locals'] or step['locals'][var] != val:
                        continue
            else:
                if var_filter not in step['locals']:
                    continue

        print(f"Line {step['line']}: {step['code']}")

        for var, value in step['locals'].items():
            if not var_filter or var == var_filter:
                print(f"    {var} = {value}")

        if step.get("globals"):
            print("  [Globals]")
            for gvar, gval in step["globals"].items():
                print(f"    {gvar} = {gval}")

        print("-" * 40)
        time.sleep(1)
