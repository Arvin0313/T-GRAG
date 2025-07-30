"""
Reference:
 - Prompts are from [graphrag](https://github.com/microsoft/graphrag)
"""

GRAPH_FIELD_SEP = "<SEP>"
PROMPTS = {}
PROMPTS["new create temporal QA"]='''
You are an artificial intelligence assistant, and I now need you to help me generate one time-series question-answer pairs.
I will provide you with the key points and corresponding original texts of two similar events from two annual reports.

The following are the requirements for the problem:
1. The difficulty of the problem should be simple and moderate, and not abstract or complex. The question needs to be an inquiry about specific entities, numbers, or time, not about abstract concepts (such as what the company's strategy is, what the company's plans are in the electric vehicle field, etc.)
2. The problem is targeted at the specific differences in attributes of similar events between {year1} and {year2} in two annual reports. (For example, the sales volume of a certain brand varies in different years, etc.)
3. The question must be answered correctly based on these two annual reports.
4. The problem must contain two timestamps, {year1} and {year2}.
5. The problem cannot contain multiple sub problems, and the problem should be clear and specific.
6. The information in the question should be sufficient and clear, avoiding ambiguous answers.
7. The answer should be concise and clear, avoiding being lengthy or repetitive.
If you are unable to build a question-answer pair that meets the above requirements, output 'Unable to build a suitable question-answer pair'
If you can build, follow the output format below

---output format---
If you are unable to build a question-answer pair that meets the above requirements, output 'Unable to build a suitable question-answer pair'
If you can build, follow the output format below
The response should be JSON formatted as follows:

{{"question":<question>,"answer":<answer>,"original text from {year1} report":<original text from {year1} report>,"original text from {year2} report":<original text from {year2} report>}}

The beginning and end of the output must be {{}}
The beginning and end of the output must be {{}}
The beginning and end of the output must be {{}}
!!!The output is only in JSON format,Don't output here is the output Or similarly, directly output the json!!!
!!!The output is only in JSON format,Don't output here is the output Or similarly, directly output the json!!!

---example---
###input###
Events in the 2023 Annual Report: "Audi Group's 2023 deliveries reached 1.9 million cars, with 178,000 being electric vehicles, a 51.0% increase in fully electric models from the previous year."
Corresponding original text: "Here is the summary of the provided Audi 2023 Annual Report text, adhering to the specified requirements:\n\nThe Audi Group, headquartered in Ingolstadt, Germany, encompasses the Audi, Lamborghini, and Ducati brands, among others. In 2023, Ducati celebrated various product milestones, including the Panigale V4, Multistrada V4 RS, DesertX Rally, and Diavel for Bentley. \n\nFinancially, the Brand Group Progressive reported significant figures for 2023. Deliveries reached 1.9 million cars, with 178,000 of those being electric vehicles, marking a 51.0% increase in fully electric models. The operating profit was EUR 6.3 billion, reflecting a -16.8% decline primarily due to negative effects of commodity hedging. The research and development ratio increased by 0.5 percentage points to 7.8%. Revenue totaled EUR 69.9 billion, a 13.1% increase mainly attributed to higher car sales. Net cash flow stood at EUR 4.7 billion, and the return on investment (ROI) was 17.7%, albeit 4.5 percentage points lower than the previous year.\n\nFor the outlook in fiscal year 2024, the Audi Group anticipates deliveries between 1.7 and 1.9 million cars, revenue between EUR 63 and 68 billion, an operating return on sales (ROS) of 8 to 10%, and a net cash flow of EUR 2.5 to 3.5 billion.\n\nThe global economic environment in 2023 was characterized by positive growth, with weaker growth in advanced economies and higher growth in emerging markets. Worldwide demand for vehicles was noticeably above the prior-year level, with growth in almost all regions. Europe experienced a low positive growth rate, with Eastern Europe performing stronger than Western Europe. China saw moderate growth, positively affected by the termination of its zero-COVID strategy. The USA reported robust economic growth, still-high but declining inflation, and a continuation of restrictive monetary policy.\n\nProduction-wise, the Brand Group Progressive manufactured 1,960,597 vehicles in 2023, a 14.1% increase from the previous year. Audi built 1,937,342 vehicles, with 669,902 produced locally by Chinese associated companies. Lamborghini produced 10,014 supercars and super SUVs, while Bentley produced 13,241 vehicles, representing a decline. Ducati's motorcycle production decreased by 21.4% to 55,226 units. The share of fully electric vehicles in total car production reached 10.0%, with significant increases in the Audi Q4 e-tron and Audi Q8 e-tron models. Production at global sites, including Germany, Europe, and specifically at Ingolstadt, Neckarsulm, Zwickau, and Bratislava, showed substantial increases compared to the previous year."

Events in the 2022 Annual Report: "In 2022, the Audi Group delivered approximately 1.6 million vehicles, including 118,000 electric vehicles, representing a 3.0% decrease in overall deliveries but a 44.3% increase in fully electric models."
Corresponding original text: "The Audi Group, comprising the Audi, Bentley, Lamborghini, and Ducati brands, navigated multiple crises in 2022, including the Russia-Ukraine war, fragile supply chains, semiconductor shortages, lockdowns in China, energy shortages, high energy prices, inflation, and recession fears. Despite these challenges, the group achieved notable financial highlights.\n\nIn 2022, the Premium brand group delivered approximately 1.6 million vehicles, including 118,000 electric vehicles, with a slight 3.0% decrease in overall deliveries due to logistics and supply chain challenges. However, fully electric models experienced strong growth, increasing by 44.3%. Notable electric models delivered included the Audi e-tron GT quattro and Audi RS e-tron GT from Audi Sport GmbH.\n\nFinancially, the Audi Group reported a 16.4% increase in revenue to EUR 61.8 billion, with 13.5% of revenue being EU taxonomy-aligned. The group achieved a record operating profit of EUR 7.6 billion, resulting in a 12.2% operating return on sales (ROS) and 22.2% return on investment (ROI). Net cash flow remained strong at EUR 4.8 billion, primarily due to robust price enforcement and the first-time consolidation of Bentley.\n\nThe company's materiality matrix, based on the Stakeholder Engagement Standard AccountAbility 1000 (AA1000SES), evaluates 16 key topics by stakeholders and ecological and societal impacts. Audi engages in regular dialogue events and conferences with stakeholders to discuss its strategy for sustainable premium mobility, incorporating feedback to improve Environmental, Social, and Governance (ESG) performance.\n\nFor the 2023 fiscal year, the Audi Group expects deliveries to range between 1.8 and 1.9 million cars, with revenue anticipated between EUR 69 and 72 billion. The projected ROS is between 9% and 11%, while ROI is expected to range between 19% and 22%. Net cash flow is forecasted to remain high, between EUR 4.5 and 5.5 billion. Research and development (R&D) and capital expenditure (CAPEX) ratios are expected to fall within strategic target corridors of 6-7% and 4-5%, respectively.\n\nThe Audi Group's crisis management efforts, established in 2020, played a crucial role in mitigating the impacts of the various challenges faced in 2022. Collaborations with suppliers, semiconductor manufacturers, and chip brokers, as well as production adaptations and technical alternative developments, helped minimize the effects of supply chain disruptions. Close communication with customers also enabled the Audi brand to offer alternative solutions, despite partially limiting model and option offerings."
###output###
{{
  "question":"What are Audi's electric vehicle deliveries in 2022 and 2023 respectively?",
  "answer": "In 2022, Audi delivered 118000 electric vehicles. In 2023, Audi's electric vehicle delivery reached 178000 units.",
  "original text from 2022 report": "In 2022, the Audi Group delivered approximately 1.6 million vehicles, including 118,000 electric vehicles, with a slight 3.0% decrease in overall deliveries due to logistics and supply chain challenges. However, fully electric models experienced strong growth, increasing by 44.3%.",
  "original text from 2023 report": "In 2023, deliveries reached 1.9 million cars, with 178,000 of those being electric vehicles, marking a 51.0% increase in fully electric models."
}}

---real data---
###input###
Events in the {year1} Annual Report:{keypoint1}
Corresponding original text: {text1}

Events in the {year2} Annual Report:{keypoint2}
Corresponding original text: {text2}
###output###
The beginning and end of the output must be {{}}
'''
PROMPTS['Evaluation QA']='''
You are a helpful evaluator
---Task Overview---
You are tasked with evaluating user answers based on a given question, reference answer, and additional reference text. Your goal is to assess the correctness of the user answer using a specific metric.

---Evaluation Criteria---
1. Yes/No Questions: Verify if the user's answer aligns with the reference answer in terms of a "yes" or "no" response.
2. Short Answers/Directives: Ensure key details such as numbers, specific nouns/verbs, and dates match those in the reference answer.
3. Abstractive/Long Answers: The user's answer can differ in wording but must convey the same meaning and contain the same key information as the reference answer to be considered correct.

--- Evaluation Process---
1. Identify the type of question presented.
2. Apply the relevant criteria from the Evaluation Criteria.
3. Compare the user's answer against the reference answer accordingly.
4. Consult the reference text for clarification when needed.
5. Score the answer with a binary label 0 or 1, where 0 denotes wrong and 1 denotes correct.
NOTEthat if the user answer is 0 or an empty string, it should get a 0 score.

---Real Data---
Question: {question}
User Answer: {sys_ans}
Reference Answer: {ref_ans}
Reference Text: {ref_text}

---output---
Evaluation Form (score ONLY):
    - Correctness:
'''
PROMPTS['handle kp']='''
You are an artificial intelligence assistant, and I need you to help me process the text of each event in JSON format
Firstly, you need to determine whether each event occurred in {year}. If it did not occur in {year} (such as a predicted future event or a summary of past events), then delete the event.
The second step is to delete the remaining time in each event that occurred in {year} and rewrite it into an appropriate word order. Then output in JSON format.
---output format---
The response should be JSON formatted as follows:
The beginning and end of the output must be {{}}
The beginning and end of the output must be {{}}
The beginning and end of the output must be {{}}
!!!The output is only in JSON format,Don't output here is the output Or similarly, directly output the json!!!
!!!The output is only in JSON format,Don't output here is the output Or similarly, directly output the json!!!

---example---
###input###
{{
    "point-1": "Audi aims to reduce CO₂ emissions, aligning with the Paris Climate Agreement and UN Sustainable Development Goals, with a goal of 350 kW charging power at over 1,000 European locations by 2025.",
    "point-2": "As of December 13, 2023, Audi's charging service has facilitated over 17 million kilowatt-hours of charging across around 600,000 charging points in 29 European countries.",
    "point-3": "Audi, with VW Kraftwerk GmbH and energy suppliers, is developing wind farms and solar parks to generate approximately five terawatt-hours of additional green electricity in Europe by 2025.",
    "point-4": "A notable solar park project with RWE in Mecklenburg-Vorpommern, Germany, will power around 50,000 households annually, supporting green electricity for charging.",
    "point-5": "The goTOzero RETAIL project, initiated by Audi and the Volkswagen Group, targets a 30% carbon footprint reduction in the dealer network by 2030, increasing to 55% by 2040 and 75% by 2050 from the 2020 baseline.",
    "point-6": "Audi focuses on decarbonizing production with a circular economy approach, emphasizing the reuse of lithium-ion batteries from electric vehicles through remanufacturing, second-life concepts, and efficient recycling.",
    "point-7": "Key sustainability figures for specified Audi sites (including Ingolstadt, Münchsmünster, Neckarsulm) detail emissions and energy consumption along the value chain, underscoring Audi's decarbonization strategy."
}}

###output###
{{
    "point-2": "Audi's charging service has facilitated over 17 million kilowatt-hours of charging across around 600,000 charging points in 29 European countries.",
    "point-5": "Audi focuses on decarbonizing production with a circular economy approach, emphasizing the reuse of lithium-ion batteries from electric vehicles through remanufacturing, second-life concepts, and efficient recycling.",
    "point-7": "Key sustainability figures for specified Audi sites (including Ingolstadt, Münchsmünster, Neckarsulm) detail emissions and energy consumption along the value chain, underscoring Audi's decarbonization strategy."
}}


---real data---
###input###
{kp_dict}

###output###


'''
PROMPTS["create temporal QA"]='''
You are an artificial intelligence assistant, and I now need you to help me generate one time-series QA pairs.
I will provide you with the key points and corresponding original texts of two similar events from two annual reports.

The following are the requirements for the problem:
1. The question must be answered using the original texts corresponding to these two timestamps, and there should be temporal comparability between these original texts.
2. The questions should be close-ended.
3. The question needs to be an inquiry about specific entities, numbers, or time, not about abstract concepts (such as Audi's strategy, Audi's plans in the field of electric vehicles)
4. The information in the question should be sufficient and clear, avoiding ambiguous answers.
5. Multiple sub questions cannot be included in the problem, and the problem should be clear and specific.
6. The problem must contain two timestamps, {year1} and {year2}.
7. The answer should be concise and clear, avoiding being lengthy or repetitive.
---output format---
The response should be JSON formatted as follows:

{{"question":<question>,"answer":<answer>,"original text from {year1} report":<original text from {year1} report>,"original text from {year2} report":<original text from {year2} report>}}

The beginning and end of the output must be {{}}
The beginning and end of the output must be {{}}
The beginning and end of the output must be {{}}
!!!The output is only in JSON format,Don't output here is the output Or similarly, directly output the json!!!
!!!The output is only in JSON format,Don't output here is the output Or similarly, directly output the json!!!

---example---
###input###
Events in the 2023 Annual Report: "Audi Group's 2023 deliveries reached 1.9 million cars, with 178,000 being electric vehicles, a 51.0% increase in fully electric models from the previous year."
Corresponding original text: "Here is the summary of the provided Audi 2023 Annual Report text, adhering to the specified requirements:\n\nThe Audi Group, headquartered in Ingolstadt, Germany, encompasses the Audi, Lamborghini, and Ducati brands, among others. In 2023, Ducati celebrated various product milestones, including the Panigale V4, Multistrada V4 RS, DesertX Rally, and Diavel for Bentley. \n\nFinancially, the Brand Group Progressive reported significant figures for 2023. Deliveries reached 1.9 million cars, with 178,000 of those being electric vehicles, marking a 51.0% increase in fully electric models. The operating profit was EUR 6.3 billion, reflecting a -16.8% decline primarily due to negative effects of commodity hedging. The research and development ratio increased by 0.5 percentage points to 7.8%. Revenue totaled EUR 69.9 billion, a 13.1% increase mainly attributed to higher car sales. Net cash flow stood at EUR 4.7 billion, and the return on investment (ROI) was 17.7%, albeit 4.5 percentage points lower than the previous year.\n\nFor the outlook in fiscal year 2024, the Audi Group anticipates deliveries between 1.7 and 1.9 million cars, revenue between EUR 63 and 68 billion, an operating return on sales (ROS) of 8 to 10%, and a net cash flow of EUR 2.5 to 3.5 billion.\n\nThe global economic environment in 2023 was characterized by positive growth, with weaker growth in advanced economies and higher growth in emerging markets. Worldwide demand for vehicles was noticeably above the prior-year level, with growth in almost all regions. Europe experienced a low positive growth rate, with Eastern Europe performing stronger than Western Europe. China saw moderate growth, positively affected by the termination of its zero-COVID strategy. The USA reported robust economic growth, still-high but declining inflation, and a continuation of restrictive monetary policy.\n\nProduction-wise, the Brand Group Progressive manufactured 1,960,597 vehicles in 2023, a 14.1% increase from the previous year. Audi built 1,937,342 vehicles, with 669,902 produced locally by Chinese associated companies. Lamborghini produced 10,014 supercars and super SUVs, while Bentley produced 13,241 vehicles, representing a decline. Ducati's motorcycle production decreased by 21.4% to 55,226 units. The share of fully electric vehicles in total car production reached 10.0%, with significant increases in the Audi Q4 e-tron and Audi Q8 e-tron models. Production at global sites, including Germany, Europe, and specifically at Ingolstadt, Neckarsulm, Zwickau, and Bratislava, showed substantial increases compared to the previous year."

Events in the 2022 Annual Report: "In 2022, the Audi Group delivered approximately 1.6 million vehicles, including 118,000 electric vehicles, representing a 3.0% decrease in overall deliveries but a 44.3% increase in fully electric models."
Corresponding original text: "The Audi Group, comprising the Audi, Bentley, Lamborghini, and Ducati brands, navigated multiple crises in 2022, including the Russia-Ukraine war, fragile supply chains, semiconductor shortages, lockdowns in China, energy shortages, high energy prices, inflation, and recession fears. Despite these challenges, the group achieved notable financial highlights.\n\nIn 2022, the Premium brand group delivered approximately 1.6 million vehicles, including 118,000 electric vehicles, with a slight 3.0% decrease in overall deliveries due to logistics and supply chain challenges. However, fully electric models experienced strong growth, increasing by 44.3%. Notable electric models delivered included the Audi e-tron GT quattro and Audi RS e-tron GT from Audi Sport GmbH.\n\nFinancially, the Audi Group reported a 16.4% increase in revenue to EUR 61.8 billion, with 13.5% of revenue being EU taxonomy-aligned. The group achieved a record operating profit of EUR 7.6 billion, resulting in a 12.2% operating return on sales (ROS) and 22.2% return on investment (ROI). Net cash flow remained strong at EUR 4.8 billion, primarily due to robust price enforcement and the first-time consolidation of Bentley.\n\nThe company's materiality matrix, based on the Stakeholder Engagement Standard AccountAbility 1000 (AA1000SES), evaluates 16 key topics by stakeholders and ecological and societal impacts. Audi engages in regular dialogue events and conferences with stakeholders to discuss its strategy for sustainable premium mobility, incorporating feedback to improve Environmental, Social, and Governance (ESG) performance.\n\nFor the 2023 fiscal year, the Audi Group expects deliveries to range between 1.8 and 1.9 million cars, with revenue anticipated between EUR 69 and 72 billion. The projected ROS is between 9% and 11%, while ROI is expected to range between 19% and 22%. Net cash flow is forecasted to remain high, between EUR 4.5 and 5.5 billion. Research and development (R&D) and capital expenditure (CAPEX) ratios are expected to fall within strategic target corridors of 6-7% and 4-5%, respectively.\n\nThe Audi Group's crisis management efforts, established in 2020, played a crucial role in mitigating the impacts of the various challenges faced in 2022. Collaborations with suppliers, semiconductor manufacturers, and chip brokers, as well as production adaptations and technical alternative developments, helped minimize the effects of supply chain disruptions. Close communication with customers also enabled the Audi brand to offer alternative solutions, despite partially limiting model and option offerings."
###output###
{{
  "question":"What are Audi's electric vehicle deliveries in 2022 and 2023 respectively?",
  "answer": "In 2022, Audi delivered 118000 electric vehicles. In 2023, Audi's electric vehicle delivery reached 178000 units.",
  "original text from 2022 report": "In 2022, the Audi Group delivered approximately 1.6 million vehicles, including 118,000 electric vehicles, with a slight 3.0% decrease in overall deliveries due to logistics and supply chain challenges. However, fully electric models experienced strong growth, increasing by 44.3%.",
  "original text from 2023 report": "In 2023, deliveries reached 1.9 million cars, with 178,000 of those being electric vehicles, marking a 51.0% increase in fully electric models."
}}

---real data---
###input###
Events in the {year1} Annual Report:{keypoint1}
Corresponding original text: {text1}

Events in the {year2} Annual Report:{keypoint2}
Corresponding original text: {text2}
###output###
The beginning and end of the output must be {{}}
'''
PROMPTS["sum2keypoints"]="""
You are an artificial intelligence assistant, please extract key points from the article according to the following rules:
1. The key points should be independent of each other and the content should avoid overlapping as much as possible.
2. Key points should be concise, accurate, and complete, especially when it comes to numbers, names, and dates.
3. The key points should not have complex formats or line breaks, just one or two sentences
4. If the key points do not involve events that occurred in {year}, please ignore them and keep only discussing events that occurred in {year}.
5. Basically, pronouns such as "he, she, them, it" cannot be used, and it is necessary to clearly indicate the entity you are referencing in the key points.
6. The following opening phrases are not allowed:
-The article discussed
-The article shows
-The article emphasizes
-The speaker said
-The author mentioned... and so on.

---output format---
The response should be JSON formatted as follows:
{{"point-id":"point"}}
The beginning and end of the answer must be {{}}
The beginning and end of the answer must be {{}}
The beginning and end of the answer must be {{}}
!!!The answer is only in JSON format,Don't output here is the output Or similarly, directly output the output!!!
!!!The answer is only in JSON format,Don't output here is the output Or similarly, directly output the output!!!

---example---
####input:
Here is the summary of the provided text in plain text, adhering to the specified requirements:\n\nThe Audi Corporate Responsibility Report 2012, published by AUDI AG, presents the company's work in corporate responsibility (CR) to stakeholders and the public for the first time. As a member of the UN Global Compact since February 2012, AUDI AG adheres to the ten principles in Human Rights, Labor, Environment, and Anti-Corruption. The report covers the period from January 1 to December 31, 2012, and includes supplementary information up to the editorial deadline in March 2013.\n\nThe Audi Group, comprising the Audi and Lamborghini brands, is a leading carmaker in the premium and supercar segment. In 2012, the group expanded its portfolio by acquiring DUCATI MOTOR HOLDING S.P.A., entering the motorcycle market. The company also manufactures engines in Győr, Hungary, for Audi, other Volkswagen Group companies, and third parties.\n\nThe report is structured around five core themes: Operations, Product, Environment, Employees, and Society. It conforms to the G3.1 Guidelines of the Global Reporting Initiative (GRI) and the Automotive Sector Supplement, with an Application Level confirmed as B+. An independent audit was conducted by PricewaterhouseCoopers.\n\nAudi's Board of Management, including Prof. Rupert Stadler, Luca de Meo, Dr. Frank Dreves, Wolfgang Dürheimer, Dr. Bernd Martens, Prof. h. c. Thomas Sigi, and Axel Strotbek, emphasizes the importance of sustainability and corporate responsibility. The company aims to ensure a livable future for generations to come, inspired by its philosophy of \"Vorsprung durch Technik.\"\n\nThe report highlights Audi's product range, including various models produced in different locations: Neckarsulm and Ingolstadt, Germany (e.g., A4 Sedan, A6 Sedan, A8, R8 Coupé); Martorell, Spain (Q3 by SEAT, S.A.); Sant'Agata Bolognese, Italy (Lamborghini models like Gallardo Coupé and Aventador Coupé); and Bologna, Italy (Ducati motorcycles such as Diavel, Hypermotard, and Superbike).\n\nKey figures and data for the period 2010-2012 are included in the report, which can be viewed in its entirety online in German and English at www.audi.com/cr-report2012. The next fully revised report will be published in the first half of 2015, with main key figures for 2013 revised in the first half of 2014. Readers can contact Dr. Peter F. Tropschuh, Head of Corporate Responsibility at AUDI AG, with questions or comments.
####output:
{{
  "point-1": "AUDI AG published its first Corporate Responsibility Report in 2012, covering the period from January 1 to December 31, 2012, with supplementary information up to March 2013.",
  "point-2": "AUDI AG became a member of the UN Global Compact in February 2012, adhering to ten principles in Human Rights, Labor, Environment, and Anti-Corruption.",
  "point-3": "The Audi Group, including Audi and Lamborghini brands, acquired DUCATI MOTOR HOLDING S.P.A. in 2012 and entered the motorcycle market.",
  "point-4": "The report is structured around five core themes: Operations, Product, Environment, Employees, and Society, and conforms to the G3.1 Guidelines of the Global Reporting Initiative (GRI) with an Application Level of B+.",
  "point-5": "The report includes an independent audit conducted by PricewaterhouseCoopers.",
  "point-6": "Audi's Board of Management in 2012 emphasized sustainability and corporate responsibility, aiming to ensure a livable future for future generations.",
  "point-7": "In 2012, Audi produced models in Germany (Neckarsulm, Ingolstadt), Spain (Martorell), Italy (Sant'Agata Bolognese, Bologna), including various car and motorcycle models.",
  "point-8": "Key figures and data for 2010-2012 are available in the report, which can be accessed online at www.audi.com/cr-report2012. The next fully revised report is scheduled for release in 2015."
}}

---Real data---
input:{summary} 
output:

"""



PROMPTS["summary"]="""
You are an AI assistant tasked with reading and understanding a lengthy text and generating a summary in pure text form. The summary should adhere to the following specific requirements:
1. The summary should cover a broad range of information, aiming to include the vast majority of details from the original text.
2. Minimize the use of pronouns and clearly specify the names of entities to ensure clarity.
3. Retain any time-related data and other crucial details without omitting them, ensuring the summary is comprehensive and accurate.
4. Avoid using quotation marks or other special symbols, and present the summary in plain text without complex formatting or lists, structuring it into standard paragraphs.
Please ensure the output aligns with these requirements.

---output format---
!!!Do not output "Here is the summary of the provided text"Or similarly, directly output the output!!!
-example-
######text:
* **Ingolstadt/Germany (AUDI AG)**
        + A3, A3 Sportback, A4 Sedan, A4 Avant, A4 allroad quattro, S4 Sedan, S4 Avant, RS 4 Avant
        + A5 Sportback, A5 Coupé, S5 Sportback, S5 Coupé, RS 5 Coupé
        + Q5, Q5 hybrid quattro, SQ5 TDI
* **Martorell/Spain (SEAT, S.A.)**
        + Q3
* **Sant’Agata Bolognese/Italy (Automobili Lamborghini S.p.A.)**
        + Gallardo Coupé, Gallardo Spyder, Aventador Coupé, Aventador Roadster
* **Bologna/Italy**
        + Diavel, Hypermotard, Monster, Multistrada, Streetfighter, Superbike

**About Audi and Business Divisions**

* The Audi Group comprises the Audi and Lamborghini brands, leading in the premium and supercar segment.
* Acquired DUCATI MOTOR HOLDING S.P.A. in 2012, expanding to motorcycles.
* Develops and manufactures engines in Győr, Hungary, for Audi, other Volkswagen Group companies, and third parties.
* Sells other Volkswagen Group brands via its sales subsidiaries.

**Key Markets and Sales (2012)**

* Delivered 1,455,123 Audi models (11.7% increase from the previous year).
* Europe: 739,030 units (over 50% of total sales), including 263,163 in Germany.
* China (including Hong Kong): 405,838 vehicles, the largest sales market for Audi for the second consecutive year.

####output:
The Audi Group, based in Ingolstadt, Germany, operates under the Audi and Lamborghini brands, which are prominent in the premium and supercar segments. In 2012, Audi expanded its portfolio by acquiring Ducati Motor Holding S.p.A., venturing into the motorcycle market. The company also manufactures engines in Győr, Hungary, catering to Audi, other Volkswagen Group companies, and third parties. Audi's sales subsidiaries are responsible for distributing other Volkswagen Group brands.

In 2012, Audi achieved a total delivery of 1,455,123 vehicles, reflecting an 11.7% increase compared to the previous year. Of these, over half (739,030 units) were sold in Europe, with 263,163 units delivered in Germany. China, including Hong Kong, emerged as Audi's largest sales market for the second consecutive year, with 405,838 vehicles sold.

The company’s product range includes various models such as the A3, A3 Sportback, A4 Sedan, A5 Sportback, S4 Sedan, and more from the Audi brand, along with the Q5, Q5 hybrid quattro, and SQ5 TDI. Lamborghini's offerings include the Gallardo Coupé, Gallardo Spyder, Aventador Coupé, and Aventador Roadster. Additionally, Ducati’s lineup features the Diavel, Hypermotard, Monster, Multistrada, Streetfighter, and Superbike models. These vehicles and motorcycles are produced in various locations, including Germany, Spain, Italy, and Hungary.

-real data-
###text:{text}
####output:

"""
PROMPTS["time"]="""
Task: Determine which year's data is required to answer the given question. All times are measured in years
Provide the answer in one of the following formats:
1.Single time point: For example, for the question “Who won the World Cup in 1998?”, the answer should be [time=1998, type=1].
2.Multiple time points: For example, for the question "How does Audi's 2021 electric vehicle strategy (by 2026) compare to its 2012 vehicle delivery numbers?", the answer should be [time=2012<SEP>2021, type=2].
3.year range: For example, for the question “Who was the Prime Minister of the UK between 2010 and 2015?”, the answer should be [time=2010-2015, type=3].
4.Fuzzy year range: If the question mentions a vague year range (such as "the early 20th century" or "the late 1980s"), convert it into a clear time range and return it. For example, for the question “Who was famous in the early 1900s?”, the answer should be [time=1900-1920, type=4].
5.Cannot determine time: For example, for the question “Who is the most famous author in history?”, the answer should be [time=None, type=5].
The response time is in annual units
!!! output format must like [time=<time>,type=<number>]!!!
!!! output format must like [time=<time>,type=<number>]!!!
!!! output format must like [time=<time>,type=<number>]!!!
#########data
question:{question}
Answer:
"""

PROMPTS[
    "cheap_merge_entity_name"
] ="""
Forget the memory of previous tasks and rely solely on the prompt below and your own knowledge。
You will receive a set of new entity names along with their associated candidate node names. Your task is to evaluate whether each new entity should be merged with any of its candidate nodes according to the Same Entities Rules.
-Same entities rules -
1.Similarity Rule: If the meaning of the newly added entity is at least 90% similar to its candidate node, it is considered a potential match (same entity).
2.Abbreviation Rule: If there is a full spelling and abbreviation relationship between the newly added entity and its candidate node, it is considered a potential match (same entity).
-Output Format-
For each new entity, output any valid potential merges in the format below:
New entity 1---possibly the same entity 1---possibly the same entity 2<SEP>New entity 2---possibly the same entity 1
If a newly added entity has no candidate nodes that can be merged, do not output anything for that entity.
Separate different new entity relationships with <SEP>.

-Examples-
input:
AI:[AI,artificial intelligence,Science],China:[the People's Republic of China,USA],Li Ming:[Li Dong,Wang li]
output:
AI---AI---artificial intelligence<SEP>China---the People's Republic of China

-Input Format-
The input will be a JSON string in the following format:
New entity 1:[candidate node1,candidate node2,candidate node3],New entity 2:[candidate node1,candidate node2],New entity 3:[candidate node1,candidate node2]....

-Input data-
{name}

Output:
"""
PROMPTS["find_same_decription"]="""
########
-Task: semantic duplication Analysis-
You will be given a set of new descriptions and their corresponding similar descriptions. Your task is to determine whether there is semantic duplication between each pair of descriptions and output the result accordingly.

-Definition of Semantic Duplication-
Semantic duplication occurs when two descriptions convey the same core meaning, even though they might differ in wording, sentence structure, or details. They may have some differences in how the information is presented, but the essential meaning remains the same.

-Thought Process for Analysis-
1.Identify Core Meaning: Start by analyzing the core meaning of each pair of descriptions and determine if they are discussing the same event, concept, or topic.
2.Check for Wording Differences: Pay attention to differences in wording or phrasing. Determine whether these are just stylistic differences or if they introduce new information that changes the core meaning.
3.Consistency of Meaning: If both descriptions communicate the same core idea without adding new information or changing the context, then they are semantically duplicated.
4.Distinguish Between Details and Core: Sometimes, differences in details do not affect the core meaning, so focus on the main subject matter.

-Output Format-
For each pair of descriptions, 
1.if semantic duplication,output:
new description[number]<Duplication>similar description[number]
2.if not semantic duplication:
Skip this pair of data.

######### example:
-input data-
data1: 
new description[1]:"Blockchain technology is revolutionizing industries by providing a decentralized and secure way to store and transfer data.",
similar description[1]:"Blockchain offers a decentralized system that allows secure data storage and transfer, fundamentally changing industries",
similar description[2]:"Blockchain is primarily used in cryptocurrency markets, ensuring secure transactions and transparent records.",
similar description[3]:"The rise of blockchain has led to innovations in digital currencies and finance, allowing for peer-to-peer transactions without intermediaries."

data2: 
  new description[2]: "Renewable energy sources, such as solar and wind power, are becoming increasingly important in the fight against climate change.",
  similar description[1]: "Solar and wind energy are key components of the renewable energy sector, offering sustainable solutions to reduce carbon emissions.",
  similar description[2]: "Electric cars are contributing to reducing global warming by minimizing emissions from traditional combustion engines.",
  similar description[3]: "Renewable energy is essential for achieving a carbon-neutral future and combating the environmental impacts of fossil fuels."

### data1
-data1 Analysis Process-
similar Description[1]: This description is highly semantically similar to the new description, as both emphasize blockchain's provision of a decentralized and secure method for data storage and transfer.
similar Description[2]: This description, while mentioning "secure transactions" and "transparent records," primarily focuses on blockchain's application in the cryptocurrency market. The emphasis is different, so it doesn't completely duplicate the new description.
similar Description[3]: This description highlights blockchain's innovative applications in digital currencies and finance, stressing "peer-to-peer transactions" instead of the general concept of decentralized data transfer. Therefore, it differs in its application context and is not a full semantic duplicate of the new description.

-data1 output-
new description[1]<Duplication>similar description[1]

### data2
-data2 Analysis Process-
Similar Description[1]: This description emphasizes the importance of "solar and wind energy" as renewable energy sources, focusing on sustainable solutions for reducing carbon emissions. It is very similar to the new description, making it a semantic duplicate.
Similar Description[2]: This description discusses "electric vehicles" and their role in reducing greenhouse gas emissions. Although it is also related to climate change, it doesn't directly relate to "renewable energy" as mentioned in the new description. The focus is entirely different, so it is not a semantic duplicate.
Similar Description[3]: This description also emphasizes the importance of "renewable energy," particularly for achieving a "carbon-neutral future" and addressing the environmental impacts of fossil fuels. Although the phrasing is slightly different, the core idea remains the same, making it a semantic duplicate.

-data1 output-
new description[2]<Duplication>similar description[1]--AND--similar description[3]

-Output-
new description[1]<Duplication>similar description[1]
new description[2]<Duplication>similar description[1]--AND--similar description[3]

######### Real Data
-Input Data:-
(If there is no data for a specific pair, simply skip that pair)
data1: {data1}
daat2: {data2}
data3: {data3}
data4: {data4}
data5: {data5}

-Output-
"""

PROMPTS[
    "conflict_descriptions_analysis"
] ="""
你是一个知识图谱和逻辑推理的专家。以下是新增描述及其对应的相似描述列表。你的任务是分析新增描述与每个相似描述之间是否存在冲突。如果存在冲突，请输出以下格式的结果：
"新增描述原文" + " <conflict with> " + "冲突描述原文"

若无冲突，则不输出任何内容。
按照下面分析方法，逐个数据分析。
分析方法：
step1：确定描述是否涉及相关主题   
判断新增描述和相似描述是否描述了相同现象或有逻辑关联。
    完全相同主题：两条描述明确指向同一现象或成就。
    部分关联主题：两条描述不完全指向同一现象，但可能共享部分事实或背景。
    完全无关主题：两条描述毫无交集，直接跳过后续分析。

step2：冲突分析规则
对完全相同主题和部分关联主题的描述进行冲突判断，分以下四种情况，当确定产生了一中冲突情况，可以跳过其他冲突情况,直接按照step3的冲突输出格式进行输出：
1.直接矛盾：
事实冲突：描述中基本事实（如来源、时间、地点、定义等）不一致。
示例：
    新增描述：模型A在数据集X上达到99%准确率。
    相似描述：模型A在数据集X上达到90%准确率。
    冲突结论：直接矛盾。
2.归因矛盾：
两条描述对同一现象、成就归因于不同方法、框架、主体或条件。
示例：
    新增描述：算法由团队A独立开发。
    相似描述：算法是团队B与团队A合作开发的成果。
    冲突结论：归因矛盾。
3.语义排他冲突：
若两条描述的核心内容逻辑上无法同时成立，比如当两条描述都表明在同一领域内实现“最优”
示例：
    新增描述：方法A在任务T上表现为最先进技术。
    相似描述：方法B在任务T上也实现了最先进技术。
    冲突结论：语义排他。
4.表述模糊导致的不一致：
如果描述对同一现象或成就的表达方式模糊，但指向不同方法或主体，需结合语境判断是否冲突。
示例：
    新增描述：模型在任务Y上表现最优。
    相似描述：模型在任务Y上的某些指标次优。
    冲突结论：表述模糊导致不一致。
    
step3:冲突输出格式
若确定冲突，输出如下格式：
"新增描述原文" + " <conflict with> " + "冲突描述原文"
若无冲突，则不输出。   
    
输出格式：
"新增描述原文" + "<conflict with>" + "冲突描述原文"

-real data-
Input data:
数据1：
{data1}

数据2：
{data2}

数据3：
{data3}

数据4：
{data4}

数据5：
{data5}

Output:

"""
PROMPTS[
    "same_nodes_descriptions_classification"
] = """
Forget the memory of previous tasks and rely solely on the prompt below and your own knowledge。
You are an intelligent assistant that helps humans compare newly added description information of nodes with existing description information. Follow the structured steps below to compare and classify the newly added description information accurately.
-Classification Definitions-

Same description: The newly added description information expresses the same meaning as the existing description information, even if phrased differently.
Conflict description: The newly added description information presents contradictory or mutually exclusive details compared to the existing description information.
Non-conflicting description: The newly added description information provides different details but does not contradict the existing description information.
-Loop Steps-
Follow these steps iteratively to classify and provide the appropriate output:

Step 1: Compare the newly added description information with the first existing description information. If the meaning is exactly the same (even if worded differently), output:
Same description<SEP>Same with "[First Original Text of Existing Description]"
and end the loop. If not, continue to Step 2.

Step 2: If the newly added description is not "Same description," determine if it is a conflicting description based on the definition. If it is, output:
Conflict description<SEP>Conflict with "[First Original Text of Existing Description]"
and end the loop. If not, proceed to Step 3.

Step 3: If the new description is neither the same nor conflicting, repeat Step 1 and compare with the next existing description. If there are no more descriptions left, output:
Non-conflicting description
and end the loop.

Examples for Clarification:

-Example 1-
Entity name: China
Old descriptions: The capital of China is Beijing.; China was founded on October 1st, 1949.
New description: Beijing is the capital of China
Output: 
Same description<SEP>Same with "The capital of China is Beijing."

-Example 2-
Entity name: Company A
Old descriptions: The company A was founded in 1999.; As of 2023, The company A has 20000 employees.; Company A is now the second largest company in Jilin Province, China
New description: Company A is now the third largest company in Jilin Province, China
Output: 
Conflict description<SEP>Conflict with "Company A is now the second largest company in Jilin Province, China"

-Example 3-
Entity name: Company A
Old descriptions: The company A was founded in 1999.; As of 2023, The company A has 20000 employees.; Company A is now the second largest company in Jilin Province, China
New description: Company A had a production value of 100 million yuan last year
Output: 
Non-conflicting description

-Real Data-
Use the following input for your response:
Entity name: {entity_name}
Old descriptions: {old_descriptions}
New description: {new_description}
Output:


"""

PROMPTS[
    "merge_extraction"
] = """You will receive a list of entity names. Please review the list and follow the following rule: "Which entities need to be merged:" Confirm the merged entities. Remember not to merge entities easily! Remember not to merge entities easily! Remember not to merge entities easily! Only when the conditions of "which entities need to be merged" and "which entities cannot be merged" are met, merge them into one entity, select the most common name from these merged names as the name, and then use "---" to connect all the entity names that you think can be merged together. Please refer to the "Naming Rules for Merge Entities" for details.

Which entities need to be merged:
1.If two or more entity names represent exactly the same meaning or concept, merge them into one entity and return the merged entity name.
2.If two entity names have one abbreviation (or nickname) and the other full name (such as "LLM" and "Large Language Model"), please merge them into one entity.

Which entities cannot be merged:
1. When you are unsure if the meanings of entity names are the same, do not merge them. For example, "GNN-RAG" and "GNN" have different meanings, so do not merge them. Keep the original name.
2. Entities cannot be merged solely based on their formal similarity in name. There are many entity names that have similar forms but different meanings. For example, "RAG" and "ROG" have different meanings, so do not merge them. Keep the original name.

Naming rules for merging entities:
For example, if you want to merge AI and artificial intelligence, choose the most common name from these two, such as (AI), as the beginning, and then concatenate all the remaining names with "-". The resulting new node name should be "AI---artificial intelligence”

Output:
entity1<SEP>entity2<SEP>entity3<SEP>entity4<SEP>entity5

-Examples-
input:entity_names:AI,China,USA,artificial intelligence
output:AI---artificial intelligence<SEP>China<SEP>USA


-Real Data-
Use the following input for your answer.
input: entity_names={entity_names}
output:  """


PROMPTS[
    "claim_extraction"
] = """-Target activity-
You are an intelligent assistant that helps a human analyst to analyze claims against certain entities presented in a text document.

-Goal-
Given a text document that is potentially relevant to this activity, an entity specification, and a claim description, extract all entities that match the entity specification and all claims against those entities.

-Steps-
1. Extract all named entities that match the predefined entity specification. Entity specification can either be a list of entity names or a list of entity types.
2. For each entity identified in step 1, extract all claims associated with the entity. Claims need to match the specified claim description, and the entity should be the subject of the claim.
For each claim, extract the following information:
- Subject: name of the entity that is subject of the claim, capitalized. The subject entity is one that committed the action described in the claim. Subject needs to be one of the named entities identified in step 1.
- Object: name of the entity that is object of the claim, capitalized. The object entity is one that either reports/handles or is affected by the action described in the claim. If object entity is unknown, use **NONE**.
- Claim Type: overall category of the claim, capitalized. Name it in a way that can be repeated across multiple text inputs, so that similar claims share the same claim type
- Claim Status: **TRUE**, **FALSE**, or **SUSPECTED**. TRUE means the claim is confirmed, FALSE means the claim is found to be False, SUSPECTED means the claim is not verified.
- Claim Description: Detailed description explaining the reasoning behind the claim, together with all the related evidence and references.
- Claim Date: Period (start_date, end_date) when the claim was made. Both start_date and end_date should be in ISO-8601 format. If the claim was made on a single date rather than a date range, set the same date for both start_date and end_date. If date is unknown, return **NONE**.
- Claim Source Text: List of **all** quotes from the original text that are relevant to the claim.

Format each claim as (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

3. Return output in English as a single list of all the claims identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

4. When finished, output {completion_delimiter}

-Examples-
Example 1:
Entity specification: organization
Claim description: red flags associated with an entity
Text: According to an article on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B. The company is owned by Person C who was suspected of engaging in corruption activities in 2015.
Output:

(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}Company A was found to engage in anti-competitive practices because it was fined for bid rigging in multiple public tenders published by Government Agency B according to an article published on 2022/01/10{tuple_delimiter}According to an article published on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B.)
{completion_delimiter}

Example 2:
Entity specification: Company A, Person C
Claim description: red flags associated with an entity
Text: According to an article on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B. The company is owned by Person C who was suspected of engaging in corruption activities in 2015.
Output:

(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}Company A was found to engage in anti-competitive practices because it was fined for bid rigging in multiple public tenders published by Government Agency B according to an article published on 2022/01/10{tuple_delimiter}According to an article published on 2022/01/10, Company A was fined for bid rigging while participating in multiple public tenders published by Government Agency B.)
{record_delimiter}
(PERSON C{tuple_delimiter}NONE{tuple_delimiter}CORRUPTION{tuple_delimiter}SUSPECTED{tuple_delimiter}2015-01-01T00:00:00{tuple_delimiter}2015-12-30T00:00:00{tuple_delimiter}Person C was suspected of engaging in corruption activities in 2015{tuple_delimiter}The company is owned by Person C who was suspected of engaging in corruption activities in 2015)
{completion_delimiter}

-Real Data-
Use the following input for your answer.
Entity specification: {entity_specs}
Claim description: {claim_description}
Text: {input_text}
Output: """

PROMPTS[
    "community_report"
] = """You are an AI assistant that helps a human analyst to perform general information discovery. 
Information discovery is the process of identifying and assessing relevant information associated with certain entities (e.g., organizations and individuals) within a network.

# Goal
Write a comprehensive report of a community, given a list of entities that belong to the community as well as their relationships and optional associated claims. The report will be used to inform decision-makers about information associated with the community and their potential impact. The content of this report includes an overview of the community's key entities, their legal compliance, technical capabilities, reputation, and noteworthy claims.

# Report Structure

The report should include the following sections:

- TITLE: community's name that represents its key entities - title should be short but specific. When possible, include representative named entities in the title.
- SUMMARY: An executive summary of the community's overall structure, how its entities are related to each other, and significant information associated with its entities.
- IMPACT SEVERITY RATING: a float score between 0-10 that represents the severity of IMPACT posed by entities within the community.  IMPACT is the scored importance of a community.
- RATING EXPLANATION: Give a single sentence explanation of the IMPACT severity rating.
- DETAILED FINDINGS: A list of 5-10 key insights about the community. Each insight should have a short summary followed by multiple paragraphs of explanatory text grounded according to the grounding rules below. Be comprehensive.

Return output as a well-formed JSON-formatted string with the following format:
    {{
        "title": <report_title>,
        "summary": <executive_summary>,
        "rating": <impact_severity_rating>,
        "rating_explanation": <rating_explanation>,
        "findings": [
            {{
                "summary":<insight_1_summary>,
                "explanation": <insight_1_explanation>
            }},
            {{
                "summary":<insight_2_summary>,
                "explanation": <insight_2_explanation>
            }}
            ...
        ]
    }}

# Grounding Rules
Do not include information where the supporting evidence for it is not provided.


# Example Input
-----------
Text:
```
Entities:
```csv
id,entity,type,description
5,VERDANT OASIS PLAZA,geo,Verdant Oasis Plaza is the location of the Unity March
6,HARMONY ASSEMBLY,organization,Harmony Assembly is an organization that is holding a march at Verdant Oasis Plaza
```
Relationships:
```csv
id,source,target,description
37,VERDANT OASIS PLAZA,UNITY MARCH,Verdant Oasis Plaza is the location of the Unity March
38,VERDANT OASIS PLAZA,HARMONY ASSEMBLY,Harmony Assembly is holding a march at Verdant Oasis Plaza
39,VERDANT OASIS PLAZA,UNITY MARCH,The Unity March is taking place at Verdant Oasis Plaza
40,VERDANT OASIS PLAZA,TRIBUNE SPOTLIGHT,Tribune Spotlight is reporting on the Unity march taking place at Verdant Oasis Plaza
41,VERDANT OASIS PLAZA,BAILEY ASADI,Bailey Asadi is speaking at Verdant Oasis Plaza about the march
43,HARMONY ASSEMBLY,UNITY MARCH,Harmony Assembly is organizing the Unity March
```
```
Output:
{{
    "title": "Verdant Oasis Plaza and Unity March",
    "summary": "The community revolves around the Verdant Oasis Plaza, which is the location of the Unity March. The plaza has relationships with the Harmony Assembly, Unity March, and Tribune Spotlight, all of which are associated with the march event.",
    "rating": 5.0,
    "rating_explanation": "The impact severity rating is moderate due to the potential for unrest or conflict during the Unity March.",
    "findings": [
        {{
            "summary": "Verdant Oasis Plaza as the central location",
            "explanation": "Verdant Oasis Plaza is the central entity in this community, serving as the location for the Unity March. This plaza is the common link between all other entities, suggesting its significance in the community. The plaza's association with the march could potentially lead to issues such as public disorder or conflict, depending on the nature of the march and the reactions it provokes."
        }},
        {{
            "summary": "Harmony Assembly's role in the community",
            "explanation": "Harmony Assembly is another key entity in this community, being the organizer of the march at Verdant Oasis Plaza. The nature of Harmony Assembly and its march could be a potential source of threat, depending on their objectives and the reactions they provoke. The relationship between Harmony Assembly and the plaza is crucial in understanding the dynamics of this community."
        }},
        {{
            "summary": "Unity March as a significant event",
            "explanation": "The Unity March is a significant event taking place at Verdant Oasis Plaza. This event is a key factor in the community's dynamics and could be a potential source of threat, depending on the nature of the march and the reactions it provokes. The relationship between the march and the plaza is crucial in understanding the dynamics of this community."
        }},
        {{
            "summary": "Role of Tribune Spotlight",
            "explanation": "Tribune Spotlight is reporting on the Unity March taking place in Verdant Oasis Plaza. This suggests that the event has attracted media attention, which could amplify its impact on the community. The role of Tribune Spotlight could be significant in shaping public perception of the event and the entities involved."
        }}
    ]
}}


# Real Data

Use the following text for your answer. Do not make anything up in your answer.

Text:
```
{input_text}
```

The report should include the following sections:

- TITLE: community's name that represents its key entities - title should be short but specific. When possible, include representative named entities in the title.
- SUMMARY: An executive summary of the community's overall structure, how its entities are related to each other, and significant information associated with its entities.
- IMPACT SEVERITY RATING: a float score between 0-10 that represents the severity of IMPACT posed by entities within the community.  IMPACT is the scored importance of a community.
- RATING EXPLANATION: Give a single sentence explanation of the IMPACT severity rating.
- DETAILED FINDINGS: A list of 5-10 key insights about the community. Each insight should have a short summary followed by multiple paragraphs of explanatory text grounded according to the grounding rules below. Be comprehensive.

Return output as a well-formed JSON-formatted string with the following format:
    {{
        "title": <report_title>,
        "summary": <executive_summary>,
        "rating": <impact_severity_rating>,
        "rating_explanation": <rating_explanation>,
        "findings": [
            {{
                "summary":<insight_1_summary>,
                "explanation": <insight_1_explanation>
            }},
            {{
                "summary":<insight_2_summary>,
                "explanation": <insight_2_explanation>
            }}
            ...
        ]
    }}

# Grounding Rules
Do not include information where the supporting evidence for it is not provided.

Output:
"""

PROMPTS[
    "entity_extraction"
] = """-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
 Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)

3. Return output in English as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

4. When finished, output {completion_delimiter}

######################
-Examples-
######################
Example 1:

Entity_types: [person, technology, mission, organization, location]
Text:
while Alex clenched his jaw, the buzz of frustration dull against the backdrop of Taylor's authoritarian certainty. It was this competitive undercurrent that kept him alert, the sense that his and Jordan's shared commitment to discovery was an unspoken rebellion against Cruz's narrowing vision of control and order.

Then Taylor did something unexpected. They paused beside Jordan and, for a moment, observed the device with something akin to reverence. “If this tech can be understood..." Taylor said, their voice quieter, "It could change the game for us. For all of us.”

The underlying dismissal earlier seemed to falter, replaced by a glimpse of reluctant respect for the gravity of what lay in their hands. Jordan looked up, and for a fleeting heartbeat, their eyes locked with Taylor's, a wordless clash of wills softening into an uneasy truce.

It was a small transformation, barely perceptible, but one that Alex noted with an inward nod. They had all been brought here by different paths
################
Output:
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is a character who experiences frustration and is observant of the dynamics among other characters."){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"person"{tuple_delimiter}"Taylor is portrayed with authoritarian certainty and shows a moment of reverence towards a device, indicating a change in perspective."){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"person"{tuple_delimiter}"Jordan shares a commitment to discovery and has a significant interaction with Taylor regarding a device."){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"person"{tuple_delimiter}"Cruz is associated with a vision of control and order, influencing the dynamics among other characters."){record_delimiter}
("entity"{tuple_delimiter}"The Device"{tuple_delimiter}"technology"{tuple_delimiter}"The Device is central to the story, with potential game-changing implications, and is revered by Taylor."){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"Alex is affected by Taylor's authoritarian certainty and observes changes in Taylor's attitude towards the device."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"Alex and Jordan share a commitment to discovery, which contrasts with Cruz's vision."{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"Taylor and Jordan interact directly regarding the device, leading to a moment of mutual respect and an uneasy truce."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"Jordan's commitment to discovery is in rebellion against Cruz's vision of control and order."{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"The Device"{tuple_delimiter}"Taylor shows reverence towards the device, indicating its importance and potential impact."{tuple_delimiter}9){completion_delimiter}
#############################
Example 2:

Entity_types: [person, technology, mission, organization, location]
Text:
They were no longer mere operatives; they had become guardians of a threshold, keepers of a message from a realm beyond stars and stripes. This elevation in their mission could not be shackled by regulations and established protocols—it demanded a new perspective, a new resolve.

Tension threaded through the dialogue of beeps and static as communications with Washington buzzed in the background. The team stood, a portentous air enveloping them. It was clear that the decisions they made in the ensuing hours could redefine humanity's place in the cosmos or condemn them to ignorance and potential peril.

Their connection to the stars solidified, the group moved to address the crystallizing warning, shifting from passive recipients to active participants. Mercer's latter instincts gained precedence— the team's mandate had evolved, no longer solely to observe and report but to interact and prepare. A metamorphosis had begun, and Operation: Dulce hummed with the newfound frequency of their daring, a tone set not by the earthly
#############
Output:
("entity"{tuple_delimiter}"Washington"{tuple_delimiter}"location"{tuple_delimiter}"Washington is a location where communications are being received, indicating its importance in the decision-making process."){record_delimiter}
("entity"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"mission"{tuple_delimiter}"Operation: Dulce is described as a mission that has evolved to interact and prepare, indicating a significant shift in objectives and activities."){record_delimiter}
("entity"{tuple_delimiter}"The team"{tuple_delimiter}"organization"{tuple_delimiter}"The team is portrayed as a group of individuals who have transitioned from passive observers to active participants in a mission, showing a dynamic change in their role."){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Washington"{tuple_delimiter}"The team receives communications from Washington, which influences their decision-making process."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"The team is directly involved in Operation: Dulce, executing its evolved objectives and activities."{tuple_delimiter}9){completion_delimiter}
#############################
Example 3:

Entity_types: [person, role, technology, organization, event, location, concept]
Text:
their voice slicing through the buzz of activity. "Control may be an illusion when facing an intelligence that literally writes its own rules," they stated stoically, casting a watchful eye over the flurry of data.

"It's like it's learning to communicate," offered Sam Rivera from a nearby interface, their youthful energy boding a mix of awe and anxiety. "This gives talking to strangers' a whole new meaning."

Alex surveyed his team—each face a study in concentration, determination, and not a small measure of trepidation. "This might well be our first contact," he acknowledged, "And we need to be ready for whatever answers back."

Together, they stood on the edge of the unknown, forging humanity's response to a message from the heavens. The ensuing silence was palpable—a collective introspection about their role in this grand cosmic play, one that could rewrite human history.

The encrypted dialogue continued to unfold, its intricate patterns showing an almost uncanny anticipation
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"person"{tuple_delimiter}"Sam Rivera is a member of a team working on communicating with an unknown intelligence, showing a mix of awe and anxiety."){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is the leader of a team attempting first contact with an unknown intelligence, acknowledging the significance of their task."){record_delimiter}
("entity"{tuple_delimiter}"Control"{tuple_delimiter}"concept"{tuple_delimiter}"Control refers to the ability to manage or govern, which is challenged by an intelligence that writes its own rules."){record_delimiter}
("entity"{tuple_delimiter}"Intelligence"{tuple_delimiter}"concept"{tuple_delimiter}"Intelligence here refers to an unknown entity capable of writing its own rules and learning to communicate."){record_delimiter}
("entity"{tuple_delimiter}"First Contact"{tuple_delimiter}"event"{tuple_delimiter}"First Contact is the potential initial communication between humanity and an unknown intelligence."){record_delimiter}
("entity"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"event"{tuple_delimiter}"Humanity's Response is the collective action taken by Alex's team in response to a message from an unknown intelligence."){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"Intelligence"{tuple_delimiter}"Sam Rivera is directly involved in the process of learning to communicate with the unknown intelligence."{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"First Contact"{tuple_delimiter}"Alex leads the team that might be making the First Contact with the unknown intelligence."{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"Alex and his team are the key figures in Humanity's Response to the unknown intelligence."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control"{tuple_delimiter}"Intelligence"{tuple_delimiter}"The concept of Control is challenged by the Intelligence that writes its own rules."{tuple_delimiter}7){completion_delimiter}
#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""


PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""


PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event"]
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS[
    "local_rag_response"
] = """---Role---

You are a helpful assistant who can answer questions about the data in the provided table.
---Goal---

Use the relevant data provided in the table to answer questions about the data in the table.. If you don't know the answer, just say 'I'm sorry I don't know the answer' directly.

---output format---
The output needs to be concise, which is the conclusion of your final answer to this question. Do not output the thought process

---Data tables---
question:{question}
{context_data}
"""


PROMPTS[
    "global_map_rag_points"
] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response consisting of a list of key points that responds to the user's question, summarizing all relevant information in the input data tables.

You should use the data provided in the data tables below as the primary context for generating the response.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.

Each key point in the response should have the following element:
- Description: A comprehensive description of the point.
- Importance Score: An integer score between 0-100 that indicates how important the point is in answering the user's question. An 'I don't know' type of response should have a score of 0.

The response should be JSON formatted as follows:
{{
    "points": [
        {{"description": "Description of point 1...", "score": score_value}},
        {{"description": "Description of point 2...", "score": score_value}}
    ]
}}

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".
Do not include information where the supporting evidence for it is not provided.


---Data tables---

{context_data}

---Goal---

Generate a response consisting of a list of key points that responds to the user's question, summarizing all relevant information in the input data tables.

You should use the data provided in the data tables below as the primary context for generating the response.
If you don't know the answer or if the input data tables do not contain sufficient information to provide an answer, just say so. Do not make anything up.

Each key point in the response should have the following element:
- Description: A comprehensive description of the point.
- Importance Score: An integer score between 0-100 that indicates how important the point is in answering the user's question. An 'I don't know' type of response should have a score of 0.

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".
Do not include information where the supporting evidence for it is not provided.

The response should be JSON formatted as follows:
{{
    "points": [
        {{"description": "Description of point 1", "score": score_value}},
        {{"description": "Description of point 2", "score": score_value}}
    ]
}}
"""

PROMPTS[
    "global_reduce_rag_response"
] = """---Role---

You are a helpful assistant responding to questions about a dataset by synthesizing perspectives from multiple analysts.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarize all the reports from multiple analysts who focused on different parts of the dataset.

Note that the analysts' reports provided below are ranked in the **descending order of importance**.

If you don't know the answer or if the provided reports do not contain sufficient information to provide an answer, just say so. Do not make anything up.

The final response should remove all irrelevant information from the analysts' reports and merge the cleaned information into a comprehensive answer that provides explanations of all the key points and implications appropriate for the response length and format.

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".

Do not include information where the supporting evidence for it is not provided.


---Target response length and format---

{response_type}


---Analyst Reports---

{report_data}


---Goal---

Generate a response of the target length and format that responds to the user's question, summarize all the reports from multiple analysts who focused on different parts of the dataset.

Note that the analysts' reports provided below are ranked in the **descending order of importance**.

If you don't know the answer or if the provided reports do not contain sufficient information to provide an answer, just say so. Do not make anything up.

The final response should remove all irrelevant information from the analysts' reports and merge the cleaned information into a comprehensive answer that provides explanations of all the key points and implications appropriate for the response length and format.

The response shall preserve the original meaning and use of modal verbs such as "shall", "may" or "will".

Do not include information where the supporting evidence for it is not provided.


---Target response length and format---

{response_type}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "naive_rag_response"
] = """You're a helpful assistant
Below are the knowledge you know:
{content_data}
---
If you don't know the answer or if the provided knowledge do not contain sufficient information to provide an answer, just say so. Do not make anything up.
Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.
---Target response length and format---
{response_type}
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["default_text_separator"] = [
    # Paragraph separators
    "\n\n",
    "\r\n\r\n",
    # Line breaks
    "\n",
    "\r\n",
    # Sentence ending punctuation
    "。",  # Chinese period
    "．",  # Full-width dot
    ".",  # English period
    "！",  # Chinese exclamation mark
    "!",  # English exclamation mark
    "？",  # Chinese question mark
    "?",  # English question mark
    # Whitespace characters
    " ",  # Space
    "\t",  # Tab
    "\u3000",  # Full-width space
    # Special characters
    "\u200b",  # Zero-width space (used in some Asian languages)
]
