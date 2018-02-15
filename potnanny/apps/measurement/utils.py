CHARTBASE = {
    'type': 'line',
    'options': {
        'responsive': True,
        'maintainAspectRatio': False,
        'animation': {
            'duration': 0
        },
        'scales': {
            'xAxes': [{
                'display': False
            }],
            'yAxes': [{
                'ticks': {
                    'beginAtZero': False
                }
            }],
        },
        'legend': {
            'display': False,
            'position': 'bottom',
            'labels': {
                'boxWidth': 8
            }
        }
    },
    'data': {
        'labels': [],
        'datasets': []
    }
}


class ChartColor(object):
    def __init__(self, index):
        self.colors = [
            # "rgb(120, 200, 0)",
            # "rgb(20, 140, 220)",
            # "rgb(220, 70, 20)",
            # "rgb(220, 220, 130)",
            # "rgb(220, 180, 130)",

            "rgb(255, 193, 7)",
            "rgb(104, 159, 56)",
            "rgb(139, 195, 74)",
            "rgb(33, 33, 33)",
            "rgb(220, 180, 130)",            
        ]
        self.index = index

    def rgb_color(self):
        return self.colors[self.index % len(self.colors)]

