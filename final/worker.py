from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from imdb import Cinemagoer
import asyncio

''' fetches the budget and box office of the given movie tconst

Args:
    goer: Cinemagoer object
    tconst: str, the tconst of the movie

Returns:
    list of [tconst, budget, box_office, country]
'''
async def fetch(goer, tconst):
    try:
        loop = asyncio.get_event_loop()
        movie = await loop.run_in_executor(executor, goer.get_movie, tconst)
        finance = movie['box office']
        country = movie['country codes'] if 'country codes' in movie else []
        country = " ".join(country)
        finance_budget = finance['Budget'] if 'Budget' in finance else ""
        finance_cwg = finance['Cumulative Worldwide Gross'] if 'Cumulative Worldwide Gross' in finance else ""

        print(f'i = {tconst}: {finance_budget}, {finance_cwg}, {country}')
        return [tconst, finance_budget, finance_cwg, country]
    except Exception as e:
        print(f'Error: {e}')

''' Opens the given movie csv file and fetches the data of the movies
'''
async def work(n: int):
    # get budget from cinemagoer
    box_office = pd.DataFrame(columns=('mid', 'budget', 'box_office', 'country'))

    # read the csv file using arg n and reconstruct df_movie
    df_movie = pd.read_csv(f'./work_parts/df_movie_{n}.csv')
    print(f'Processing part {n}...')

    # fetch the movie defined in the csv file
    goer = Cinemagoer()
    fetched = await asyncio.gather(*(fetch(goer, tconst) for tconst in df_movie["tconst"]))

    for i, data in enumerate(fetched):
        if data is None:
            continue
        box_office.loc[i] = data

    box_office.to_csv(f'./result_parts/box_office_part_{n}.csv', index=False)

if __name__ == '__main__':
    # get input argument of the python file 
    # and convert it to integer
    import sys
    import pathlib

    n = int(sys.argv[1])
    executor = ThreadPoolExecutor(max_workers=100)

    pathlib.Path('./result_parts').mkdir(parents=True, exist_ok=True)
    asyncio.run(work(n))