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
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]


    result = actees.groupby('category').agg({'person_id':['nunique']}).reset_index()
    result.columns = ['category', 'num_actees']
    
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
        .sort_values(["rating","primary_title"], ascending=(False,True))\
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

    most_actees = num_df.sort_values(['cast_size','primary_title'], ascending=(False,True))[:1]
    return most_actees

def Q4Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    titles = pd.read_csv("data/titles.csv")
    movies = titles[titles.type == 'movie']
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]

    num_df = pd.merge(left=movies, right=actees, on='title_id').groupby(['title_id','primary_title']).size().reset_index()
    num_df.columns = ['title_id', 'primary_title', 'cast_size']

    most_actees = num_df.sort_values(['cast_size','primary_title'], ascending=False)
    most_actees = most_actees[most_actees.cast_size == most_actees.max()['cast_size']].sort_values('primary_title').reset_index()
    return most_actees


def Q5Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    titles = pd.read_csv("data/titles.csv")
    people = pd.read_csv('data/people.csv')
    movies = titles[titles.type == 'movie']
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]
    
    movie_crew = pd.merge(left=movies, right=actees, on='title_id')
    actee_jobs = movie_crew.groupby('person_id').agg({'title_id':['nunique']}).reset_index()
    actee_jobs.columns = ['person_id', 'num_appearances']
    
    actee_total_jobs = pd.merge(right=movie_crew[['person_id','category']], left=actee_jobs, on='person_id').drop_duplicates()

    named_actees_by_job_count = pd.merge(left=actee_total_jobs, right=people[['person_id','name']], on='person_id').sort_values(['num_appearances','name'], ascending=(False,True))
    
    return named_actees_by_job_count[['name','category','num_appearances']]

def Q6Pandas():
    """
    Write your Pandas query here, return a dataframe to answer the question
    """
    crew = pd.read_csv("data/crew.csv")
    titles = pd.read_csv("data/titles.csv")
    people = pd.read_csv('data/people.csv')
    ratings = pd.read_csv("data/ratings.csv")

    movies = titles[titles.type == 'movie']
    actees = crew[(crew.category == 'actor') | (crew.category == 'actress')]
    
    movie_crew = pd.merge(left=movies, right=actees, on='title_id')
    actee_jobs = movie_crew.groupby('person_id').agg({'title_id':['nunique']}).reset_index()
    actee_jobs.columns = ['person_id', 'num_appearances']

    actee_total_jobs = pd.merge(right=movie_crew[['person_id','category']], left=actee_jobs, on='person_id').drop_duplicates()

    named_actees = pd.merge(left=actee_total_jobs, right=people[['person_id','name']], on='person_id').sort_values('name')
    best_actees = named_actees[named_actees.num_appearances >= 5]
    best_actees_with_movies = pd.merge(left=best_actees, right=crew[["title_id","person_id"]], on="person_id")
    best_actees_with_movies_and_ratings = pd.merge(left=best_actees_with_movies, right=ratings, on="title_id")

    final = best_actees_with_movies_and_ratings.groupby(['name', 'num_appearances', 'person_id']).agg({'rating':['mean']}).reset_index()
    final.columns = ["name", "num_appearances", "person_id", "avg_rating"]
    final.drop(columns="person_id")

    return final.sort_values(['avg_rating','name'], ascending=(False,True))[:15]

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