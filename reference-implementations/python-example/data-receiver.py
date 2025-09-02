# Simple data receiver
# Connects to the broker and subscribes to a topic
#
# Expects that stations are differentiated by topics. 
# Receives both the metadata and the values; stores the latest metadata and displays received values on the graph. 
#
# Run it as in the following example:
# python3 data-receiver.py --broker s87beff9.ala.eu-central-1.emqxsl.com --port 8883 --tls --insecure --topic "firstmile/#"  --username geolux --password "XXXX"
#
# After starting the receiver, open the following URL in the browser: http://localhost:8050

import argparse
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from protospy import firstmile_pb2 as pb2
from google.protobuf.json_format import MessageToDict
import threading
import queue
import json
import pandas as pd
import paho.mqtt.client as mqtt
import ssl
import re


state = {}
message_queue = queue.Queue()
metadata_queue = queue.Queue()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(userdata["topic"])

def on_message(client, userdata, msg):
    print("Received message on topic:", msg.topic)
    topic = msg.topic
    payload = msg.payload

    if re.match(r"firstmile/.*/metadata/.*", topic):
        metadata = pb2.Metadata()
        metadata.ParseFromString(payload)
        d = MessageToDict(metadata)
        metadata_queue.put((topic, d))
    elif re.match(r"firstmile/.*/data/.*", topic):
        transmission = pb2.Data()
        transmission.ParseFromString(payload)
        d = MessageToDict(transmission)
        message_queue.put((topic, d))


# MQTT handler
def start_mqtt(broker, port, topic, username=None, password=None, tls=None):
    client = mqtt.Client(userdata={"topic": topic})

    if username and password:
        client.username_pw_set(username, password)

    if tls:
        client.tls_set(
            ca_certs=tls.get("ca_cert"),
            certfile=tls.get("client_cert"),
            keyfile=tls.get("client_key"),
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        client.tls_insecure_set(tls.get("insecure", False))

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_start()


# UI display
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content"),
    dcc.Interval(id="interval", interval=2*1000, n_intervals=0)
])

def render_home_page():
    cards = []

    if not state:
        return html.P("No topics received yet.")

    for topic, site_data in state.items():
        metadata_exists = "metadata" in site_data
        n_obs = len(site_data.get("data", []))
        card = dbc.Card([
            dbc.CardHeader(html.H5(topic)),
            dbc.CardBody([
                html.P(f"Metadata received: {'Yes' if metadata_exists else 'No'}"),
                html.P(f"Observations received: {n_obs}"),
                dbc.Button("View details", href=f"/site/{topic}", color="primary")
            ])
        ], className="mb-3")
        cards.append(card)

    return dbc.Container(cards)

def render_site_page(topic):
    if topic not in state:
        return html.P(f"No data for topic {topic}")

    site_data = state[topic]

    warnings_ui = []
    for w in site_data.get("warnings", []):
        warnings_ui.append(html.P(w, style={"color": "red"}))

    metadata_json = json.dumps(site_data.get("metadata", {}), indent=2)

    graphs_ui = []
    obs_list = site_data.get("data", [])
    if obs_list:
        df_all = []
        for obs in obs_list:
            param_id = obs.get("parameterDefinitionId")
            time_str = obs.get("time", None)

            for i, val in enumerate(obs.get("values", [])):
                for k, v in val.items():
                    df_all.append({
                        "paramId": param_id,
                        "paramIndex": i,
                        "kind": k,
                        "timestamp": time_str,
                        "value": v
                    })

        if df_all:
            df = pd.DataFrame(df_all)

            # Group by paramId → one graph per paramId
            for paramId, param_group in df.groupby("paramId"):
                fig = go.Figure()

                for (paramIndex, kind), series_group in param_group.groupby(["paramIndex", "kind"]):
                    series_name = f"Value {paramIndex} ({kind})"
                    fig.add_trace(go.Scatter(
                        x=series_group["timestamp"],
                        y=series_group["value"],
                        mode='lines+markers',
                        name=series_name
                    ))

                # Lookup metadata for graph title and unit
                param_name = f"Param ID {paramId}"
                unit = ""

                meta = site_data.get("metadata")
                if meta:
                    param_defs = meta.get("parameterDefinitions", [])
                    for pdef in param_defs:
                        if str(pdef["id"]) == str(paramId):
                            if pdef.get("parameters"):
                                names = []
                                units = set()
                                for param in pdef["parameters"]:
                                    names.append(param.get("longName", ""))
                                    unit_val = param.get("unit", "")
                                    if unit_val:
                                        units.add(unit_val)
                                param_name = ", ".join([n for n in names if n])
                                unit = ", ".join(units)
                            break

                fig.update_layout(
                    title=f"{param_name} (Unit: {unit})"
                )

                graphs_ui.append(dcc.Graph(figure=fig))
        else:
            graphs_ui.append(html.P("No data to plot yet."))
    else:
        graphs_ui.append(html.P("No observations yet."))

    return dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Button("⬅ Back", href="/", color="secondary"), width="auto")
        ]),
        html.H3(f"Site: {topic}"),
        *warnings_ui,
        html.H5("Metadata:"),
        html.Pre(metadata_json, style={"maxHeight": "300px", "overflowY": "scroll"}),
        html.H5("Graphs:"),
        *graphs_ui
    ])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("interval", "n_intervals")
)
def update_page(pathname, n_intervals):
    # Process queued MQTT metadata messages
    while not metadata_queue.empty():
        topic, msg = metadata_queue.get()

        # use regex to extract vendor and hostid from the topic in format firstmile/{vendor}/metadata/{hostid}
        match = re.match(r"firstmile/([^/]+)/metadata/([^/]+)", topic)
        if match:
            vendor = match.group(1)
            hostid = match.group(2)
            key = f"{vendor}/{hostid}"

            if key not in state:
                state[key] = {
                    "last_messages": [],
                    "data": [],
                    "warnings": []
                }

            state[key]["metadata"] = msg
            state[key]["last_messages"].append(msg)
            state[key]["last_messages"] = state[key]["last_messages"][-20:]

    # Process queued MQTT data messages
    while not message_queue.empty():
        topic, msg = message_queue.get()

        # use regex to extract vendor and hostid from the topic in format firstmile/{vendor}/metadata/{hostid}
        match = re.match(r"firstmile/([^/]+)/data/([^/]+)", topic)
        if match:
            vendor = match.group(1)
            hostid = match.group(2)
            key = f"{vendor}/{hostid}"

            if key not in state:
                state[key] = {
                    "last_messages": [],
                    "data": [],
                    "warnings": []
                }

            if "metadata" not in state[key]:
                warning = f"⚠️ WARNING: Data for topic {topic} arrived with no metadata and no cached metadata."
                print(warning)
                state[key]["warnings"].append(warning)

            state[key]["last_messages"].append(msg)
            state[key]["last_messages"] = state[key]["last_messages"][-20:]

            state[key]["data"].extend(msg.get("observations", []))
            # Limit stored data to avoid memory growth
            MAX_OBS = 500
            if len(state[key]["data"]) > MAX_OBS:
                state[key]["data"] = state[key]["data"][-MAX_OBS:]

    # Routing
    if pathname == "/" or pathname == "":
        return render_home_page()
    elif pathname.startswith("/site/"):
        key = pathname.replace("/site/", "", 1)
        return render_site_page(key)
    else:
        return html.P("Unknown page.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AWS MQTT Data Receiver PoC")
    parser.add_argument("--broker", required=True, help="MQTT broker address")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic", required=True, help="MQTT topic")
    parser.add_argument("--username", help="MQTT username (optional)")
    parser.add_argument("--password", help="MQTT password (optional)")
    parser.add_argument("--tls", action="store_true", help="Enable TLS (MQTTS)")
    parser.add_argument("--ca-cert", help="CA certificate file for TLS connection")
    parser.add_argument("--client-cert", help="Client certificate file for mutual TLS (optional)")
    parser.add_argument("--client-key", help="Client private key file for mutual TLS (optional)")
    parser.add_argument("--insecure", action="store_true", help="Skip server certificate verification")

    args = parser.parse_args()

    start_mqtt(
        broker=args.broker,
        port=args.port,
        topic=args.topic,
        username=args.username,
        password=args.password,
        tls={
            "ca_cert": args.ca_cert,
            "client_cert": args.client_cert,
            "client_key": args.client_key,
            "insecure": args.insecure
        } if args.tls else None
    )

    app.run(host="0.0.0.0", port=8050, debug=True)
