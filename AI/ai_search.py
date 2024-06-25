# Importing the proper classes
from DeepTextSearch import LoadData,TextEmbedder,TextSearch

# Load data from CSV file
data = LoadData().from_csv("C:/Users/Владимир/Desktop/sample_100_rows.csv") # Нужно преобразовать pdf to csv

# For Serching we need to Embed Data first, After Embedding all the data stored on the local path
TextEmbedder().embed(corpus_list=data)

# for searching, you need to give the query_text  and the number of the similar text you want
TextSearch().find_similar(query_text="Which names start with the letter B?",top_n=10) #Запрос вводим свой
