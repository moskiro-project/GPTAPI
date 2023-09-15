import openai
import pandas as pd
import time
import json
openai.api_key = "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"

excel_file = "./ReducedDataset300Entries.xlsx"
data = pd.read_excel(excel_file)
data = data.values.tolist()

outputJobTitle = []
outputJobSkills = []
output = []

#Generierung: Erste Anfrage
for i in data:
    try:
        content1 = ("Identifiziere Skills in der Jobbeschreibung. Beschreibe die gefunden Skills mit 1-3 Schlagwörtern die genau in dieser Konstellation in dem Text zu finden sind, trenne sie mit Kommata und verwende keine Überschriften oder Einleitungsn. Ignoriere Vorteile im Unternehmen wie Urlaub oder Arbeitszeiten. Analysiere die folgende Jobbeschreibung:")
        #Generierung der Anfrage
        content1 = content1 + i[2]
        responseSkill = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "Du beantwortest Anfragen nur mit dem exakt gleichen Wortlaut wie sie in der Jobbeschreibung stehen. Aufzählungen mit Bindestrich dürfen nicht ausgeschrieben werden. Ignoriere Vorteile im Unternehmen wie Urlaub oder Arbeitszeiten."},
            #Mehr Informationen an das System um den Output so praktikabel wie möglich zu gestalten,
            {"role": "user", "content": content1}
          ],
          temperature = 0.5
        )

        JobSkillResponse = responseSkill["choices"][0]["message"]["content"] # type: ignore
        output.append((i[1],i[2],JobSkillResponse))
        time.sleep(1)
        #Warten um die API nicht zu überlasten - begrenzte Anzahl an Anfragen pro Minute
        
#Errorhandling
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

    print(i, "\n") 
    
#Umwandeln der Liste in Dataframe
df = pd.DataFrame(output, columns=["Jobtitle","Description","Jobskills"])

with pd.ExcelWriter("output.xlsx") as writer:
    #Abspeichern des Dataframes in Datei
    df.to_excel(writer)

