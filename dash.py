import sqlite3
import pandas as pd
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Label, LabelSet
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.palettes import Spectral9, Viridis256

date = '2017-09-22'
output_file("dashboard.html", title='Chester Student Accomodation Analysis')
conn = sqlite3.connect("student_data.db")
sql_byarea = "select Sum(BedroomsAvailable) as RoomsAvailable, Area from student_data where Date='" + \
    date + "' group by Area;"
sql_bytype = "select Sum(BedroomsAvailable) as RoomsAvailable, Title As Area from student_data where Date='" + \
    date + "' group by Title;"
sql_total = "select Sum(BedroomsAvailable) as RoomsAvailable from student_data where Date='" + date + "';"


totalrooms = pd.read_sql_query(sql_total, conn)

totalrooms = str(totalrooms.iloc[0]['RoomsAvailable'])

df = pd.read_sql_query(sql_byarea, conn)
roomsavailable = df['RoomsAvailable'].tolist()
area = df['Area'].tolist()
source = ColumnDataSource(
    data=dict(area=area, roomsavailable=roomsavailable, color=Spectral9))
max_room = int(20 * round(float(max(roomsavailable)) / 20))
# Rooms by Area
p = figure(y_range=area,  x_range=(0, max_room), plot_width=600, plot_height=550, toolbar_location=None,
           title="Chester Student Rooms Available as of " + date)
p.hbar(y='area', left=0, right='roomsavailable',
       color='color', height=0.8, source=source)
labels = LabelSet(x='roomsavailable', y='area', text='roomsavailable', text_font_size='8pt', level='glyph',
                  x_offset=-20, y_offset=-8.5, source=source, render_mode='canvas')
p.add_layout(labels)
p.ygrid.grid_line_color = None
p.xaxis.axis_label = "Available Rooms"
p.outline_line_color = None

headline = Label(x=0, y=-100, x_units='screen', y_units='screen',
                 text="Total Rooms Available: " + totalrooms, render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
p.add_layout(headline)


citation = Label(x=400, y=-100, x_units='screen', y_units='screen',
                 text='Data sourced from www.chesterstudentstamp.co.uk', render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
p.add_layout(citation)


# ByType
df_type = pd.read_sql_query(sql_bytype, conn)
roomsavailable = df_type['RoomsAvailable'].tolist()
area = df_type['Area'].tolist()
source = ColumnDataSource(data=dict(area=area, roomsavailable=roomsavailable))
max_room = int(20 * round(float(max(roomsavailable)) / 20))

q = figure(y_range=area,  x_range=(0, max_room), plot_width=600, plot_height=550, toolbar_location=None,
           title="Available Rooms by location as of " + date)
q.hbar(y='area', left=0, right='roomsavailable',
       color='lightblue', height=0.8, source=source)

q.ygrid.grid_line_color = None
q.xaxis.axis_label = "Available Rooms"
q.outline_line_color = None


# show(p)
show(row(p, q))


