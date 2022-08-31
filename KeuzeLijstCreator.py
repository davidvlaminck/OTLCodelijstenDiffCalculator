import rdflib
from rdflib import Graph, URIRef


class Keuzelijst:
    def __init__(self, label='', definitie='', objectUri='', status=''):
        self.label = label
        self.definitie = definitie
        self.objectUri = objectUri
        self.keuzelijst_waardes = {}
        self.status = status


class KeuzelijstWaarde:
    def __init__(self, invulwaarde='', label='', definitie='', objectUri='', status=''):
        self.invulwaarde = invulwaarde
        self.label = label
        self.definitie = definitie
        self.objectUri = objectUri
        self.status = status


class KeuzelijstCreator:
    @classmethod
    def read_ttl_file_and_create_keuzelijst(cls, filepath: str = '', env: str = ''):
        g = KeuzelijstCreator.get_graph_from_file(filepath)
        k = KeuzelijstCreator.get_keuzelijstwaardes_from_graph(g, env)
        return k

    @classmethod
    def get_graph_from_file(cls, filepath: str = ''):
        g = rdflib.Graph()
        return g.parse(filepath, format="turtle")

    @classmethod
    def get_keuzelijstwaardes_from_graph(cls, g: Graph, env):
        k = Keuzelijst()

        subjects = set(g.subjects(predicate=None, object=None))
        distinct_subjects_list = sorted(subjects, key=lambda x: str(x), reverse=True)

        for distinct_subject in distinct_subjects_list:
            subject_str = str(distinct_subject)
            if 'conceptscheme' in subject_str:
                k.status = g.value(subject=distinct_subject, predicate=URIRef('https://www.w3.org/ns/adms#status'))
                if k.status is not None:
                    if env == 'tei':
                        k.status = str(k.status).replace(
                            'https://wegenenverkeer-test.data.vlaanderen.be/id/concept/KlAdmsStatus/', '').replace(
                            'https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAdmsStatus/', '')
                    else:
                        k.status = str(k.status).replace(
                            'https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAdmsStatus/', '')
                k.label = str(
                    g.value(subject=distinct_subject, predicate=URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')))
                k.objectUri = subject_str.replace('-test', '')
                k.definitie = str(
                g.value(subject=distinct_subject, predicate=URIRef('http://www.w3.org/2004/02/skos/core#definition')))

                continue

            waarde = KeuzelijstWaarde()
            waarde.objectUri = subject_str
            status = g.value(subject=distinct_subject, predicate=URIRef('https://www.w3.org/ns/adms#status'))
            if status is not None:
                if env == 'tei':
                    waarde.status = str(status).replace(
                        'https://wegenenverkeer-test.data.vlaanderen.be/id/concept/KlAdmsStatus/', '').replace(
                        'https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAdmsStatus/', '')
                else:
                    waarde.status = str(status).replace(
                        'https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAdmsStatus/', '')
            waarde.invulwaarde = str(
                g.value(subject=distinct_subject, predicate=URIRef('http://www.w3.org/2004/02/skos/core#notation')))
            waarde.definitie = str(
                g.value(subject=distinct_subject, predicate=URIRef('http://www.w3.org/2004/02/skos/core#definition')))
            waarde.label = str(
                g.value(subject=distinct_subject, predicate=URIRef('http://www.w3.org/2004/02/skos/core#prefLabel')))
            k.keuzelijst_waardes[waarde.invulwaarde] = waarde

        return k