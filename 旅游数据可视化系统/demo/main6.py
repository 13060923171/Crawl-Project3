from pyecharts import options as opts
from pyecharts.charts import Bar, Line

from pyecharts.globals import ThemeType

v1 = [11000000,7800000,]
v2 = ['1400000','1000000']
x_data = ['组团人数','持续人数']


bar = (
    Bar(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.MACARONS))
    .add_xaxis(x_data)
    .add_yaxis("本月(人次)", v1,category_gap="80%")
    .extend_axis(
        yaxis=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"), interval=500000
        )
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="旅行社团内旅游组团人数和接待人数"),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}"),interval=2000000),
    )
)

line = Line().add_xaxis(x_data).add_yaxis("同地增长(%)", v2, yaxis_index=1)
bar.overlap(line)
bar.render("图六.html")