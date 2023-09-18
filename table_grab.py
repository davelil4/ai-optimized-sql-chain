import pandas as pd
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
from ast import literal_eval
from dotenv import load_dotenv
import openai
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_base = "https://api.openai.com/v1"


# search through the reviews for a specific product
def search_table(user_query, top_n=1):
    
    df = pd.read_csv(os.path.join(
        os.getcwd(),
        'embeddings_database_gen/dataframe_csvs/schemata_embeddings_openai_df.csv'
    ))
    
    df.embedding = df.embedding.apply(literal_eval)
    
    # embedding = get_embedding(
    #     user_query,
    #     engine="text-embedding-ada-002" # engine should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    # )
    
    embedding = openai.Embedding.create(model='text-embedding-ada-002',
                                    input=user_query).data[0].embedding
    df["similarities"] = df.embedding.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    
    return res

def getTableContext(df: pd.DataFrame):
    return "".join(df['context'].tolist())

def getContext(question):
    return getTableContext(search_table(question)) + "---\n\n" + open(os.path.join(os.getcwd(), "gen.txt")).read()
    
    
def getSQL(question) -> str:
    
    context = getContext(question)
    
    print(context)
    
    comp = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
            {'role':'system', 'content':'You are an assistant that provides only SQL responses for PostgreSQL 15.'},
            {"role": "user", "content": context + "---\n\n" + question}
        ],
        temperature=.3
    )
    
    res = comp.choices[0].message.content
    
    return res
    
    
