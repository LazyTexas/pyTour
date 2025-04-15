from pyecharts.charts import Bar, Line
from pyecharts import options as opts

from pyecharts.faker import Faker
from pyecharts.globals import ThemeType, RenderType

c = (
    Bar(
        # InitOpts: 初始化配置项
        init_opts=opts.InitOpts(
            width='700px',
            height='400px',  # 图表画布大小，css长度单位
            renderer=RenderType.CANVAS,  # 渲染风格,可选：canvas,svg
            page_title='网页标题',
            theme=ThemeType.WHITE,  # 主题
            bg_color='white'  # 背景颜色
        )
    )
    .add_xaxis(Faker.choose())

    .add_yaxis('商家A', Faker.values())
    .add_yaxis('商家B', Faker.values())

    # 全局配置项
    .set_global_opts(

        # TitleOpts: 标题配置项
        title_opts=opts.TitleOpts(
            title='柱形图',  # 主标题
            title_link='https://www.baidu.com',  # 主标题点击跳转链接
            title_target='blank',  # blank新窗口打开，self 当前窗口打开

            subtitle='副标题',  # 副标题
            subtitle_link='https://www.baidu.com',
            subtitle_target='blank',

            # 位置
            pos_left='20px',
            pos_top='0px',
            # pos_right
            # pos_bottom
            padding=10,  # 内边距
            item_gap=5,  # 主标题和副标题之间的间隙
        ),

        # DataZoomOpts：区域缩放配置项
        datazoom_opts=opts.DataZoomOpts(
            is_show=True,  # 是否显示组件
            type_='slider',  # 组件的类型：slider, inside
            is_realtime=True,  # 拖动时是否实时更新图表
            range_start=20,  # 数据窗口的起始百分比
            range_end=80,  # 数据窗口的结束百分比
            orient='horizontal',  # horizontal 或 vertical
            is_zoom_lock=False,  # 是否锁定选择区域
        ),

        # LegendOpts: 图例配置项
        legend_opts=opts.LegendOpts(
            # 图例类型： plain普通图例，scroll:可以滚动翻页的图例,用于图例较多的情况
            type_='plain',
            is_show=True,  # 是否显示图例
            pos_left='20%',  # 图例位置:pos_left,pos_right,pos_top,pos_bottom
            orient='vertical',  # horizontal 或 vertical

            # 选择模式
            #  True: 开启图例点击
            #  False: 关闭图例点击
            #  single: 单选
            #  multiple: 多选
            selected_mode="multiple",

            # 图标和文字的位置
            align='left',
            padding=10,  # 内边距
            item_gap=5,  # 图例中每项之间的间距
            item_width=30,  # 项的宽度
            item_height=15,  # 项的高度
            inactive_color='#ccc',  # 图例关闭时的颜色,

            # PyEcharts常见的图标： circle,rect,roundRect,triangle, diamond,arrow
            legend_icon='roundRect'
        ),

        # VisualMapOpts：视觉映射配置项
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            type_='color',  # color 或 size
            min_=0,  # 最小值
            max_=150,  # 最大值
            range_opacity=0.7,  # 图元和文字透明度
            range_text=['max', 'min'],  # 两端的文本
            range_color=['blue', 'green', 'red'],  # 过渡颜色

            orient='vertical',  # horizontal 或 vertical
            pos_right='5%',
            pos_top='0%',
            is_piecewise=True,  # 是否为分段型
            is_inverse=True  # 是否反转
        ),

        # TooltipOpts: 提示框配置项
        tooltip_opts=opts.TooltipOpts(
            is_show=True,

            # 触发类型
            #  item: 数据项，一般用于:散点图，柱形图，饼图
            #  axis: 坐标轴，提示线，主要用于条形图，折线图等
            trigger='item',
            # 触发条件：
            #  mousemove, click, mousemove|click
            trigger_on='click',

            is_show_content=True,  # 是否显示提示框浮层

            # 标签内容的格式
            #  字符串中的模板变量：
            #  {a}: 系列名series_name
            #  {b}: 数据名
            #  {c}：值
            formatter='{a}: {b}-{c}',

            background_color='black',  # 背景颜色
            border_color='white',  # 边框颜色
            border_width=1,  # 边框宽度
        ),

        # AxisOpts: 坐标轴配置项
        xaxis_opts=opts.AxisOpts(
            is_show=True,  # 是否显示X轴

            # 坐标轴类型:
            #   value: 数值轴，用于连续数据
            #   category: 类目轴，适用于离散数据，比如：星期一，星期二等
            #   time: 时间轴，适用于连续的时序数据
            type_='category'
        ),

        yaxis_opts=opts.AxisOpts(
            # is_show=False,
            # 不显示y轴的线
            axisline_opts=opts.AxisLineOpts(is_show=False),
            # 不显示y轴的刻度
            axistick_opts=opts.AxisTickOpts(is_show=False)

        )
    )

)
c.render()

from pyecharts.faker import Faker
from pyecharts.charts import Pie
import pyecharts.options as opts

v = Faker.choose()
[list(i) for i in zip(v, Faker.values())]
c = (
    Pie()
    .add(
        '',
        [list(i) for i in zip(v, Faker.values())],
        radius=['30%', '75%'],
        center=['25%', '50%'],
        rosetype='radius',
        label_opts=opts.LabelOpts(is_show=False)  # 不显示标签
    )
    .add(
        '',
        [list(i) for i in zip(v, Faker.values())],
        radius=['20%', '55%'],
        center=['75%', '50%'],
        rosetype='area',
        label_opts=opts.LabelOpts(is_show=True)  # 显示标签
    )
    .set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图'))
)
c.render()