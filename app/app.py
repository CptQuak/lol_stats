from shiny import App, render, ui, reactive
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shiny_download import get_url
plt.style.use('ggplot')

url = r'https://raw.githubusercontent.com/CptQuak/lol_stats/shiny-app/shinydata/lol.csv'
relevant_columns = ['playername', 'league', 'position', 'teamname', 'kills', 'deaths', 'assists', 'dpm', 'total cs']


##########################################################
app_ui = ui.page_fluid(    
    ui.panel_title('League of Legends 2023 season player statistics'),
#     ui.navset_tab_card(
#         elements ----
#         ui.nav("a", "tab a content"),
#         ui.nav("b", "tab b content"),
#     ),
#     ui.markdown('''
#         App showing statistics describing performance of professional League of Legends players
#     '''),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_numeric('num_players', 'Number of players', value=10),
            ui.input_selectize("position", "Select position", 
                dict(all='All positions', top="Toplane", jng='Jungle' ,mid="Midlane", bot='Ad carry', sup='Support'),
                selected='all',
            ),
            ui.input_selectize("var", "Select variable",
                dict(average_kills="average_kills", average_deaths="average_deaths", 
                     average_assists='average_assists', average_dpm='average_dpm', average_cs='average_cs'),
                selected='average_kills',
            ),
            ui.input_checkbox_group("tournaments", "Select torunaments (multiple)", 
                           dict(MSI='MSI', LCK='LCK', LPL='LPL', LEC='LEC'), 
                           selected='MSI'
            ),
            ui.input_selectize("tab_sorting", "Sort table by", 
                {x: x for x in ['total_kills', 'total_deaths', 'total_assists', 'highest_dpm', 'highest_cs']},
                selected='top',
            ),
        ), 
        ui.panel_main(
            ui.output_plot("plot"),
            ui.output_table('topstats')
        )
    )
)


def server(input, output, session):
    reactive_df = reactive.Value(pd.DataFrame())
    
    @reactive.Calc
    async def get_data():
        response = await get_url(url, 'string')
        data = StringIO(response.data)
        return data
    
    @reactive.Effect
    async def _():
        data = await get_data()
        reactive_df.set(pd.read_csv(data, header=0))
        print(reactive_df().head())

    @output
    @render.plot
    def plot():
        query_position = [input.position()] if input.position() != 'all' else ['top', 'jgl', 'mid', 'bot', 'sup']
        df = reactive_df()
        data = (
            df
            [(df['league'].isin(input.tournaments())) & (df['position'].isin(query_position))]
            .groupby(['playername'])
            .agg(
                average_kills = pd.NamedAgg('kills', 'mean'),
                average_deaths = pd.NamedAgg('deaths', 'mean'),
                average_assists = pd.NamedAgg('assists', 'mean'),
                average_dpm = pd.NamedAgg('dpm', 'mean'),
                average_cs = pd.NamedAgg('total cs', 'mean'),
            )
            .reset_index()
            .sort_values(input.var(), ascending=False)
            .head(input.num_players())
        )

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        # im = ax.imshow(data2d, cmap=input.cmap(), vmin=input.range()[0], vmax=input.range()[1])
        sns.barplot(data, x=input.var(), y='playername', color='#12b6f8', ax=ax)
        return fig

    @output
    @render.table
    def topstats():
        query_position = [input.position()] if input.position() != 'all' else ['top', 'jgl', 'mid', 'bot', 'sup']
        df = reactive_df()
        data = (
            df
            [(df['league'].isin(input.tournaments())) & (df['position'].isin(query_position))]
            .groupby(['playername'])
            .agg(
                total_kills = pd.NamedAgg('kills', 'sum'),
                total_deaths = pd.NamedAgg('deaths', 'sum'),
                total_assists = pd.NamedAgg('assists', 'sum'),
                highest_dpm = pd.NamedAgg('dpm', 'max'),
                highest_cs = pd.NamedAgg('total cs', 'max'),
            )
            .reset_index()
            .sort_values(input.tab_sorting(), ascending=False)
            .head(input.num_players())
        )
        return data

app = App(app_ui, server)
