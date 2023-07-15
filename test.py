import openai
import pandas as pd
import time
import csv
openai.api_key = "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"

excel_file = "./Data/2023_07_10_Datensatz_unbereinigt_LN_v3.xlsx"
data = pd.read_excel(excel_file)
data = data.values.tolist()
outputJobTitle = []
outputJobSkills = []
output = []

#Generierung: Erste Anfrage
for i in range(25,26):
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

    content1 = ("Identifiziere Skills in der Jobbeschreibung. Beschreibe die gefunden Skills mit 1-3 Schlagwörtern die genau in dieser Konstellation in dem Text zu finden sind und trenne sie mit Kommata. Ignoriere Vorteile im Unternehmen wie Urlaub oder Arbeitszeiten. Nutze dafür die folgende Jobbeschreibung:")
    content1 = content1 + data [i][2]
    responseSkill = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Du beantwortest Anfragen nur mit dem exakt gleichen Wortlaut wie sie in der Anfrage stehen. Aufzählungen mit Bindestrich dürfen nicht ausgeschrieben werden. Die Antwort soll ohne Einleitung und Überschrift erfolgen. Ignoriere Vorteile im Unternehmen wie Urlaub oder Arbeitszeiten."},
        {"role": "user", "content": content1}
      ],
      temperature = 0.7
    )

    JobSkillResponse = responseSkill["choices"][0]["message"]["content"] # type: ignore
    output.append((JobTitleResponse,data[i][2],JobSkillResponse))
    time.sleep(1)  
    


print(output[0][2],output[0][0])

with open("example.csv","w", newline="", encoding="utf-8-sig" ) as file:
    writer = csv.writer(file, delimiter=";")

    writer.writerow(["Jobtitle", "Decribtion", "Jobskill"])
    for item in output:
        writer.writerow(item)