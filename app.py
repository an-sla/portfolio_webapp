from flask import Flask, render_template
import plotly
import plotly.express as px
import pandas as pd
import json
import git

app = Flask(__name__)


def download_df():
    df = pd.read_csv('/home/ansla/portfolio_webapp/files/geonames.csv', sep=';')
    df['Name'] = df['Name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df[['lats', 'longs']] = df['Coordinates'].str.split(',', 1, expand=True)
    df['city_name'] = df['Name']
    df.drop(df.columns.difference(['lats', 'longs', 'city_name', 'Country name EN']), axis=1, inplace=True)
    return df


locations = ['St. Moritz', 'Menaggio', 'London', 'Prague', 'Moscow', 'Lysa nad Labem', 'Corvara in Badia']
countries = ['Switzerland', 'Italy', 'United Kingdom', 'Czech Republic', 'Russian Federation', 'Czech Republic',
             'Italy']


# method for adding city and country
def add_city_country(city, country, loc, country_list):
    loc.append(city)
    country_list.append(country)


def prep_df(loc, country_list, df):
    coord = pd.DataFrame(columns=['city_name'], data=loc)
    coord['countries'] = country_list
    coord = coord.merge(df, on='city_name', how='inner')
    coord = coord.loc[(coord['Country name EN'] == coord['countries'])]
    coord['lats'] = coord['lats'].astype(float)
    coord['longs'] = coord['longs'].astype(float)
    coord['dummy_column_for_size'] = 12
    return coord


country_collection = download_df()
coordinates = prep_df(locations, countries, country_collection)
prague_lat = coordinates[coordinates['city_name'] == 'Prague']['lats'].values[0]
prague_lon = coordinates[coordinates['city_name'] == 'Prague']['longs'].values[0]


def make_fig(coord):
    px.set_mapbox_access_token(
        'pk.eyJ1IjoiYW5zbGEiLCJhIjoiY2w1d3JwMDEyMGU0NDNkcGltMjNicDI1biJ9.nEww_FHimU8Klrqc-qhNTg')  # Токен из mapbox
    fig = px.scatter_mapbox(coord, lon=coord['longs'], lat=coord['lats'], custom_data=['city_name'],
                            mapbox_style='dark', size='dummy_column_for_size', color_discrete_sequence=['#527066'],
                            zoom=3, center={'lat': prague_lat, 'lon': prague_lon})
    fig.update_traces(hovertemplate='%{customdata[0]}')
    fig.update_layout(paper_bgcolor='black')
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig


def dump_json(fig):
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


graphJSON = dump_json(make_fig(coordinates))


@app.route('/')
def display():  # app code here
    return render_template('index.html', graphJSON=graphJSON)


# for continuous deployment through GitHub webhooks:
@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./portfolio_webapp')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
