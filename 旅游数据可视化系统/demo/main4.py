from pyecharts import options as opts
from pyecharts.charts import Grid, Liquid
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Page
l1 = (
    Liquid()
    .add(
        "线上预订",
        [0.261],
        center=["60%", "50%"],
        is_outline_show=False,
        color='Yellow',
        label_opts=opts.LabelOpts(
             font_size=50,
             formatter=JsCode(
                 """function (param) {
                         return (Math.floor(param.value * 10000) / 100) + '%';
                     }"""
             ),
             position="inside",
         ),
         )
)

l2 = Liquid().add(
    "线下预订",
    [0.251],
    center=["25%", "50%"],
    is_outline_show=False,
    label_opts=opts.LabelOpts(
        font_size=50,
        formatter=JsCode(
            """function (param) {
                    return (Math.floor(param.value * 10000) / 100) + '%';
                }"""
        ),
        position="inside",
    ),
)
x_data = ['去哪儿了','百度/谷歌','携程网']
y_data1 = ['30','60','20']
y_data2 = ['30','40','40']
c = (
    Bar(init_opts=opts.InitOpts(width="1300px", height="600px",theme=ThemeType.LIGHT))
    .add_xaxis(x_data)
    .add_yaxis("线下用户信息探索（%）", y_data1,stack="stack1",label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("线上用户信息,搜索(%)", y_data2,stack="stack1",label_opts=opts.LabelOpts(is_show=False))
    .reversal_axis()
    .set_global_opts(
                title_opts=opts.TitleOpts("中国亲子旅游占国内旅游用户的比重情况/线上预订、线下预订",pos_left="35%", pos_top="5%")
            )
)


page = Page(layout=Page.DraggablePageLayout)
page.add(
    l1,
    l2,
    c,

)
page.save_resize_html(cfg_file="chart_config.json")
# page.render()

