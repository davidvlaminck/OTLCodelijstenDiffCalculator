import unittest

from KeuzeLijstCreator import KeuzelijstCreator, Keuzelijst

expected_rdf_lijst = [(
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer',
                      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2004/02/skos/core#Concept'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer',
                      'http://www.w3.org/2004/02/skos/core#definition', 'Conische paal met afgeronde kop en sierring.'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer',
                      'http://www.w3.org/2004/02/skos/core#inScheme',
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer',
                      'http://www.w3.org/2004/02/skos/core#notation', 'conischeTrottoirpaalAmsterdammer'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer',
                      'http://www.w3.org/2004/02/skos/core#prefLabel', 'conischeTrottoirpaalAmsterdammer'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer',
                      'http://www.w3.org/2004/02/skos/core#topConceptOf',
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/diamantkoppaal',
                      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2004/02/skos/core#Concept'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/diamantkoppaal',
                      'http://www.w3.org/2004/02/skos/core#definition',
                      'Een paal voorzien van een diamantkop en op de hoeken 4 vellingkanten.'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/diamantkoppaal',
                      'http://www.w3.org/2004/02/skos/core#inScheme',
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/diamantkoppaal',
                      'http://www.w3.org/2004/02/skos/core#notation', 'diamantkoppaal'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/diamantkoppaal',
                      'http://www.w3.org/2004/02/skos/core#prefLabel', 'diamantkoppaal'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/diamantkoppaal',
                      'http://www.w3.org/2004/02/skos/core#topConceptOf',
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType',
                      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2004/02/skos/core#ConceptScheme'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType',
                      'http://www.w3.org/2004/02/skos/core#definition', 'De vormen van een anti-parkeerpaal.'), (
                      'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType',
                      'http://www.w3.org/2004/02/skos/core#prefLabel', 'Anti-parkeerpaal type')]


class KeuzelijstCreatorTests(unittest.TestCase):
    def test_load_file_to_list_of_tuples(self):
        lijst = KeuzelijstCreator.load_ttl_file('AntiParkeerpaalType.ttl')

        self.assertListEqual(expected_rdf_lijst, lijst)

    def test_convert_tuples_to_keuzelijst_keuzelijstObject(self):
        keuzelijst = KeuzelijstCreator.convert_tuples_to_keuzelijst(tuples_list=expected_rdf_lijst)
        self.assertTrue(isinstance(keuzelijst, Keuzelijst))
        self.assertEqual('https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/AntiParkeerpaalType', keuzelijst.objectUri)
        self.assertEqual('De vormen van een anti-parkeerpaal.', keuzelijst.definitie)
        self.assertEqual('Anti-parkeerpaal type', keuzelijst.label)

    def test_convert_tuples_to_keuzelijst_keuzelijstWaardes(self):
        keuzelijst = KeuzelijstCreator.convert_tuples_to_keuzelijst(tuples_list=expected_rdf_lijst)
        self.assertEqual(2, len(keuzelijst.keuzelijstWaardes.items()))
        uri = 'https://wegenenverkeer.data.vlaanderen.be/id/concept/AntiParkeerpaalType/conischeTrottoirpaalAmsterdammer'
        self.assertEqual(uri, keuzelijst.keuzelijstWaardes[uri].objectUri)
        self.assertEqual('conischeTrottoirpaalAmsterdammer', keuzelijst.keuzelijstWaardes[uri].notitie)
        self.assertEqual('conischeTrottoirpaalAmsterdammer', keuzelijst.keuzelijstWaardes[uri].label)
        self.assertEqual('Conische paal met afgeronde kop en sierring.', keuzelijst.keuzelijstWaardes[uri].definitie)

