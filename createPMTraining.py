import openai
import pandas as pd
import time
import json
openai.api_key = "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"

excel_file = "./Data/2023_07_10_Datensatz_unbereinigt_LN_v3.xlsx"
data = pd.read_excel(excel_file)
data = data.values.tolist()
outputJobTitle = []
output = []
j = 0

#Generierung: Erste Anfrage
for i in data:
    try:
        content = ("Bereinige den folgenden Jobtitel von allen unnötigen Informationen:")
        content = content + i[1]
        responseTitle = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "Antworte lediglich mit einer Job Titel. Mit unnötigen informationen sind solche gemeint wie (m/w/d), Arbeitszeiten, die Stadt, Ort der Niederlassungen und weiterführende Informationen nach -"},
            {"role": "user","content": content }
          ],
          temperature = 0.5
        )

        JobTitleResponse = responseTitle["choices"][0]["message"]["content"] # type: ignore
        time.sleep(1)

    except openai.error.Timeout as e: # type: ignore
      #Handle timeout error
      print(f"OpenAI API request timed out: {e}")
      continue
    except openai.error.APIError as e: # type: ignore
      #Handle API error
      print(f"OpenAI API returned an API Error: {e}")
      continue
    except openai.error.APIConnectionError as e: # type: ignore
      #Handle connection error
      print(f"OpenAI API request failed to connect: {e}")
      continue
    except openai.error.ServiceUnavailableError as e: # type: ignore
       #Handle connection error
       print(f"OpenAI API request failed to connect: {e}")
       continue

    output.append((i[1],JobTitleResponse,i[2]))
    

df = pd.DataFrame(output, columns=["JobTitle", "NewJobTitle","Description"])

with pd.ExcelWriter("PMTraining.xlsx") as writer:
    df.to_excel(writer)
