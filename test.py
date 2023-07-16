import openai
import pandas as pd
import time
import json
openai.api_key = "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"

excel_file = "./Data/2023_07_10_Datensatz_unbereinigt_LN_v3.xlsx"
data = pd.read_excel(excel_file)
data = data.values.tolist()
outputJobTitle = []
outputJobSkills = []
output = []

#Generierung: Erste Anfrage
for i in range(99):
    try:
        content = ("Bereinige den folgenden Jobtitel von allen unnötigen Informationen:")
        content = content + data [i][1]
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

        content1 = ("Identifiziere Skills in der Jobbeschreibung. Beschreibe die gefunden Skills mit 1-3 Schlagwörtern die genau in dieser Konstellation in dem Text zu finden sind, trenne sie mit Kommata und verwende keine Überschriften oder Einleitungsn. Ignoriere Vorteile im Unternehmen wie Urlaub oder Arbeitszeiten. Analysiere die folgende Jobbeschreibung:")
        #content1 = ("Verhalte dich als wärst du ein NER das Skills aus Texten erkennt. Erkenne alle angegebenen Skills in dem folgenden Text und gebe die Wörter in Form einer Liste wieder die durch Kommata getrennt wird. Wörter die das Arbeitsumfeld oder Arbeitsbedingungen betreffen sollen nicht ausgegeben werden: ")
        content1 = content1 + data [i][2]
        responseSkill = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "Du beantwortest Anfragen nur mit dem exakt gleichen Wortlaut wie sie in der Jobbeschreibung stehen. Aufzählungen mit Bindestrich dürfen nicht ausgeschrieben werden. Ignoriere Vorteile im Unternehmen wie Urlaub oder Arbeitszeiten."},
            #{"role": "system", "content": "Arbeitsbedinungen und das Arbeitsumfeld sind keine Fähigkeiten die vom NER erfasst werden"},
            {"role": "user", "content": content1}
          ],
          temperature = 0.5
        )

        JobSkillResponse = responseSkill["choices"][0]["message"]["content"] # type: ignore
        output.append((JobTitleResponse,data[i][2],JobSkillResponse))
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

    print(i, "\n") 
    

df = pd.DataFrame(output, columns=["Jobtitle","Description","Jobskills"])

with pd.ExcelWriter("example.xlsx") as writer:
    df.to_excel(writer)

