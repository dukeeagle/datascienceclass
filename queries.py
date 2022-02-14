import sqlite3 as sql
import pandas as pd
import argparse

def runSQL(query_num, store):
    with sql.connect("data/imdb.db") as conn, open("queries/q{}.sql".format(query_num)) as in_query:
        cur = conn.cursor()
        df = pd.read_sql_query(in_query.read(), conn)
        pd.set_option('display.max_rows', 100)
        if store: df.to_csv(f"submission/sql_sol{query_num}.csv", index=False)
        return df

def Q1Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    actors = crew[crew['category'] == 'actor']
    actresses = crew[crew['category'] == 'actress']
    actees = pd.concat([actresses,actors])


    result = actees.groupby('category').agg({'person_id':['nunique']})
    return result

def Q2Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    titles = pd.read_csv("data/titles.csv")
    ratings = pd.read_csv("data/ratings.csv")

    action_shows = titles[(titles['genres'].str.contains('Action')) & (titles.type=='tvSeries') & (titles.premiered == 2021)]
    action_show_ratings = pd.merge(left=action_shows, right=ratings, on='title_id')
    return action_show_ratings[(action_show_ratings.rating >= 8) & (action_show_ratings.votes >= 100)]\
        .sort_values(["rating","primary_title"], ascending=False)\
        [['title_id','primary_title','rating']]

def Q3Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    titles = pd.read_csv("data/titles.csv")
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]
    movies = titles[titles.type == 'movie']
    num_df = pd.merge(left=movies, right=actees, on='title_id').groupby(['title_id','primary_title']).size().reset_index()
    num_df.columns = ['title_id', 'primary_title', 'cast_size']

    most_actees = num_df.sort_values(['cast_size','primary_title'], ascending=False)[:1]
    return most_actees

def Q4Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    titles = pd.read_csv("data/titles.csv")
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]
    num_df = pd.merge(left=movies, right=actees, on='title_id').groupby(['title_id','primary_title']).size().reset_index()
    num_df.columns = ['title_id', 'primary_title', 'cast_size']

    most_actees = num_df.sort_values(['cast_size','primary_title'], ascending=False)
    return most_actees[most_actees.cast_size == most_actees.max()['cast_size']].sort_values('primary_title')


def Q5Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    titles = pd.read_csv("data/titles.csv")
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]
    movie_crew = pd.merge(left=movies, right=actees, on='title_id')
    actee_jobs = movie_crew.groupby('person_id').agg({'title_id':['nunique']}).reset_index()
    actee_jobs.columns = ['person_id', 'num_movies']
    
    actee_total_jobs = pd.merge(right=movie_crew[['person_id','category']], left=actee_jobs, on='person_id').drop_duplicates()

    return pd.merge(left=actee_total_jobs, right=people[['person_id','name']], on='person_id').sort_values('name')

def Q6Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """

    return None

pandas_queries = [Q1Pandas, Q2Pandas, Q3Pandas, Q4Pandas, Q5Pandas, Q6Pandas]
df = None
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="Run a specific query", type=int)
    parser.add_argument("--store", "-s", help="Store", default=False, action='store_true')
    args = parser.parse_args()

    store = args.store

    queries = range(1, 11)
    if args.query != None:
        queries = [args.query]
    for query in queries:
        print("\nQuery {}".format(query))
        if query <= 6:
            print("\nPandas Output")
            df = pandas_queries[query-1]()
            print(df)
            if store: df.to_csv(f"submission/pandas_sol{query}.csv", index=False)
        print("\nSQLite Output")
        df = runSQL(query, store)
        print(df)