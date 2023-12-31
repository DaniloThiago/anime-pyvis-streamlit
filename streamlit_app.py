import random
import pandas as pd
from pyvis import network as net
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
got_net = net.Network(
    notebook=True,
    cdn_resources="remote",
    bgcolor="#222222",
    font_color="white",
    height="750px",
    width="100%",
    filter_menu=True,
)

got_net.barnes_hut()
got_data = pd.read_csv("./Anime.csv")
filtered_data = got_data.query('Release_year >= 2022.0')
filtered_data = filtered_data.loc[:, ['Name', 'Voice_actors']]
filtered_data = filtered_data.dropna(subset=['Voice_actors'])
filtered_data['Voice_actors'] = filtered_data['Voice_actors'].str.split('\n').str[0]
filtered_data = filtered_data[filtered_data['Voice_actors'].str.contains(':')]

obras_atores = {}
node_attributes = {}  # Dicionário auxiliar para armazenar os atributos dos nós

unique_obras = filtered_data['Name'].unique()
num_obras = len(unique_obras)
colors = ['#' + '%06x' % random.randint(0, 0xFFFFFF) for _ in range(num_obras)]  # Gera uma lista de cores aleatórias

obras_colors = dict(zip(unique_obras, colors))  # Mapeia cada obra com uma cor aleatória

for index, row in filtered_data.iterrows():
  name = row['Name']
  actors = row['Voice_actors'].split(',')

  for actor in actors:
    a = actor.split(':')
    if len(a) > 1:
      actor_name = a[1].strip()
      if actor_name not in node_attributes:
        got_net.add_node(actor_name)
        node_attributes[actor_name] = {'name': actor_name}  # Armazenar atributo name do nó

      if name in obras_atores:
        obras_atores[name].append(actor_name)
      else:
        obras_atores[name] = [actor_name]

for obra, atores in obras_atores.items():
  for i in range(len(atores)):
    for j in range(i+1, len(atores)):
      ator1 = atores[i]
      ator2 = atores[j]

      if ator1 != ator2:
        color = obras_colors[obra]  # Obtém a cor aleatória correspondente à obra
        got_net.add_edge(ator1, ator2, title=obra, label=obra, color=color)  # Adicionar rótulo e cor para cada aresta


# Obter a lista de nós
node_list = sorted(node_attributes.keys())

# Menu suspenso para seleção do nó
selected_node = st.sidebar.selectbox('Selecione um nó', node_list)

# Exibir o nome do nó selecionado
st.write("Nome do nó selecionado:", selected_node)

# Marcar o nó selecionado no gráfico
for node_name in got_net.nodes:
  if node_name["id"] == selected_node:
    node_name['color'] = 'red'  # Definir a cor do nó destacado como 'red'

# Exibir o gráfico de rede
got_net.show("animes.html")

with open("animes.html", 'r', encoding='utf-8') as HtmlFile: source_code = HtmlFile.read()
components.html(source_code, height=1200, scrolling=True)