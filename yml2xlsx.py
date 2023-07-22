import yaml
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo

def yaml_to_excel(filename, output_filename):
    # Read the yaml file
    with open(filename, 'r', encoding='utf-8') as file:
        data_dict = yaml.safe_load(file)

    # Transform the data to a flat dataframe
    df = pd.json_normalize(data_dict['Technologies'], sep='_')

    # Convert list elements to string in the dataframe
    df = df.applymap(lambda x: '\n'.join(f'- {i}' for i in x) if isinstance(x, list) else x)
    
    # Convert list elements in 'Vendors' to comma-separated string
    df['Vendors'] = df['Vendors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active

    # Append rows of the dataframe to the worksheet
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Wrap text for all cells
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrapText=True)

    # Create a table style
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=True)

    # Add a table with the style to the worksheet
    table = Table(ref=ws.dimensions, displayName="Table1", tableStyleInfo=style)
    ws.add_table(table)

    # Save the workbook
    wb.save(output_filename)

if __name__ == "__main__":
    yaml_to_excel('ai.yaml', 'output.xlsx')
