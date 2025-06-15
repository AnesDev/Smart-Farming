import plotly.graph_objects as go
import streamlit as st
import altair as alt

# === plotter les jauges ===
def plot_gauge(value, metric_name, min_val, max_val, green_range, orange_range=None, red_ranges=None):
    steps = []
    if red_ranges:
        for r in red_ranges:
            steps.append({'range': r, 'color': 'red'})
    if orange_range:
        steps.append({'range': orange_range, 'color': 'orange'})
    steps.append({'range': green_range, 'color': 'green'})

    boundaries = set()
    for step in steps:
        start, end = step['range']
        boundaries.add(start)
        boundaries.add(end)

    boundaries.add(min_val)
    boundaries.add(max_val)
    boundaries = sorted(boundaries)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': metric_name},
        gauge={
            'axis': {
                'range': [min_val, max_val],
                'tickvals': boundaries,
                'ticktext': [str(b) for b in boundaries]
            },
            'bar': {'color': "darkblue"},
            'steps': steps,
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': value}
        }
    ))
    fig.update_layout(height=250, width=250,
                      margin=dict(t=20, b=20, l=20, r=20),
                      paper_bgcolor='#ECFAE5',
                      plot_bgcolor='#ECFAE5')

    st.plotly_chart(fig, use_container_width=False, key=f"gauge_{metric_name}_{id(value)}")



# === plotter la direction du vent ===

def plot_wind_direction_gauge(direction_deg: float, magnitude: float = 2.5, max_magnitude: float = 3.0):
    fig = go.Figure()
    fig.add_trace(go.Barpolar(
        r=[magnitude],
        theta=[direction_deg],
        width=[180],
        marker_color="orange",
        marker_line_color="black",
        marker_line_width=2,
        opacity=0.8
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='black',
            angularaxis=dict(
                rotation=90,
                direction="clockwise",
                tickmode='array',
                tickvals=[0, 90, 180, 270],
                ticktext=["N", "E", "S", "W"],
            ),
            radialaxis=dict(range=[0, max_magnitude], showticklabels=True, ticks='')
        ),
        showlegend=False,
        height=200,
        width=200,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='#ECFAE5',
        plot_bgcolor='#ECFAE5'
    )

    st.plotly_chart(fig)

# === Obtenir la couleur par valeur ===
def get_color_for_value(value, green_range, orange_range, red_ranges):
    if green_range[0] <= value <= green_range[1]:
        return "#9bffba"  # Green
    elif orange_range[0] <= value <= orange_range[1]:
        return "#ffe193"  # Orange
    else:
        for low, high in red_ranges:
            if low <= value <= high:
                return "#ffa184"  # Red
    return "#ffa184"  # Default to red


def style_plant_table1(df):
    ranges = {
        "Température du sol (°C)": ([18, 30], [30, 35], [(0, 18), (35, 50)]),
        "Humidité du sol (%)": ([40, 70], [30, 40], [(0, 30), (70, 100)]),
        "Température de l'air (°C)": ([20, 35], [35, 40], [(0, 20), (40, 60)]),
        "Humidité de l'air (%)": ([40, 70], [30, 40], [(0, 30), (70, 100)])
    }

    def apply_color(row):
        param = row["Paramètre"]
        val = float(row["valeur"].split()[0])

        green, orange, red = ranges[param]
        color = get_color_for_value(val, green, orange, red)
        return [f'background-color: {color}' if col == 'valeur' else '' for col in row.index]

    return df.style.apply(apply_color, axis=1)


def style_both_plants(df, col1, col2):
    ranges = {
        "Température du sol (°C)": ([18, 30], [30, 35], [(0, 18), (35, 50)]),
        "Humidité du sol (%)": ([40, 70], [30, 40], [(0, 30), (70, 100)]),
        "Température de l'air (°C)": ([20, 35], [35, 40], [(0, 20), (40, 60)]),
        "Humidité de l'air (%)": ([40, 70], [30, 40], [(0, 30), (70, 100)])
    }

    def apply_color(row):
        param = row["Paramètre"]

        green, orange, red = ranges[param]

        styles = []
        for col in row.index:
            if col == col1 or col == col2:
                val = float(row[col].split()[0])
                color = get_color_for_value(val, green, orange, red)
                styles.append(f'background-color: {color}')
            else:
                styles.append('')

        return styles

    return df.style.apply(apply_color, axis=1)


def plot_altair(df, y_column, label, line_color="#29740b", bg_color="#E6F6DD"):
    chart = (
        alt.Chart(df)
        .mark_line(color=line_color, strokeWidth=3)
        .encode(
            x=alt.X(
                "date:T",
                title="Date",
                axis=alt.Axis(
                    format="%d %b",
                    tickCount="day",
                    labelColor="#174206",
                    titleColor="#174206",
                    grid=False,
                ),
            ),
            y=alt.Y(f"{y_column}:Q", title=label),
        )
        .properties(
            width=600,
            height=300,
            background=bg_color,
        )
        .configure_axis(
            labelFontSize=12,
            titleFontSize=14,
        )
        .configure_view(
            stroke="#1b4d07"
        )
        .interactive(bind_x=True)
    )

    return chart
