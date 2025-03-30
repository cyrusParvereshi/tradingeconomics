from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from data import obtain_data, clean_data, plot_data, read_api_key
import io


app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Home Page</p>"

@app.route('/test')
def chartTest():
  create_figure()
  # plt.savefig('/static/images/new_plot.png')
  return render_template('index.html', name = 'new_plot', url ='/static/img/graph.png')

def create_figure():
    api_key = read_api_key()
    (mfg_mex_gdp, mx_unemp) = obtain_data(api_key)
    df_combo = clean_data(mfg_mex_gdp, mx_unemp)
    fig = plot_data(df_combo, False)
    fig.savefig('./static/img/graph.png')
    return fig