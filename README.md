# Judgements Anonymization

In this project I will anonymize documents from criminal and civil judgments available free of charge online for consultation.
NER models are often used to anonymize documents. These models are trained to extract the text entities.

In this work an alternative method for anonymization is proposed which is based on the extraction of relationships within a text, in this case on criminal sentences.
From this spaCy project https://github.com/explosion/projects/tree/v3/tutorials/rel_component I built a pipeline and trained it to extract the relationships between judge and accused and between lawyer and accused, with the aim of identifying the accused entity and anonymizing it, because I think the relationship can help distinguish the entity I'm interested in (accused) from those I don't intend to anonymize (judge, lawyer). I used state of the art NLP via the spacy-transformers library.  More info in the report.pdf

I have created an interactive dashboard where you can enter any judgements by taking the link of the pdf from the following site http://www.italgiure.giustizia.it/sncass/ and you are shown a bar chart with top-k most likely defendants and a piece of the judgement with its anonymization. In addition, a copy of the pdf is downloaded in which the most eligible accused is obscured.
In the gif below the dashboard is shown and later on how to use it on colab is explained


<img src="https://github.com/Gianpe/NLP_Anonymization/blob/main/images/def_extractor2.gif" width="600" height="338"/>

### Install pipeline
```bash
pip install https://github.com/Gianpe/NLP_Anonymization/releases/download/v0.0.1/en_relation_def_extraction-0.0.1.tar.gz
```
### Usage on Colab to use dashboard
Open a Colab notebook and copy the following lines of code:
(Remember to change the runtime type and choose GPU)

Clone the repository and go to the Step4_Visualization folder
```bash
!git clone https://github.com/Gianpe/NLP_Anonymization.git
%cd /content/NLP_Anonymization/notebooks/Step4_Visualization/
```

Install the necessary libraries in the order they are in the requirements.txt file
```bash
!cat requirements.txt | xargs -n 1 -L 1 pip install
```

Use ngrok to create a tunnel between colab server and your localhost
(sign up on https://ngrok.com/ to obtain YOUR_TOKEN and replace it in the code below
```bash
#This step is necessary because the config file of a library we import is not updated and it brings to error. 
!grep -rl "defaults = yaml.load(f)" /usr/local/lib/python3.7/dist-packages/distributed/config.py | xargs sed -i 's/defaults = yaml.load(f)/defaults = yaml.load(f, Loader=yaml.FullLoader)/g'

!ngrok authtoken YOUR_TOKEN
```
Create the tunnel
```bash
from pyngrok import ngrok
#To run dash in colab it is necessary to create a tunnel. The first link will be the one to use to see the dashboards
ngrok.connect(8050)
```
Run the the dashboard
```bash
!python3 app.py
```
After running this code on colab click on the NgrokTunnel and the dashboard will open where you can enter the judgement link taken from the following link: http://www.italgiure.giustizia.it/sncass/.
The pdf of the judgement will be downloaded with the relative anonymization as in the image below:

<img src="https://github.com/Gianpe/NLP_Anonymization/blob/main/images/anon_sent.PNG" width="600" height="338"/>


## Usage pipeline
Libraries needed
```bash
pip install -U spacy-nightly --pre
pip install spacy==3.2.1
pip install transformers==4.15.0
pip install spacy_transformers==1.1.4
```
Install 2 pipelines
```bash
pip install https://github.com/Gianpe/NLP_Anonymization/releases/download/v0.0.1/en_relation_def_extraction-0.0.1.tar.gz
python -m spacy download it_core_news_lg
```
Import pipelines
```bash
import spacy

nlp_rel = spacy.load('en_relation_def_extraction')
nlp_it = spacy.load('it_core_news_lg')

text = ''' Con ordinanza in data 17/12/2020 il Giudice per le indagini preliminari del
Tribunale di Monza ha disposto, nei confronti di Gianmarco Pepi, la
revoca della sanzione sostitutiva dei lavori di pubblica utilit?? applicata, per la
durata di 86 giorni, in sostituzione della pena di 80 giorni di arresto e di
1.500,00 euro di ammenda'''

doc = nlp_rel(nlp_it(text))
print(doc._.rel)
```
