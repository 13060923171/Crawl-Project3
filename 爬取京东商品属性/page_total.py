from pyecharts.charts import Page
from main_bar import main_bar
from main_line import main_line
from main_pie import main_pie
from main_radar import main_radar
from main_word import main_word
from main_reversal import main_reversal
from main_funnel import main_funnel
from main_scatter import main_scatter

def page_draggable_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        main_bar(),
        main_line(),
        main_pie(),
        main_radar(),
        main_word(),
        main_reversal(),
        main_funnel(),
        main_scatter()

    )
    page.save_resize_html(cfg_file="chart_config.json")
    # page.render()

if __name__ == '__main__':
    page_draggable_layout()