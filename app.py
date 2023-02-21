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


locations = ['St. Moritz', 'Pontresina', 'Celerina', 'Scuol', 'Menaggio', 'London', 'Prague',
             'Lysa nad Labem', 'Corvara in Badia', 'Brunico']
countries = ['Switzerland', 'Switzerland', 'Switzerland', 'Switzerland', 'Italy', 'United Kingdom', 'Czech Republic', 'Czech Republic',
             'Italy', 'Italy']


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
        'pk.eyJ1IjoiYW5zbGEiLCJhIjoiY2w1d3JwMDEyMGU0NDNkcGltMjNicDI1biJ9.nEww_FHimU8Klrqc-qhNTg')  # Mapbox token
    fig = px.scatter_mapbox(coord, lon=coord['longs'], lat=coord['lats'], custom_data=['city_name'],
                            mapbox_style='dark', size='dummy_column_for_size', color_discrete_sequence=['#527066'],
                            zoom=3.5, center={'lat': prague_lat, 'lon': prague_lon})
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


@app.route('/corvara')
def corvara():
    return render_template('Corvara_in_Badia.html')


@app.route('/lysa_nad_labem')
def lysa():
    return render_template('Lysa_nad_Labem.html')


@app.route('/london_brixton')
def brixton():
    return render_template('London(brixton).html')


@app.route('/london_centre')
def ldn_centre():
    return render_template('London(centre).html')


@app.route('/celerina_muottas_muragl')
def muottas_muragl():
    return render_template('Celerina(muottas_muragl).html')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)
