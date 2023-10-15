This google colab notebook generates embeddings of all the texts scraped from the GVSU ACI webpages.

First, I use the sentence-transformers to generate embeddings and find that there are 927 rows and 384 columns (features).

Then, I use the declare-lab/flan-alpaca-large model to generate embeddings because we will be use alpaca model to be at the backend of the AI system.

Using alpaca, there were 927 rows and 1024 columns (features).

When the user asks the question, these embeddings will be used to find the similarity between the question's embedding and these alpaca embeddings and the answer will be extracted based on that similarity with the generated embeddings.