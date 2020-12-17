import pandas as pd
import json

id                      = "1BouPWCBx9rD8ORVC3GoStxGleOwDr9vg-uql-_DG66M"
trust_boundaries        = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=trust__boundaries".format(id))
assets                  = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=assets".format(id))
security_controls       = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=security_controls".format(id))
threat_actors           = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=threat_actors".format(id))
threat_table            = pd.read_csv("https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=threat_table".format(id))
comb12                  = pd.concat([trust_boundaries,assets.rename(columns={'Asset_ID':'Trust_Boundary_ID'})], ignore_index=True)
new_col                 = threat_table['Trust_Boundary_ID'].map(comb12.set_index('Trust_Boundary_ID')['Description'])

threat_table.insert(loc = 1, column = 'Trust_Boundary_Description', value = new_col)
threat_table['Security_Control_Description'] = threat_table['Security_Control_ID'].map(security_controls.set_index('Security_Control_ID')['Description'])

new_colm                = threat_table['Threat_Actor_ID'].map(threat_actors.set_index('Threat_Actor_ID')['Description'])
new_coln                = threat_table['Threat_Actor_ID'].map(threat_actors.set_index('Threat_Actor_ID')['Skills'])

threat_table.insert(loc = 4, column = 'Threat_Actor_Description', value = new_colm)
threat_table.insert(loc = 5, column = 'Skills', value = new_coln)
threat_table.fillna(0, inplace=True)


# Auxiliar functions

def wrap_by_word(s, n):
    """
    Returns a string where \n is inserted between every n words

    :param s: string
    :param n: integer, number of words
    :return:
    """
    a                   = s.split()
    ret                 = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'
    return ret


def add_node(id_counter, label="", n=3, group="Reference", x=-950, y=-950, color="#99CDFF", shape="default", repeat_nodes = False):
    """
    Add nodes to the network
    """
    d                   = {}
    d["id"]             = id_counter

    if group            == "Reference":

        d["label"]      = label
        d["x"]          = x
        d["y"]          = y
        d["color"]      = color
        d["fixed"]      = True
        d["physics"]    = False
        if shape       != "default":
            d["shape"]  = shape
    else:

        if isinstance(label, str):
            d["label"]  = wrap_by_word(label, n)
        else:
            d["label"]  = label

        d["group"]      = group

        if group        == "TrustBoundary":
            d["color"]  = "#99CDFF"
            d["shape"]  = "circle"
            d["level"]  = 0
        elif group      == "Asset":
            d["color"]  = "#FEEBA7"
            d["shape"]  = "circle"
            d["level"]  = 0
        elif group      == "ThreatActor":
            d["color"]  = "#FFBBB2"
            d["shape"]  = "circle"
            d["level"]  = 1
        elif group      == "SecurityControl":
            d["color"]  = "#C6E7B0"
            d["shape"]  = "circle"
            d["level"]  = 4
        elif group      == "Vulnerability":
            d["color"]  = "#DAADF0"
            d["shape"]  = "box"
            d["level"]  = 2
        elif group      == "Risk":
            d["color"]  = "#FCC603"
            d["shape"]  = "box"
            d["level"]  = 3

    if repeat_nodes     == False:
        if label not in nodes_ids.keys():

            nodes_ids[label] = [id_counter]

            nodes_labels[id_counter] = label
            nodes_ns[id_counter] = n
            nodes_groups[id_counter] = group

            nodes.append(d)
            id_counter += 1
    else:
        if label not in nodes_ids.keys():
            nodes_ids[label] = [id_counter]
        else:
            nodes_ids[label].append(id_counter)

        nodes_labels[id_counter] = label
        nodes_ns[id_counter] = n
        nodes_groups[id_counter] = group

        nodes.append(d)
        id_counter += 1

    return id_counter


def add_edge(a, b, edge_id, label="", color="black", length=100):
    """
    Add edges to the network. If there are more than one edge between "a" and "b",
    use different colors for the arrows.
    """

    m = edges_pairs.count((a, b))

    if m == 0 :
        color = "black"
    if m == 1:
        color = "red"
    if m == 2:
        color = "blue"

    edges_pairs.append((a, b))
    edges_pairs_by_id[edge_id] = (a, b)
    edges_labels_by_id[edge_id] = label

    edges.append({"id": edge_id,
                "from": a,
                "to": b,
                "label": label,
                "arrows": "to",
                "color": color,
                "length": length
                 })
    edge_id += 1

    return edge_id


def add_edge2(a, b, edge_id, id_counter, label="", color="black", length=100):
    """
    Add edges to the hierarchy network. If an edge between "a" and "b" already exist,
    check if such edge has the same label, if it does, no new edge is added,
    otherwise, if labels are different, duplicate node "a" and create a new edge
    between the duplicated node and "b"
    """

    m = edges_pairs.count((a, b))

    if m == 0: # if edge doesn't exist
        edge_id = add_edge(a, b, edge_id, label, color, length)

    else: # if edge already exist

        # check if edge label already exist or not

        # get id of existing edges:
        ids = [i for i,p in edges_pairs_by_id.items() if p==(a, b)]

        # get all labels of existing edges
        labels=[]
        for i in ids:
            labels.append(edges_labels_by_id[i])

        # if label already exist do nothing
        # else, duplicate node
        if label not in labels:

            node_label = nodes_labels[a]
            n = nodes_ns[a]
            group = nodes_groups[a]

            id_counter = add_node(id_counter, node_label, n, group, repeat_nodes=True)

            a2 = nodes_ids[node_label][-1]
            # a2 = id_counter-1 #(this is equivalent)

            edge_id = add_edge(a2, b, edge_id, label, color, length=200)

    return edge_id, id_counter

# CREATE JSON FILE FOR THE HIERARCHY NETWORK

nodes                   = []
edges                   = []

nodes_ids               = {}
nodes_labels            = {}
nodes_ns                = {}
nodes_groups            = {}
id_counter              = 0
edge_id                 = 0
edges_pairs             = []
edges_pairs_by_id       = {}
edges_labels_by_id      = {}


for i in range(len(threat_table)):

    # NODES
    label1              = threat_table.iloc[i]['Trust_Boundary_Description']

    if threat_table.iloc[i]['Trust_Boundary_ID'][0]=='T':
        group           = "TrustBoundary"
    elif threat_table.iloc[i]['Trust_Boundary_ID'][0]=='A':
        group           = "Asset"

    id_counter          = add_node(id_counter, label1, n=2, group=group)

    label2              = threat_table.iloc[i]['Threat_Actor_Description']
    id_counter          = add_node(id_counter, label2, n=2, group="ThreatActor")

    label3              = threat_table.iloc[i]['Vulnerability']
    id_counter          = add_node(id_counter, label3, group="Vulnerability")

    label4              = threat_table.iloc[i]['Risk']
    id_counter          = add_node(id_counter, label4, group="Risk")

    label5              = threat_table.iloc[i]['Security_Control_Description']
    id_counter          = add_node(id_counter, label5, n=2, group="SecurityControl")

    # EDGES
    label6              = wrap_by_word(threat_table.iloc[i]['Threat'], 2)
    label7              = "Skills: \n" + threat_table.iloc[i]['Skills']
    label8              = "\nRisk Possibility: \n" +  threat_table.iloc[i]['Risk_Possibility'] + "\nRisk Impact: \n" + threat_table.iloc[i]['Risk_Impact'] + "\nRisk Level: \n" + threat_table.iloc[i]['Risk_Level']

    edge_id, id_counter = add_edge2(nodes_ids[label1][0], nodes_ids[label2][0], edge_id, id_counter, label6, length=200)
    edge_id, id_counter = add_edge2(nodes_ids[label2][0], nodes_ids[label3][0], edge_id, id_counter, label7, length=200)
    edge_id, id_counter = add_edge2(nodes_ids[label3][0], nodes_ids[label4][0], edge_id, id_counter,)
    edge_id, id_counter = add_edge2(nodes_ids[label4][0], nodes_ids[label5][0], edge_id, id_counter, label8, length=300)


threat_table_1          = {"nodes": nodes, "edges": edges}

# save to JSON
with open('data/threat_table_1.json', 'w') as fp:
    json.dump(threat_table_1, fp)

# CREATE JSON FILE FOR THE NO HIERARCHY NETWORK

nodes                   = []
edges                   = []

nodes_ids               = {}
nodes_labels            = {}
nodes_ns                = {}
nodes_groups            = {}
id_counter              = 0
edge_id                 = 0
edges_pairs             = []
edges_pairs_by_id       = {}
edges_labels_by_id      = {}

BLUE                    = "#99CDFF"
YELLOW                  = "#FEEBA7"
PINK                    = "#FFBBB2"
PURPLE                  = "#DAADF0"
ORANGE                  = "#FCC603"
GREEN                   = "#C6E7B0"

SHAPE                   = "circle"
SHAPE2                  = "box"

x                       = -950
y                       = -950
step                    = 70

# REFERENCE NODES
id_counter              = add_node(id_counter, label="Trust Boundary", x=x, y=y, color=BLUE)
id_counter              = add_node(id_counter, label="Asset", x=x, y=y+step, color=YELLOW)
id_counter              = add_node(id_counter, label="Threat Actor", x=x, y=y+2*step, color=PINK)
id_counter              = add_node(id_counter, label="Vulnerability", x=x, y=y+3*step, color=PURPLE, shape=SHAPE2)
id_counter              = add_node(id_counter, label="Risk", x=x, y=y+4*step, color=ORANGE, shape=SHAPE2)
id_counter              = add_node(id_counter, label="Security Control", x=x, y=y+5*step, color=GREEN)


for i in range(len(threat_table)):

    # NODES
    label1              = threat_table.iloc[i]['Trust_Boundary_Description']

    if threat_table.iloc[i]['Trust_Boundary_ID'][0]=='T':
        group           = "TrustBoundary"
    elif threat_table.iloc[i]['Trust_Boundary_ID'][0]=='A':
        group           = "Asset"

    id_counter          = add_node(id_counter, label1, n=2, group=group)

    label2              = threat_table.iloc[i]['Threat_Actor_Description']
    id_counter          = add_node(id_counter, label2, n=2, group="ThreatActor")

    label3              = threat_table.iloc[i]['Vulnerability']
    id_counter          = add_node(id_counter, label3, group="Vulnerability")

    label4              = threat_table.iloc[i]['Risk']
    id_counter          = add_node(id_counter, label4, group="Risk")

    label5              = threat_table.iloc[i]['Security_Control_Description']
    id_counter          = add_node(id_counter, label5, n=2, group="SecurityControl")

    # EDGES
    label6              = wrap_by_word(threat_table.iloc[i]['Threat'], 2)
    label7              = "Skills: \n" + threat_table.iloc[i]['Skills']
    label8              = "\nRisk Possibility: \n" +  threat_table.iloc[i]['Risk_Possibility'] + "\nRisk Impact: \n" + threat_table.iloc[i]['Risk_Impact'] + "\nRisk Level: \n" + threat_table.iloc[i]['Risk_Level']

    edge_id             = add_edge(nodes_ids[label1][0], nodes_ids[label2][0], edge_id, label6, length=200)
    edge_id             = add_edge(nodes_ids[label2][0], nodes_ids[label3][0], edge_id, label7, length=200)
    edge_id             = add_edge(nodes_ids[label3][0], nodes_ids[label4][0], edge_id)
    edge_id             = add_edge(nodes_ids[label4][0], nodes_ids[label5][0], edge_id, label8, length=300)


threat_table_2          = {"nodes": nodes, "edges": edges}

# save to JSON
with open('data/threat_table_2.json', 'w') as fp:
    json.dump(threat_table_2, fp)
