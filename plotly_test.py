import plotly.graph_objects as go
import numpy as np

n_timesteps = 100
l, w = 1, 0.5
pos_traj = np.array([
    np.sin(np.linspace(0, 2*np.pi, n_timesteps)),
    np.cos(np.linspace(0, 2*np.pi, n_timesteps))
])
angle_traj = np.linspace(2*np.pi, 0, n_timesteps)


def R(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])


shape_traj = np.array([[
    pos_traj[:, i] + R(angle_traj[i])@[l/2, w/2],
    pos_traj[:, i] + R(angle_traj[i])@[l/2, -w/2],
    pos_traj[:, i] + R(angle_traj[i])@[-l/2, -w/2],
    pos_traj[:, i] + R(angle_traj[i])@[-l/2, w/2],
    pos_traj[:, i] + R(angle_traj[i])@[l/2, w/2]
    ] for i in range(n_timesteps)
])

fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(
    x=[],
    y=[],
    mode="lines",
    name="position"
))

fig.add_trace(go.Scatter(
    x=[],
    y=[],
    mode="lines",
    name="ship shape"
))

# Set up frames
frame_data: list[go.Frame] = [[] for _ in range(n_timesteps)]

for i in range(n_timesteps):
    frame_data[i].append(go.Scatter(
        x=pos_traj[0, :i+1], y=pos_traj[1, :i+1],
        mode="lines", name="position"))

    frame_data[i].append(go.Scatter(
        x=shape_traj[i, :, 0], y=shape_traj[i, :, 1],
        mode="lines", name="ship shape"))

fig.frames = [
    go.Frame(data=frame, name=str(i))
    for i, frame in enumerate(frame_data)
]

fig.update_layout(
    xaxis=dict(range=[-20, 20]),
    yaxis=dict(scaleanchor="x", scaleratio=1),
)

fig.update_layout(
    updatemenus=[{
        'buttons': [
            {
                'args': [
                    None,
                    {
                        'frame': {'duration': 0, 'redraw': True},
                        'fromcurrent': True
                    }
                ],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [
                    [None],
                    {
                        'frame': {'duration': 0, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }
                ],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }],
    sliders=[{
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 10},
            'prefix': 'Time step: ',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 0},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': [{
            'args': [
                [str(k)],
                {
                    'frame': {'duration': 0, 'redraw': True},
                    'mode': 'immediate'
                }
            ],
            'label': str(k),
            'method': 'animate',
        } for k in range(0, n_timesteps)]
    }]
)

fig.show()
