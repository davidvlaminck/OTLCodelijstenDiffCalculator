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
        self.temp_dir_path = ''

    def download_lists(self, temp_dir_path: str=''):
        if temp_dir_path != '':
            self.temp_dir_path = temp_dir_path + '\\'
        GitHubDownloader.download_all_branches(self.branches_dict, temp_dir=self.temp_dir_path)

    def convert_branches_to_keuzelijsten(self):
        for branch in self.branches_dict:
            self.keuzelijsten[branch] = {}
            for file in os.listdir(self.temp_dir_path + branch + '/codelijsten'):
                kl = KeuzelijstCreator.read_ttl_file_and_create_keuzelijst(self.temp_dir_path + branch + '/codelijsten/' + file)
                self.keuzelijsten[branch][kl.objectUri.replace('-test', '')] = kl

    def calculate_differences(self):
        differences = []
        other_envs = list(self.branches_dict.keys())
        other_envs.remove('prd')

        for prdkeyKeuzelijst in self.keuzelijsten['prd']:
            for env in other_envs:
                if prdkeyKeuzelijst not in self.keuzelijsten[env]:
                    differences.append([env, f'prd heeft een keuzelijst die niet bestaat op {env}', prdkeyKeuzelijst])
                    continue

                if self.keuzelijsten['prd'][prdkeyKeuzelijst].label != self.keuzelijsten[env][prdkeyKeuzelijst].label:
                    differences.append([env, f'prd en {env} keuzelijst verschillen van label', prdkeyKeuzelijst, '', self.keuzelijsten['prd'][prdkeyKeuzelijst].label, self.keuzelijsten[env][prdkeyKeuzelijst].label])

                if self.keuzelijsten['prd'][prdkeyKeuzelijst].definitie != self.keuzelijsten[env][prdkeyKeuzelijst].definitie:
                    differences.append([env, f'prd en {env} keuzelijst verschillen van definitie', prdkeyKeuzelijst, '', self.keuzelijsten['prd'][prdkeyKeuzelijst].definitie, self.keuzelijsten[env][prdkeyKeuzelijst].definitie])

                for waardeUri in self.keuzelijsten['prd'][prdkeyKeuzelijst].keuzelijstWaardes:
                    if waardeUri not in self.keuzelijsten[env][prdkeyKeuzelijst].keuzelijstWaardes:
                        differences.append([env, f'prd heeft een waarde in een keuzelijst die niet bestaat op {env}', prdkeyKeuzelijst, waardeUri])
                    else:
                        klWaardePrd = self.keuzelijsten['prd'][prdkeyKeuzelijst].keuzelijstWaardes[waardeUri]
                        klWaardeEnv = self.keuzelijsten[env][prdkeyKeuzelijst].keuzelijstWaardes[waardeUri]

                        if klWaardePrd.invulwaarde != klWaardeEnv.invulwaarde:
                            differences.append([env, f'prd en {env} keuzelijstwaarde verschillen van notatie',
                                                prdkeyKeuzelijst, waardeUri, klWaardePrd.invulwaarde, klWaardeEnv.invulwaarde])

                        if klWaardePrd.label != klWaardeEnv.label:
                            differences.append([env, f'prd en {env} keuzelijstwaarde verschillen van label',
                                                prdkeyKeuzelijst, waardeUri, klWaardePrd.label, klWaardeEnv.label])

                        if klWaardePrd.definitie != klWaardeEnv.definitie:
                            differences.append([env, f'prd en {env} keuzelijstwaarde verschillen van definitie',
                                                prdkeyKeuzelijst, waardeUri, klWaardePrd.definitie, klWaardeEnv.definitie])

        for env in other_envs:
            for envkeyKeuzelijst in self.keuzelijsten[env].keys():
                if envkeyKeuzelijst not in self.keuzelijsten['prd']:
                    differences.append([env, f'prd ontbreekt een keuzelijst t.o.v. {env}', envkeyKeuzelijst])
                    continue
                for waardeUri in self.keuzelijsten[env][envkeyKeuzelijst].keuzelijstWaardes:
                    if waardeUri not in self.keuzelijsten['prd'][envkeyKeuzelijst].keuzelijstWaardes:
                        differences.append([env, f'prd ontbreekt een waarde in keuzelijst t.o.v. {env}', envkeyKeuzelijst, waardeUri])

        return differences
