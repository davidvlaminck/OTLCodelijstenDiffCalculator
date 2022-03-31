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


        prdkeylist = self.keuzelijsten['prd'].keys()
        for prdkeyKeuzelijst in prdkeylist:
            for waardeUri in self.keuzelijsten['prd'][prdkeyKeuzelijst].keuzelijstWaardes:
                if waardeUri not in self.keuzelijsten['aim'][prdkeyKeuzelijst].keuzelijstWaardes:
                    differences.append(['aim ontbreekt volgende waarde', prdkeyKeuzelijst, waardeUri])

        return differences




