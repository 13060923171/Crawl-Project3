from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType

x_data = ['城镇居民','农村居民']
y_data = ['82','18']
c = (
    Pie(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.ROMANTIC))
    .add("", [list(z) for z in zip(x_data,y_data)])
    .set_global_opts(title_opts=opts.TitleOpts(title="国内旅游收入分布情况<城镇居民/农村居民>"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    .render("图二.html")
)