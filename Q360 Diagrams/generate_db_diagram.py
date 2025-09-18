import pandas as pd
from graphviz import Digraph
import datetime as datetime

def generate_db_diagram(csv_file, table_names, limit_connections, output_file="output_diagram"):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Validate required columns
    required_columns = {"TABLE_NAME", "COLUMN_NAME", "DATA_TYPE", "CHARACTER_MAXIMUM_LENGTH", "KEY_TYPE", "IS_INDEXED"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV file must contain the following columns: {required_columns}")

    # Convert all string values to uppercase
    string_columns = df.select_dtypes(include=["object"]).columns
    df[string_columns] = df[string_columns].apply(lambda col: col.str.upper())

    # Replace ampersands in relevant columns
    for column in ["TABLE_NAME", "COLUMN_NAME", "DATA_TYPE"]:
        df[column] = df[column].str.replace("&", "AND", regex=False)

    # Filter the DataFrame to include only the specified table names
    df = df[df["TABLE_NAME"].isin([name.upper() for name in table_names])]

    # Create a Graphviz Digraph
    dot = Digraph(comment="Database Diagram", format="png")
    dot.attr(rankdir="LR", fontsize="10", nodesep="1.0", ranksep="1.5", splines="polyline")

    # Group by table and add nodes for each table
    grouped_tables = df.groupby("TABLE_NAME")
    for TABLE_NAME, group in grouped_tables:
        table_label = f"<<TABLE BORDER='1' CELLBORDER='1' CELLSPACING='0'>"
        table_label += f"<TR><TD COLSPAN='4'><B>{TABLE_NAME}</B></TD></TR>"
        table_label += f"<TR><TD><B>Column Name</B></TD><TD><B>Data Type</B></TD><TD><B>Key</B></TD><TD><B>Index</B></TD></TR>"
        for _, row in group.iterrows():
            # Add column information
            column_info = f"{row['COLUMN_NAME']}"
            
            # Add data type with character limit
            data_type_info = f"{row['DATA_TYPE']}"
            if not pd.isna(row['CHARACTER_MAXIMUM_LENGTH']):
                data_type_info += f"({int(row['CHARACTER_MAXIMUM_LENGTH'])})"

            # Add key and index information
            key_info = ""
            if row['KEY_TYPE'] == "PRIMARY KEY":
                key_info = "PK"
            elif row['KEY_TYPE'] == "FOREIGN KEY":
                key_info = "FK"

            index_info = ""
            if row['IS_INDEXED']:
                index_info = "TRUE"

            # Add row to table label
            table_label += f"<TR><TD>{column_info}</TD><TD>{data_type_info}</TD><TD>{key_info}</TD><TD>{index_info}</TD></TR>"
        table_label += "</TABLE>>"
        dot.node(TABLE_NAME, label=table_label, shape="plaintext")

    # Add edges for foreign keys
    for COLUMN_NAME, group in df.groupby("COLUMN_NAME"):
        if not(limit_connections) or (limit_connections and COLUMN_NAME.upper().endswith("NO") and len(group["TABLE_NAME"].unique()) > 1):
            tables_with_column = group["TABLE_NAME"].unique()
            for i in range(len(tables_with_column) - 1):
                dot.edge(tables_with_column[i], tables_with_column[i + 1], label=COLUMN_NAME)

    
    # Append datetime to output file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_with_timestamp = f"Q360 Diagrams/generated/{output_file}_{timestamp}"

    # Render the diagram
    dot.render(output_file_with_timestamp, cleanup=True)
    print(f"Database diagram saved as {output_file_with_timestamp}.png")

# Example usage
if __name__ == "__main__":
    csv_file_path = "Q360 Diagrams/tables.csv"  # Replace with your CSV file path
    table_names_to_include = [
        "CUSTOMER", "SITE", "CONTACT", "OPPOR", "QUOTE", "QUOTEITEM", 
        "CONTRACT", "CONTRACTITEM", "PROJECTS", "SERVICECONTRACT", 
        "MACHINE", "MACHINEDETAIL", "MASTER", "ASSET", 
        "VENDINVOICE", "VENDINVOICEITEM", "INVOICE", "INVOICEITEM", 
        "DISPATCH", "SERVICECONTRACT"]  # Replace with table names to include
    limit_connections_to_fields_ending_in_no = True  # Set to True to limit connections to fields ending with 'NO'
    generate_db_diagram(csv_file_path, table_names_to_include, limit_connections_to_fields_ending_in_no)