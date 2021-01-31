from pyecharts import options as opts
from pyecharts.charts import Bar, Line

from pyecharts.globals import ThemeType

v1 = [70,80,90,100,110]
v2 = ['75','85','92','105','115']
x_data = ['2013','2014','2015','2016','2017']


bar = (
    Bar(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.ESSOS))
    .add_xaxis(x_data)
    .add_yaxis("国内旅游人数情况", v1)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="国内旅游人数情况/出境旅游"),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
    )
)

line = (
    Line(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.ESSOS))
    .add_xaxis(x_data)
    .add_yaxis('出境旅游',v2)
)
bar.overlap(line)
bar.render("图五.html")