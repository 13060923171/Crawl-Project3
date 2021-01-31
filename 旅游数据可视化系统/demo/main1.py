from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

x_data = ['价格优惠多','产品丰富','攻略详细','旅游网','点评','亲朋好友']
y_data1 = ['42','40','39','35','35','17']
y_data2 = ['58','42','45','65','65','83']


c = (
    Bar(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.ROMANTIC))
    .add_xaxis(x_data)
    .add_yaxis("普通旅游用户（%）", y_data1, stack="stack1")
    .add_yaxis("去哪儿用户（%）", y_data2, stack="stack1")
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=False, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            name="人数占比",
            type_="value",
            min_=0,
            max_=100,
            interval=20,
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="游客餐饮信息获取渠道/旅游平台网站考虑,因素"))
    .render("图一.html")
)