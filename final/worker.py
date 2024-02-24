def work(n: int):
    # get budget from cinemagoer
    import pandas as pd
    box_office = pd.DataFrame(columns=('mid', 'budget', 'box_office', 'country'))
    k = 0

    # read the csv file using arg n and reconstruct df_movie
    df_movie = pd.read_csv(f'./df_movie_{n}.csv')
    print(f'Processing part {n}...')

    # fetch the movie defined in the csv file
    from imdb import Cinemagoer, IMDbDataAccessError
    ia = Cinemagoer()
    for i in df_movie['tconst']:
        try:
            movie = ia.get_movie(i)
            print(f'Movie info: {movie}')

            finance = movie['box office']
            country = movie['country codes'] if 'country codes' in movie else []
            country = " ".join(country)
            finance_budget = finance['Budget'] if 'Budget' in finance else ""
            finance_cwg = finance['Cumulative Worldwide Gross'] if 'Cumulative Worldwide Gross' in finance else ""

            print(f'i = {i}: {finance_budget}, {finance_cwg}, {country}')
            box_office.loc[k] = [i, finance_budget, finance_cwg, country]
            k =+ 1
        except Exception as e:
            print(f'Error: {e}')

    box_office.to_csv(f'./box_office_part_{n}.csv', index=False)

if __name__ == '__main__':
    # get input argument of the python file 
    # and convert it to integer
    import sys
    n = int(sys.argv[1])
    work(n)