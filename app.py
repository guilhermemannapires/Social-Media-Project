import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(layout="centered")

st.sidebar.title('Social Media Project')

st.sidebar.divider()

df_sentiment = pd.read_csv("Components/sentimentdataset.csv")
df_influencers = pd.read_csv("Components/influencers.csv")

# Converter todas as palavras para minúsculas e remover espaços em branco adicionais

df_sentiment['Platform'] = df_sentiment['Platform'].str.lower().str.strip()

# Fig1: Criar Word Cloud dos canais digitais mais usados pelo público

st.header('The Impact of Social Media Posts')

# Contagem das palavras (o 'word' são as plataformas, e 'count' a quantidade delas)
word_counts = df_sentiment["Platform"].value_counts().reset_index()
word_counts.columns = ['word', 'count']

fig1 = px.scatter(word_counts, x="word", y="count",
                  size="count", text="word", size_max=70)
fig1.update_traces(marker=dict(color='skyblue', line=dict(
    width=2, color='DarkSlateGrey')), textfont=dict(color='black'))
fig1.update_layout(xaxis_title="Platform",
                   yaxis_title="Frequency")

st.plotly_chart(fig1)

st.divider()

# Fig2: Criar gráfico Sentiment POSITIVO, NEGATIVO, NEUTRO

# Normalizar os nomes dos Sentiment
df_sentiment['Sentiment'] = df_sentiment['Sentiment'].str.lower(
).str.strip()

# Criar variáveis para Positivo, Negativo, Neutro
positive_sentiments = ["positive", "happy", "happiness", "joy", "love", "amusement",
                       "enjoyment", "admiration", "affection", "awe", "acceptance",
                       "adoration", "anticipation", "calmness", "excitement",
                       "kind", "pride", "elation", "euphoria", "contentment",
                       "serenity", "gratitude", "hope", "empowerment", "compassion",
                       "tenderness", "enthusiasm", "fulfillment", "reverence",
                       "zest", "hopeful", "proud", "grateful", "empathetic",
                       "compassionate", "playful", "free-spirited", "inspired",
                       "confident", "whimsy", "harmony", "creativity", "radiance",
                       "wonder", "rejuvenation", "adventure", "melodic", "festivejoy",
                       "innerjourney", "freedom", "dazzle", "artisticburst",
                       "culinaryodyssey", "resilience", "immersion", "spark",
                       "marvel", "overjoyed", "motivation", "joyfulreunion",
                       "mindfulness", "dreamchaser", "elegance", "colorful",
                       "hypnotic", "connection", "iconic", "journey",
                       "creative inspiration", "runway creativity",
                       "ocean's freedom", "whispers of the past", "winter magic",
                       "thrilling journey", "nature's beauty", "celestial wonder",
                       "charm", "heartwarming", "renewed effort", "breakthrough",
                       "joy in baking", "envisioning history", "vibrancy",
                       "mesmerizing", "culinary adventure"]

neutro_sentiments = ["neutral", "confusion", "surprise", "curiosity", "reflection", "suspense", "triumph", "exploration",
                     "accomplishment", "tranquility", "grandeur", "energy", "challenge", "solitude", "heartache", "melancholy", "nostalgia"]

negative_sentiments = ["negative", "anger", "fear", "sadness", "disgust", "bitter", "shame", "despair", "betrayal", "suffering", "emotionalstorm",
                       "isolation", "lostlove", "loneliness", "grief", "indifference", "disappointment", "numbness", "melancholy", "ambivalence", "miscalculation"]

# Dizer que valores de df_sentiment_positive, neutral, negative são os valores indicados, encontrados dentro de Sentiment.
df_sentiment_positive = df_sentiment[df_sentiment["Sentiment"].isin(
    positive_sentiments)]

df_sentiment_neutral = df_sentiment[df_sentiment["Sentiment"].isin(
    neutro_sentiments)]

df_sentiment_negative = df_sentiment[df_sentiment["Sentiment"].isin(
    negative_sentiments)]

# Criar uma nova coluna 'Sentiment_Type' para indicar o tipo de sentimento
df_sentiment_positive['Sentiment_Type'] = 'Positive'
df_sentiment_neutral['Sentiment_Type'] = 'Neutral'
df_sentiment_negative['Sentiment_Type'] = 'Negative'

# Calcular a contagem de ocorrências para cada tipo de sentimento
count_positive = df_sentiment_positive.shape[0]
count_neutral = df_sentiment_neutral.shape[0]
count_negative = df_sentiment_negative.shape[0]

# Criar um DataFrame com os dados de contagem
df_counts = pd.DataFrame({
    'Sentiment_Type': ['Positive', 'Neutral', 'Negative'],
    'count': [count_positive, count_neutral, count_negative]
})

# Criar o gráfico

st.header('Sentiment Level')

fig2 = px.bar(df_counts, x='Sentiment_Type', y='count', color='Sentiment_Type',
              color_discrete_map={'Positive': 'green', 'Neutral': 'grey', 'Negative': 'red'})
st.plotly_chart(fig2)

st.divider()

# Criar tabela com o Text e Sentiment

st.header('Media Social x Sentiment x Country')

platform_multiselect = df_sentiment["Platform"].unique()
descriçao_platform = st.multiselect(
    "Select the Digital Platform:", platform_multiselect)

multiselect_filtro = df_sentiment[df_sentiment["Platform"].isin(
    descriçao_platform)]

# Normalizar os nomes dos países
multiselect_filtro['Country'] = multiselect_filtro['Country'].str.lower(
).str.strip()

st.text('Information')

st.write(multiselect_filtro[[
         "Text", "Sentiment", "Platform"]], width=800, height=1000)


# Fig3: Criar gráfico Quantidade de publicação X Country

st.text('Publication x Country')

fig3 = px.bar(multiselect_filtro["Country"].value_counts())
fig3

# Fig4: Criar gráfico com visão TOTAL Quantidade de publicação X Country agrupado por Platform

st.text("Comprehensive View of the Impact of Social Media Posts by Country")

# Normalizar os nomes dos países
df_sentiment['Country'] = df_sentiment['Country'].str.lower().str.strip()

# Calcular a contagem total de publicações por país, agrupado por plataforma
count_by_country_platform = df_sentiment.groupby(
    ['Country', 'Platform']).size().reset_index(name='count')

# Criar o gráfico de barras
fig4 = px.bar(count_by_country_platform, x='Country',
              y='count', color='Platform')

# Adicionar títulos aos eixos
fig4.update_layout(xaxis_title='Country', yaxis_title='Número de Publicações')

st.plotly_chart(fig4)

st.divider()

# Sugestão de Influencers

st.header('TikTok Influencers Recommendation')

# Trocar valores da coluna Views.avg (Multiplicar por 1000000 valores que têm M, multiplicar por 1000 valores que têm K)


def convert_views_avg(value):
    if 'M' in value:
        return float(value.replace('M', '')) * 1000000
    elif 'K' in value:
        return float(value.replace('K', '')) * 1000
    else:
        return float(value)


df_influencers['Views avg.'] = df_influencers['Views avg.'].apply(
    convert_views_avg)

# Trocar valores da coluna Subscribers (Multiplicar por 1000000 valores que têm M, multiplicar por 1000 valores que têm K)


def convert_subscribers(value):
    if 'M' in value:
        return float(value.replace('M', '')) * 1000000
    elif 'K' in value:
        return float(value.replace('K', '')) * 1000
    else:
        return float(value)


df_influencers['Subscribers'] = df_influencers['Subscribers'].apply(
    convert_subscribers)

# Top 10 maiores Influencers (Views avg)
# Usamos o .nlargest pra citar o top 10 maiores Views avg. mas sem retirar nenhuma coluna
st.text('Top 10 Biggest TikTokers by Average Views')
top10_maiores_views_avg = df_influencers.nlargest(10, 'Views avg.')

fig5 = px.bar(top10_maiores_views_avg, x='Tiktoker name', y='Views avg.')
fig5

# Top 10 maiores Influencers (Subs)
st.text('Top 10 Biggest TikTokers by Subscribers')
top10_maiores_subs = df_influencers.nlargest(10, 'Subscribers')

fig6 = px.bar(top10_maiores_subs, x='Tiktoker name', y='Subscribers')
fig6

# Top 10 médios Influencers (Views avg)
# Criamos o df_filtered e df_filtered_subs para definirmos que queremos Views avg. e Subscribers >= 1000000 e <= 6000000
st.text('Top 10 Medium-sized TikTokers by Average Views (1M to 6M)')
df_filtered = df_influencers[(df_influencers['Views avg.'] >= 1000000) & (
    df_influencers['Views avg.'] <= 6000000)]
top10_medios_views_avg = df_filtered.nlargest(10, 'Views avg.')

fig7 = px.bar(top10_medios_views_avg, x='Tiktoker name', y='Views avg.')
fig7

# Top 10 médios Influencers (Subs)
st.text('Top 10 Medium-sized TikTokers by Subscribers (1M to 6M)')
df_filtered_subs = df_influencers[(df_influencers['Subscribers'] >= 1000000) & (
    df_influencers['Subscribers'] <= 6000000)]
top10_medios_subs = df_filtered_subs.nlargest(10, 'Subscribers')

fig8 = px.bar(top10_medios_subs, x='Tiktoker name', y='Subscribers')
fig8

# Top 10 pequenos Influencers (Views avg)
# Criamos o df_filtered_min_views e df_filtered_min_subs para definirmos que queremos Views avg. e Subscribers > 0 e <= 500000
st.text('Top 10 Small-sized TikTokers by Average Views (100k to 800K)')
df_filtered_min_views = df_influencers[(df_influencers['Views avg.'] >= 100000) & (
    df_influencers['Views avg.'] <= 800000)]
top10_small_views_avg = df_filtered_min_views.nlargest(10, 'Views avg.')

fig9 = px.bar(top10_small_views_avg, x='Tiktoker name', y='Views avg.')
fig9

# Top 10 pequenos Influencers (Subs)
st.text('Top 10 Small-sized TikTokers by Subscribers (100k to 800K)')
df_filtered_min_subs = df_influencers[(df_influencers['Subscribers'] >= 100000) & (
    df_influencers['Subscribers'] <= 800000)]
top10_small_subs = df_filtered_min_subs.nlargest(10, 'Subscribers')

fig10 = px.bar(top10_small_subs, x='Tiktoker name', y='Subscribers')
fig10
