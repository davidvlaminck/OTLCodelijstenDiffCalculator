import os

from GitHubDownloader import GitHubDownloader
from KeuzeLijstCreator import KeuzelijstCreator


class KeuzelijstDiffCalculator:
    def __init__(self, branches_dict: dict):
        if 'prd' not in branches_dict:
            raise ValueError('branches dict should have a prd key')
        if len(branches_dict) < 2:
            raise ValueError('branches dict should contain at least 2 branches')
        self.branches_dict = branches_dict
        self.keuzelijsten = {}

    def download_lists(self):
        GitHubDownloader.download_all_branches(self.branches_dict)
        pass

    def convert_branches_to_keuzelijsten(self):
        for branch in self.branches_dict:
            self.keuzelijsten[branch] = {}
            for file in os.listdir(branch + '/codelijsten'):
                kl = KeuzelijstCreator.read_ttl_file_and_create_keuzelijst(branch + '/codelijsten/' + file)
                self.keuzelijsten[branch][kl.objectUri] = kl

        pass

    def calculate_differences(self):
        differences = []
        other_envs = list(self.branches_dict.keys())
        other_envs.remove('prd')

        for prdkeyKeuzelijst in self.keuzelijsten['prd']:
            for env in other_envs:
                if prdkeyKeuzelijst not in self.keuzelijsten[env]:
                    differences.append([f'{env} ontbreekt een keuzelijst', prdkeyKeuzelijst])
                    continue

                if self.keuzelijsten['prd'][prdkeyKeuzelijst].label != self.keuzelijsten[env][prdkeyKeuzelijst].label:
                    differences.append([f'prd en {env} keuzelijst verschillen van label', prdkeyKeuzelijst, self.keuzelijsten['prd'][prdkeyKeuzelijst].label, self.keuzelijsten[env][prdkeyKeuzelijst].label])

                if self.keuzelijsten['prd'][prdkeyKeuzelijst].definitie != self.keuzelijsten[env][prdkeyKeuzelijst].definitie:
                    differences.append([f'prd en {env} keuzelijst verschillen van definitie', prdkeyKeuzelijst, self.keuzelijsten['prd'][prdkeyKeuzelijst].definitie, self.keuzelijsten[env][prdkeyKeuzelijst].definitie])

                for waardeUri in self.keuzelijsten['prd'][prdkeyKeuzelijst].keuzelijstWaardes:
                    if waardeUri not in self.keuzelijsten[env][prdkeyKeuzelijst].keuzelijstWaardes:
                        differences.append([f'{env} ontbreekt een waarde in keuzelijst', prdkeyKeuzelijst, waardeUri])
                    else:
                        klWaardePrd = self.keuzelijsten['prd'][prdkeyKeuzelijst].keuzelijstWaardes[waardeUri]
                        klWaardeEnv = self.keuzelijsten[env][prdkeyKeuzelijst].keuzelijstWaardes[waardeUri]

                        if klWaardePrd.invulwaarde != klWaardeEnv.invulwaarde:
                            differences.append([f'prd en {env} keuzelijstwaarde verschillen van notatie',
                                                prdkeyKeuzelijst, waardeUri, klWaardePrd.invulwaarde, klWaardeEnv.invulwaarde])

                        if klWaardePrd.label != klWaardeEnv.label:
                            differences.append([f'prd en {env} keuzelijstwaarde verschillen van label',
                                                prdkeyKeuzelijst, waardeUri, klWaardePrd.label, klWaardeEnv.label])

                        if klWaardePrd.definitie != klWaardeEnv.definitie:
                            differences.append([f'prd en {env} keuzelijstwaarde verschillen van definitie',
                                                prdkeyKeuzelijst, waardeUri, klWaardePrd.definitie, klWaardeEnv.definitie])

        for env in other_envs:
            for envkeyKeuzelijst in self.keuzelijsten[env].keys():
                if envkeyKeuzelijst not in self.keuzelijsten['prd']:
                    differences.append(['prd ontbreekt een keuzelijst', envkeyKeuzelijst])
                    continue
                for waardeUri in self.keuzelijsten[env][envkeyKeuzelijst].keuzelijstWaardes:
                    if waardeUri not in self.keuzelijsten['prd'][envkeyKeuzelijst].keuzelijstWaardes:
                        differences.append(['prd ontbreekt een waarde in keuzelijst', envkeyKeuzelijst, waardeUri])

        return differences
