# Judgements anonymization

In this project I will anonymize documents from criminal and civil judgments available free of charge online for consultation.
NER is often used to anonymize documents. A model is trained to extract the text entities.

In this work an alternative method for anonymization is proposed which is based on the extraction of relationships within a text, in this case on criminal sentences.

From this spaCy project https://github.com/explosion/projects/tree/v3/tutorials/rel_component I built a pipeline and trained it to extract the relationships between judge and accused and between lawyer and accused, with the aim of identifying the accused entity and anonymizing it, because I think the relationship can help distinguish the entity I'm interested in (accused) from those I don't intend to anonymize (judge, lawyer). I used state of the art NLP via the spacy-transformers library.  More info in the report.pdf

I have created an interactive dashboard where you can enter any sentences by taking the link of the pdf from the following site http://www.italgiure.giustizia.it/sncass/ and you are shown a bar chart with top-k most likely defendants and a piece of the sentence with its anonymization. In addition, a copy of the pdf is downloaded in which the most papable accused is obscured.
In the gif below the dashboard is shown and later on how to use it on colab is explained


<img src="https://github.com/Gianpe/NLP_Anonymization/blob/main/images/def_extractor2.gif" width="600" height="338"/>

## Install pipeline
```bash
pip install https://github.com/Gianpe/NLP_Anonymization/raw/main/spacytransformers_umberto/package_tar_format/en_relation_def_extraction-0.0.1/dist/en_relation_def_extraction-0.0.1.tar.gz

```
