import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Charger la base de données
data = pd.read_excel(r"C:\Users\DELL\Desktop\Pratique des enquêtes\données.xlsx")

# Vérifier les noms de colonnes
print("Noms des colonnes :", data.columns)

# Renommer les colonnes si nécessaire
data.rename(columns=lambda x: x.strip(), inplace=True)

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Options pour le filtre
filters = [
    {'label': 'ISE Économie', 'value': 'ISE Économie'},
    {'label': 'ISE Mathématique', 'value': 'ISE Mathématique'},
    {'label': 'Les deux classes', 'value': 'Les deux classes'}
]

# Mise en page de l'application
app.layout = html.Div([
    # Ajouter une image en haut
    html.Div([
        html.Img(src='/assets/Capture d\'écran 2024-11-17 120050.png', 
         style={'width': '100%', 'height': '200px'})

    ]),
    # Titre du tableau de bord
    html.H1(
        "Profil des ISE 1 2024-2025",
        style={
            'textAlign': 'center',
            'color': '#003366',
            'fontWeight': 'bold',
            'textDecoration': 'underline',
            'fontFamily': 'Arial'
        }
    ),
    # Menu déroulant pour les filtres
    html.Div([
        html.Label("Choisissez une classe :"),
        dcc.Dropdown(
            id='class-filter',
            options=filters,
            value='ISE Économie',
            placeholder='Sélectionnez une classe'
        )
    ], style={'margin': '20px', 'textAlign': 'center'}),

    # Affichage de l'effectif
    html.Div(id='effectif-container', style={'textAlign': 'center', 'margin': '20px'}),

    # Graphiques
    html.Div(id='graphs-container', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),

    # Section crédits
    html.Div([
        html.H2("Travail réalisé par :", style={'textAlign': 'center'}),
        html.Div([
            html.P("KINDO P. Nathan", style={'textAlign': 'center'}),
            html.P("ATISSO Deborah", style={'textAlign': 'center'}),
            html.P("SINGIBE Hinsalbé", style={'textAlign': 'center'}),
            html.P("MANGA Wilfried", style={'textAlign': 'center'}),
            html.P("PAMNA Alfred", style={'textAlign': 'center'}),
            html.P("DEDE Wilfried", style={'textAlign': 'center'}),
        ]),
        html.P(
            "Classe : AS 2 B",
            style={'textAlign': 'center', 'fontSize': '14px', 'fontStyle': 'italic', 'marginTop': '5px'}
        ),
        html.P("Merci pour votre attention !", style={'textAlign': 'center', 'marginTop': '20px', 'fontStyle': 'italic'})
    ], style={'marginTop': '50px', 'padding': '20px', 'backgroundColor': '#f0f0f0'})
])

# Callback pour filtrer les données, afficher l'effectif et générer les graphiques
@app.callback(
    [Output('effectif-container', 'children'),
     Output('graphs-container', 'children')],
    Input('class-filter', 'value')
)
def update_dashboard(selected_class):
    # Filtrer les données
    if selected_class == 'Les deux classes':
        filtered_data = data
    else:
        try:
            filtered_data = data[data["Classe"] == selected_class]
        except KeyError:
            return "Erreur : Colonne 'Classe' introuvable dans les données.", []

    # Calcul de l'effectif
    effectif = len(filtered_data)

    # Texte de l'effectif
    effectif_text = html.H3(
        f"Effectif : {effectif}",
        style={'fontWeight': 'bold', 'textAlign': 'center', 'color': '#333'}
    )

    # Graphique 1 : Répartition par sexe
    fig_sexe = px.pie(
        filtered_data,
        names='Sexe',
        title='Répartition par Sexe',
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    # Graphique 2 : Répartition par tranche d'âge en pourcentage
    filtered_data['Tranche âge'] = pd.cut(filtered_data['Âge (en années révolues / dernier anniversaire)'],
                                          bins=5, labels=['15-20', '20-25', '25-30', '30-35', '35-40'])
    age_counts = filtered_data['Tranche âge'].value_counts(normalize=True) * 100
    fig_age = px.bar(
        x=age_counts.index.astype(str),
        y=age_counts.values,
        title='Répartition par Tranches d\'Âge (%)',
        labels={'x': 'Tranches d\'âge', 'y': 'Pourcentage'},
        color_discrete_sequence=['#636EFA']
    )

    # Graphique 3 : Répartition par nationalité en pourcentage
    nationalite_counts = filtered_data['Nationalité'].value_counts(normalize=True) * 100
    fig_nationalite = px.bar(
        x=nationalite_counts.index,
        y=nationalite_counts.values,
        title='Répartition par Nationalité (%)',
        labels={'x': 'Nationalité', 'y': 'Pourcentage'},
        color_discrete_sequence=['#00CC96']
    )

    # Graphique 4 : Répartition par niveau de formation en pourcentage
    formation_counts = filtered_data['Niveau de formation antérieure'].value_counts(normalize=True) * 100
    fig_instruction = px.bar(
        x=formation_counts.index,
        y=formation_counts.values,
        title='Répartition par Niveau de Formation (%)',
        labels={'x': 'Niveau de formation', 'y': 'Pourcentage'},
        color_discrete_sequence=['#EF553B']
    )

    # Graphique 5 : Proportion ayant suivi un cours de préparation
    fig_preparation = px.pie(
        filtered_data,
        names='Avez-vous fréquenté une structure de préparation avant de passer le concours ?',
        title='Proportion des Étudiants Ayant Suivi un Cours de Préparation',
        color_discrete_sequence=px.colors.sequential.Purp
    )

    # Disposition des graphiques
    graphs = [
        html.Div(dcc.Graph(figure=fig_sexe), style={'width': '45%', 'padding': '10px'}),
        html.Div(dcc.Graph(figure=fig_age), style={'width': '45%', 'padding': '10px'}),
        html.Div(dcc.Graph(figure=fig_nationalite), style={'width': '45%', 'padding': '10px'}),
        html.Div(dcc.Graph(figure=fig_instruction), style={'width': '45%', 'padding': '10px'}),
        html.Div(dcc.Graph(figure=fig_preparation), style={'width': '45%', 'padding': '10px'})
    ]
    return effectif_text, graphs

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
