# import libraries
import pandas as pd
import spacy
from spacy import displacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

remote = ["Remote", "work from home", "work from wherever", "telecommute", "work from home", "WFH", "team retreat",
          "remote", "work from anywhere", "work from wherever", "remote friendly", "telecommute", "remote",
          "distributed", "global", "worldwide", "telecommute", "anywhere", "work remotely", "remote first",
          "remote work", "remote only", "distributed team",
          "remote job", "remote team", "remote teams", "remote-team", "remote-teams", "remote-first", "remote-only",
          "remote-work", "work-remotely",
          "The position is remote", "fully remote work", "full remote work", "100% remote", 'remote', 'covid',
          'flexible', 'home', 'office',
          'location', 'visa', 'work from', 'anywhere', 'distributed', 'timezone', 'global', 'based in',
          'flexibility']

not_remote = ["Some remote work", "remote work when needed", "distributed networks", "distributed network",
              "remote control", "not remote", "no remote work"]
colors = {"REMOTE": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", 'NOT_REMOTE': '#B9F8FF', "LOC": '#996A60',
          'GPE': '#996A60'}
option = {"ents": ["REMOTE", 'NOT_REMOTE', 'LOC', 'GPE'], "colors": colors}

entities = {'REMOTE': remote, 'NOT_REMOTE': not_remote}


def enrich_description(description, entities_to_match, options):
    """

    :param description: a job description in html
    :param entities_to_match: list of new entities to match with keywords
    :param options: entities to highlight with color options
    :return: the highlighted html code of the job description
    """

    # initiate ner model
    ner = spacy.load('en_core_web_sm')

    # transform the text to spacy format
    doc = ner(description)

    # create the PhraseMatcher object
    matcher = PhraseMatcher(ner.vocab, attr='LOWER')

    for e in list(entities_to_match):
        # convert the phrases into document object using nlp.make_doc to #speed up.
        patterns = [ner.make_doc(text) for text in entities_to_match[e]]
        # add the patterns to the matcher object without any callbacks
        matcher.add(e, None, *patterns)

    # call the matcher object the document object
    # return match_id, start and stop indexes of the matched words
    matches = matcher(doc)

    # print the matched results and extract out the results
    for match_id, start, end in matches:
        # Get the string representation
        string_id = ner.vocab.strings[match_id]

        if string_id in list(entities_to_match):
            try:
                doc.ents += (Span(doc, start, end, label=doc.vocab.strings[string_id]),)
            except:
                pass

    # highlight the entities found and return the html code of the jd highlighted
    output = spacy.displacy.render(doc, style='ent', options=options, page=True)
    output = output.replace('&lt;', '<').replace('&gt;', '>')

    for i in options["ents"]:
        output = output.replace(
            '<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: '
            'middle; margin-left: 0.5rem">' + i + '</span>',
            "")
    return output



if __name__ == '__main__':
    df = pd.read_csv('./Data/job_export.csv')
    print(enrich_description(df.general_description[250], entities, option))
