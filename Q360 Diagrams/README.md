# Generating a Q360 Diagram
1. In the root directory of this repo, run the follow commands in the terminal (after installation, only activate venv):
    ```
    > python -m venv venv
    > venv\Source\activate
    > pip install pandas
    ```
2. Install graphviz https://graphviz.org/download/
3. Update contents of tables.csv by running generate_table_report.sql
    - Copy results of query into tables.csv
    - Ensure proper CSV formatting
4. Update values for table_names_to_include and limit_connections_to_fields_ending_in_no
5. Run the follow command in the terminal:
    ```
    python "Q360 Diagrams/generate_db_diagram.py"
    ```
6. Run the follow command in the terminal:
    ```
    > deactivate
    ```