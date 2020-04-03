﻿Imports FusionCharts.Charts
Partial Class Pages_ChartlightDataPoint
    Inherits System.Web.UI.Page
    Protected Sub Page_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        'store chart  data url as  string
        Dim jsonData As String
        jsonData = "{            'chart': {                'caption': 'Bakersfield Central - Total footfalls',                'subCaption': 'Last week',                'xAxisName': 'Day',                'yAxisName': 'No. of Visitors (In 1000s)',                'showValues': '0',                'theme': 'fusion'            },        'annotations':{            'groups': [                {                    'id': 'anchor-highlight',                    'items': [                        {                            'id': 'high-star',                            'type': 'circle',                            'x': '$dataset.0.set.2.x',                            'y': '$dataset.0.set.2.y',                            'radius': '12',                            'color': '#6baa01',                            'border': '2',                            'borderColor': '#f8bd19'                        },                        {                            'id': 'label',                            'type': 'text',                            'text': 'Highest footfall 25.5K',                            'fillcolor': '#6baa01',                            'rotate': '90',                            'x': '$dataset.0.set.2.x+75',                            'y': '$dataset.0.set.2.y-2'                        }                    ]                }            ]        },            'data': [                {                    'label': 'Mon',                    'value': '15123'                },                {                    'label': 'Tue',                    'value': '14233'                },                {                    'label': 'Wed',                    'value': '25507'                },                {                    'label': 'Thu',                    'value': '9110'                },                {                    'label': 'Fri',                    'value': '15529'                },                {                    'label': 'Sat',                    'value': '20803'                },                {                    'label': 'Sun',                    'value': '19202'                }            ]        }"
        'create gauge instance
        'chart type, chart id, width, height, data format, data source as url
        Dim columnChart As New Chart("column2d", "columnchart", "700", "400", "json", jsonData)
        'render gauge
        Literal1.Text = columnChart.Render()
    End Sub
End Class
