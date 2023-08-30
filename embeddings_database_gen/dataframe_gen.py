import pandas as pd
import os
from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()

model = "defog/sqlcoder"

def init_schemata_df():
    
    data = {
        'schemata': [],
        'context': [],
    }
    
    for filename in os.listdir(os.path.join(os.getcwd(), 'schemata')):
        if (".txt" in filename):
            f = open(os.path.join(os.getcwd(), f'schemata/{filename}'), 'r')
            data['schemata'].append(filename)
            data['context'].append(f.read())
            f.close()
    
    df = pd.DataFrame(data=data)
    
    df.to_csv(os.path.join(os.getcwd(), 'dataframe_csvs/schemata_df.csv'), index=False)
    
def apply_schemata_embeddings():
    df = pd.read_csv(os.path.join(
        os.getcwd(),
        'dataframe_csvs/schemata_df.csv'
    ))
    
    df
    
    # extract = pipeline("feature-extraction",model=model)
    try:
        df['embedding'] = df['context'].apply( lambda x: get_embedding(x))
    except Exception as e:
        print(e)
    # print(e)

    
if __name__ == "__main__":
    apply_schemata_embeddings()