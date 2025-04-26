import csv
import json

def export_to_csv(filename="tape_log.json", output_file=None):
    if output_file is None:
        base = filename.rsplit(".", 1)[0]
        output_file = base + ".csv"

    with open(filename) as f:
        steps = json.load(f)

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Line", "Code", "Locals", "Globals"])

        for i, step in enumerate(steps):
            if step.get("type") == "return":
                continue
            locals_str = json.dumps(step["locals"])
            globals_str = json.dumps(step.get("globals", {}))
            writer.writerow([i + 1, step["line"], step["code"], locals_str, globals_str])

    print(f"Data exported to {output_file}")

def export_to_html(filename="tape_log.json", output_file=None):
    if output_file is None:
        base = filename.rsplit(".", 1)[0]
        output_file = base + ".html"

    with open(filename) as f:
        steps = json.load(f)

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Timewarp Visualization</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #fafafa;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 10px 14px;
                text-align: left;
                border: 1px solid #ddd;
                vertical-align: top;
            }
            th {
                background-color: #f4f4f4;
            }
            .highlight {
                background-color: #ffff99;
            }
            .code {
                font-family: "Courier New", Courier, monospace;
                color: #333;
                white-space: pre-wrap;
            }
            .filter-section {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Timewarp Execution Steps</h1>

        <div class="filter-section">
            <label for="lineFilter">Filter by Line Numbers (comma separated): </label>
            <input type="text" id="lineFilter" placeholder="e.g. 5, 10, 12">
            <label for="varFilter">Filter by Variable Name: </label>
            <input type="text" id="varFilter" placeholder="e.g. arr">
            <button onclick="applyFilters()">Apply Filters</button>
        </div>

        <table id="stepsTable">
            <thead>
                <tr>
                    <th>Step</th>
                    <th>Line Number</th>
                    <th>Code</th>
                    <th>Locals</th>
                    <th>Globals</th>
                </tr>
            </thead>
            <tbody>
    """

    for i, step in enumerate(steps):
        step_number = i + 1

        if step.get("type") == "return":
            html_content += f"""
                <tr class="step return-step" data-line="return">
                    <td>{step_number}</td>
                    <td>—</td>
                    <td class="code"><strong>RETURN</strong>: {step['value']}</td>
                    <td colspan="2">—</td>
                </tr>
            """
            continue

        locals_html = "".join(
            f"<li><strong>{k}</strong>: {v}</li>" for k, v in step.get("locals", {}).items()
        )
        globals_html = "".join(
            f"<li><strong>{k}</strong>: {v}</li>" for k, v in step.get("globals", {}).items()
        )

        html_content += f"""
            <tr class="step" data-line="{step['line']}">
                <td>{step_number}</td>
                <td>{step['line']}</td>
                <td class="code">{step['code']}</td>
                <td><ul class="variables">{locals_html}</ul></td>
                <td><ul class="globals">{globals_html}</ul></td>
            </tr>
        """

    html_content += """
            </tbody>
        </table>

        <script>
            const steps = document.querySelectorAll('.step');
            let currentStep = 0;

            function showStep(stepIndex) {
                steps.forEach((step, index) => {
                    step.classList.toggle('highlight', index === stepIndex);
                });
            }

            function nextStep() {
                if (currentStep < steps.length - 1) {
                    currentStep++;
                    showStep(currentStep);
                }
            }

            function prevStep() {
                if (currentStep > 0) {
                    currentStep--;
                    showStep(currentStep);
                }
            }

            function applyFilters() {
                const lineFilter = document.getElementById('lineFilter').value
                    .split(',')
                    .map(s => s.trim())
                    .filter(Boolean);
                const varFilter = document.getElementById('varFilter').value.trim().toLowerCase();

                steps.forEach(step => {
                    const lineAttr = step.getAttribute('data-line');
                    const isReturn = lineAttr === 'return';
                    let show = true;

                    if (!isReturn && lineFilter.length > 0 && !lineFilter.includes(lineAttr)) {
                        show = false;
                    }

                    if (varFilter) {
                        const locals = Array.from(step.querySelectorAll('.variables li'));
                        const globals = Array.from(step.querySelectorAll('.globals li'));
                        const matchLocals = locals.some(li => li.textContent.toLowerCase().includes(varFilter));
                        const matchGlobals = globals.some(li => li.textContent.toLowerCase().includes(varFilter));
                        if (!matchLocals && !matchGlobals) {
                            show = false;
                        }
                    }

                    step.style.display = show ? 'table-row' : 'none';
                });
            }

            showStep(currentStep);

            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight') nextStep();
                if (e.key === 'ArrowLeft') prevStep();
            });
        </script>
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html_content)
    print(f"Visualization saved to {output_file}")