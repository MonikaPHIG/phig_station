import plotly.graph_objects as go

def bar(title, x, y, color, unit):
    fig = go.Figure(
        data=go.Bar(
            x=x,
            y=y,
            marker_color=color,
            text=y,
            textposition='outside'
        )
        )
    
    fig.update_layout(
        title={
            'font': {
                'size': 48
            },
            'text': title
        }
    )

    fig.update_yaxes(
        ticksuffix=unit
    )

    return fig

def gauge(title, value, unit, min, max, color):
    fig = go.Figure(go.Indicator(
        domain={
            'x': [0, 1],
            'y': [0, 1]
        },
        gauge={
            'axis': {
                'range': [min, max]
            },
            'bar': {
                'color': color,
                'thickness': 1
            },
            'bgcolor': '#eeeeee'
        },
        mode='gauge+number',
        number={
            'suffix': unit
        },
        title={
            'font': {
                'size': 48
            },
            'text': title
        },
        value=value
    ))

    return fig

def rose():
    fig = go.Figure(go.Barpolar(
        r=[1],
        theta=[270],
        width=[20],
        marker_color=["#3188c2"],
    ))

    fig.update_layout(
        title={
            'font': {
                'size': 48
            },
            'text': 'Wind Direction'
        }
    )

    return fig