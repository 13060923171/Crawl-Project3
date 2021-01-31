import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType


x_data = ["吉林", "云南", "西藏", "上海",]

(
    Line(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="春季",
        y_axis=[90, 81, 82, 85],
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=4),
    )
    .add_yaxis(
        series_name="夏季",
        y_axis=[85,95, 92, 90,],
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=4),
    )
    .add_yaxis(
        series_name="秋季",
        y_axis=[82, 87, 88, 82],
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=4),
    )
    .add_yaxis(
        series_name="冬季",
        y_axis=[80, 79, 78, 77],
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=4),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="春/夏/秋/冬/旅游成本指数省份"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
    .render("图三.html")
)

