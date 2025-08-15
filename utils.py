import pandas as pd
import re
import ast

def df_to_markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No results found."

    headers = df.columns.tolist()
    md_table = "| " + " | ".join(headers) + " |\n"
    md_table += "|" + "|".join(["---"] * len(headers)) + "|\n"

    for row in df.itertuples(index=False, name=None):
        md_table += "| " + " | ".join(map(str, row)) + " |\n"

    return md_table

def parse_llm_response_method(response_text):
    list_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if list_match:
        list_str = list_match.group(0)
        try:
            return ast.literal_eval(list_str)
        except (ValueError, SyntaxError) as e:
            print(f"AST parsing failed: {e}")
            return None
    return None

def results_to_dataframe(results, input_df):
    """Convert results to a pandas DataFrame"""
    df_data = []
    for result in results:
        row = {
            'Field': result['field'],
            'Description': input_df['Description'],
            'edfi_entity': result['edfi_entity'],
            'edfi_attribute': result['edfi_attribute']
        }
        df_data.append(row)
    
    return pd.DataFrame(df_data)