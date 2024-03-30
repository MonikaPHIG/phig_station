import plotly.graph_objects as go

def make_bar_plot(x, y, color, dp):
    plot = go.Bar(
            x=x,
            y=y,
            marker_color=color,
            text=y,
            textposition='outside'
        )
    
    plot.text = [('%.' + dp + 'f') % float(val) for val in y]

    return plot

def make_indicator_plot(value, unit, min, max, color):
    plot = go.Indicator(
        gauge={'axis': {
                'range': [min, max]
            },
            'bar': {
                'color': color,
                'thickness': 1
            },
            'bgcolor': '#eeeeee'},
        mode='gauge+number',
        number={
            'suffix': unit
        },
        value=value
    )

    return plot

def make_barpolar_plot(angle):
    plot = go.Barpolar(
        r=[1],
        theta=[angle],
        width=[14.573],
        marker_color=["#3188c2"]
    )

    return plot