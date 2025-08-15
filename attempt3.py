import boto3
import pandas as pd
from dotenv import load_dotenv
from prompt import SINGLE_PARSEABLE_SYSTEM_PROMPT
from utils import df_to_markdown_table, parse_llm_response_method, results_to_dataframe

load_dotenv()



runtime = boto3.client("bedrock-runtime")

def call_llm(input_df):
    
    md_input = df_to_markdown_table(input_df[['Field', 'Description']])

    response = runtime.converse(
        modelId="arn:aws:bedrock:us-east-1:654654390449:application-inference-profile/xjq2nc32nzby",
        messages=[
            {"role": "user", "content": [{"text": SINGLE_PARSEABLE_SYSTEM_PROMPT}, {"text": md_input}]}
        ]
    )
    parsed_reponse = parse_llm_response_method(response["output"]["message"]["content"][0]["text"])
    return parsed_reponse if parsed_reponse else []

def main(input_path, output_path, chunk_size = 30):
    results = []
    input_df = pd.read_csv(input_path)

    for i in range(0,len(input_df), chunk_size):
        chunk_df = input_df.iloc[i:i+chunk_size]
        list = call_llm(chunk_df)
        results.extend(list)

    out = results_to_dataframe(results, input_df)
    out.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_path = 'final/dallas spring enrollment.csv'
    output_path = 'final/dallas_spring_att3.csv'

    main(input_path, output_path)

def return_df(input_path, chunk_size = 30):
    results = []
    input_df = pd.read_csv(input_path)

    for i in range(0,len(input_df), chunk_size):
        chunk_df = input_df.iloc[i:i+chunk_size]
        list = call_llm(chunk_df)
        results.extend(list)

    out = results_to_dataframe(results, input_df)

    return out