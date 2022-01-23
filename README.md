# NLP_Anonymization

In this project I will anonymize documents from criminal and civil judgments available free of charge online for consultation.
NER is often used to anonymize documents. A model is trained to extract the text entities.

In this work an alternative method for anonymization is proposed which is based on the extraction of relationships within a text, in this case on criminal sentences.

From this spaCy project https://github.com/explosion/projects/tree/v3/tutorials/rel_component I built a pipeline and trained it to extract the relationships between judge and accused and between lawyer and accused, with the aim of identifying the accused entity and anonymizing it, because I think the relationship can help distinguish the entity I'm interested in (accused) from those I don't intend to anonymize (judge, lawyer). More info in the report.pdf
<img src="https://github.com/Gianpe/NLP_Anonymization/blob/main/images/def_extractor2.gif" width="600" height="338"/>
