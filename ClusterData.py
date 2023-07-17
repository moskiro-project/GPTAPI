import openai
import pandas as pd
import time
import json
openai.api_key = "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"

system_context = """Kategorien:
1. Produktion und Fertigung
2. Kundendienst und Wartung
3. Maschinen- und Anlagenführung
4. Hilfsarbeiten in der Produktion
5. Metallverarbeitung und Zerspanungstechnik
6. Instandhaltung und Reparatur
7. Mechatronik und Automatisierungstechnik
8. Maschinenbedienung und Bedienungstechnik
9. Hausmeister und Gebäudemanagement
10. Konstruktion und Design
11. Elektrotechnik und -installation
12. Forschung und Entwicklung
13. Montage und Installation
14. Bau- und Bauleitung
15. Elektrik und Haustechnik
16. Logistik und Lagerwirtschaft
17. Projektmanagement und -koordination
18. Einkauf und Beschaffung
19. Vertrieb und Verkauf
20. Maschinensteuerung und Bearbeitung
21. Rohstoffverarbeitung und -bearbeitung
22. Montagearbeiten und Montagevorbereitung
23. Technischer Vertrieb und Kundenbetreuung
24. Ingenieurwesen und technische Entwicklung
25. Schlosserei und Metallbau
26. Bau- und Baustellenhilfe
27. Schweißerei und Metallverbindungstechnik
28. Lager- und Staplerarbeit
29. IT und Softwareentwicklung
30. Holzverarbeitung und Möbelbau
31. Projektmanagement und -koordination
32. Elektrotechnik und -installation
33. Handwerk und handwerkliche Tätigkeiten
34. IT Systembetreuung und Netzwerktechnik
35. Softwareentwicklung und Programmierung
36. Lager und Logistik
37. Metallverarbeitung und -konstruktion
38. Bauingenieurwesen und -planung
39. Teamleitung und Teamkoordination
40. Schichtleitung und Schichtarbeit
41. Mechanik und Maschinenbau
42. Kundendienst und Serviceeinsatz
43. Datenverarbeitung und Datenmanagement
44. Werkzeugherstellung und -bearbeitung
45. Technisches Produktdesign und -entwicklung
46. Anwendungsingenieurwesen und -entwicklung
47. Projektmanagement und -koordination
48. Lagerverwaltung und -organisation
49. Vertriebs- und Verkaufsinnendienst
50. Qualitätskontrolle und -sicherung
51. Sonstige"""


#excel_file = "./Data/FullDataset_fromNER_v1.xlsx"
#data = pd.read_excel(excel_file)
#data = data.values.tolist()
#outputJobTitle = []
#output = []

with open('./Data/tmp.txt', 'r') as file:
    content = file.read().replace('\n', '')

entries = eval(content)
#df = pd.DataFrame(columns = ["Job", "Cluster Index"])

output = []

print(len(entries))
#print(entries)

j = 0
for i in entries:
    j = j+1
    content = "Gib nur als Zahl ohne Text den Index der passendsten Kategorie für den folgenden Jobtitel aus: " + str(i)
    try:
        responseTitle = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user","content": content }
          ],
        temperature = 1.0
        )
        ClusteredResponse = responseTitle["choices"][0]["message"]["content"]
        output.append([i, ClusteredResponse])
        
        print(j)
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
    except openai.error.RateLimitError as e:
        print(f"OpenAI API returned an API Error: {e}")
        continue


df = pd.DataFrame(output, columns=["NewJobTitle", "Cluster"])

with pd.ExcelWriter("./Data/TitleClusters.xlsx") as writer:
    df.to_excel(writer)

#ith open('./Data/clusterOutput.txt', 'w') as f:
 #   f.write(result)