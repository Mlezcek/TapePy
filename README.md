# TapePy 

**TapePy** is a lightweight tool for **recording, tracing, and analyzing Python function execution**.  
Perfect for debugging, learning, or understanding how your code behaves under the hood.

---

## Features

- **Record** each line of function execution automatically.
- **Save locals and globals** during runtime into JSON format.
- **Analyze execution statistics** (duration, most frequent lines, variable usage, global changes).
- **Trace variable history** step-by-step (`trace_history`).


## Installation

Clone the repository and install locally:

```bash
git clone https://github.com/your-username/TapePy.git
cd TapePy
pip install .
```

(Package publishing to PyPI is planned soon.)

---

## Basic Usage

### 1. Recording function execution with `@tape`

The `@tape` decorator **records the execution** of a function, capturing every step (line executed, local/global variables) automatically:

```python
from tapepy import tape

@tape
def add(a, b):
    result = a + b
    return result

add(2, 3)
```

After the function runs, a **trace log** will be saved automatically into `tape_log.json`.



### 2. Analyzing the recorded execution

You can view a quick **summary** (duration, number of lines executed, variable usage) using:

```python
from tapepy import tape_stats

tape_stats()
```

This prints useful statistics to the console, helping you understand how the function behaved.

---

### 3. Replaying the recorded execution with `replay`

You can **replay** the recorded trace step-by-step to see how the code executed:

```python
from tapepy import replay

replay()
```

This will **simulate** the execution, showing line-by-line what happened and the variable states during each step.

---

### Summary

| Feature            | Purpose                                   |
|:-------------------|:------------------------------------------|
| `@tape`            | Record function execution automatically   |
| `replay()`         | Step through the recorded execution       |
| `tape_stats()`     | View execution statistics                 |
| `trace_history()`  | View statistics of single variable        |
| `export_to_html()` | Save the execution trace manually to html |
| `export_to_csv()`  | Save the execution trace manually to csv  |

---



