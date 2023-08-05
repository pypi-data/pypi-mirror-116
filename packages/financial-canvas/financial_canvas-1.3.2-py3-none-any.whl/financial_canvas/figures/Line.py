
from bokeh.models import DatetimeTickFormatter
from bokeh.models.tools import HoverTool
from financial_canvas.figures.constants import COLOR_PALLETE
from financial_canvas.figures.CustomFigure import CustomFigure
from bokeh.models import Span


class Line(CustomFigure):
    '''
    Simple line chart with y axis autorange
    '''

    def __init__(self, df, *, column_name, figure_args, selected_from=None, color=None, x_range=None):

        # TODO: update dynamically
        self.y_range_resize_columns = [column_name]

        super().__init__(df, selected_from=selected_from)

        tooltips = [
            ('Date', '@index{%d/%m/%Y  %H:%M}'),
            (column_name, '@' + column_name + '{%f}'),
        ]

        formatters = {
            '@index': 'datetime',
            '@' + column_name: 'printf',
        }

        # using only sources (not origins) to build initial graphs
        # if switching to bokeh CDSView needs to be changed
        full_source = self.sources['main'][0]
        bokeh_figure = self.get_figure_defaults()

        x_range = x_range if x_range else (
            full_source.data['index'][0], full_source.data['index'][-1])
        p = bokeh_figure(
            x_axis_type="datetime",
            # x_axis_location="above",
            toolbar_location='right',
            tools="pan,wheel_zoom,box_zoom,save",
            active_drag='pan',
            active_scroll='wheel_zoom',
            # need to set custom x_range here, because otherwise
            # the preview slider will crash with the following error:
            # ValueError: expected an instance of type Range1d, got DataRange1d(id='1006', ...) of type DataRange1d
            # also used to set up initial zoom if passed
            x_range=x_range,
            **figure_args,
        )

        p.toolbar.logo = None

        ticks_formatter = DatetimeTickFormatter(
            years=["%Y"],
            days=["%d/%m/%Y"],
            months=["%m/%Y"],
            hours=["%H:%M"],
            minutes=["%H:%M"]
        )

        p.add_tools(HoverTool(
            tooltips=tooltips,
            formatters=formatters,
            mode='vline',
            names=['line'],
        ))

        color = color if color else COLOR_PALLETE[2]

        # zero horizontal line
        zero_hline = Span(location=0,
                          dimension='width', line_color='gray',
                          line_dash='dashed', line_width=1)
        p.add_layout(zero_hline)

        # line chart
        p.line('index', column_name,
               legend_label=column_name,
               name='line',
               line_color=color,
               source=full_source)

        # legend
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"

        # layout
        # TODO: add to defaults
        p.xaxis.formatter = ticks_formatter
        p.axis.minor_tick_line_color = None
        p.axis.major_tick_line_color = None
        p.outline_line_color = None
        p.axis.axis_line_width = 0
        p.axis.major_tick_out = 8
        p.axis.major_tick_in = 0

        self.p = p
        self.y_axis_autorange()
