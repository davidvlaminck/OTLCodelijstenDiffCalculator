import rdflib


class Keuzelijst:
    def __init__(self, label='', definitie='', objectUri=''):
        self.label = label
        self.definitie = definitie
        self.objectUri = objectUri
        self.keuzelijstWaardes = {}


class KeuzelijstWaarde:
    def __init__(self, invulwaarde='', label='', definitie='', objectUri=''):
        self.invulwaarde = invulwaarde
        self.label = label
        self.definitie = definitie
        self.objectUri = objectUri


class KeuzelijstCreator:
    @classmethod
    def read_ttl_file_and_create_keuzelijst(cls, filepath: str = ''):
        tuples_list = cls.load_ttl_file(filepath)
        keuzelijst = cls.convert_tuples_to_keuzelijst(tuples_list)
        return keuzelijst

    @classmethod
    def convert_tuples_to_keuzelijst(cls, tuples_list) -> Keuzelijst:
        k = Keuzelijst()
        for t in tuples_list:
            if 'conceptscheme' in t[0]:
                if '#ConceptScheme' in t[2]:
                    k.objectUri = t[0]
                elif '#definition' in t[1]:
                    k.definitie = t[2]
                elif '#prefLabel' in t[1]:
                    k.label = t[2]
            else:
                if '#Concept' in t[2]:
                    if not t[0] in k.keuzelijstWaardes:
                        kw = KeuzelijstWaarde()
                        kw.objectUri = t[0]
                        k.keuzelijstWaardes[t[0]] = kw
                elif '#definition' in t[1]:
                    k.keuzelijstWaardes[t[0]].definitie = t[2]
                elif '#prefLabel' in t[1]:
                    k.keuzelijstWaardes[t[0]].label = t[2]
                elif '#notation' in t[1]:
                    k.keuzelijstWaardes[t[0]].invulwaarde = t[2]
        return k

    @classmethod
    def load_ttl_file(cls, filepath: str = ''):
        g = rdflib.Graph()
        g.parse(filepath, format="turtle")

        lijst = sorted(g, key=lambda t: (t[0], t[1]))
        lijst = list(map(lambda x: (str(x[0]), str(x[1]), str(x[2])), lijst))

        return lijst
