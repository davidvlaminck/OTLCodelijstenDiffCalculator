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

    def download_lists(self, temp_dir_path: str = ''):
        if temp_dir_path != '':
            self.temp_dir_path = temp_dir_path + '/'
        GitHubDownloader.download_all_branches(self.branches_dict, temp_dir=self.temp_dir_path)

    def convert_branches_to_keuzelijsten(self):
        for branch in self.branches_dict:
            self.keuzelijsten[branch] = {}
            for file in os.listdir(self.temp_dir_path + branch + '/codelijsten'):
                kl = KeuzelijstCreator.read_ttl_file_and_create_keuzelijst(
                    self.temp_dir_path + branch + '/codelijsten/' + file, env=branch)
                self.keuzelijsten[branch][kl.objectUri.replace('-test', '')] = kl

    def calculate_differences(self, kl_eigenaar_dict):
        k_uris = []
        for branch in self.branches_dict:
            k_uris.extend(self.keuzelijsten[branch].keys())

        k_uris = sorted(set(k_uris))


        records = [['keuzelijst', 'keuzelijstwaarde', 'PRD', 'TEI', 'AIM', 'verschillen?', 'SPOC', 'Thema',
                    'opmerkingen (persistent)', 'vrije opmerkingen (persistent)']]
        for keuzelijst_uri in k_uris:

            if 'KlAardingskabelSectie' in keuzelijst_uri:
                pass

            current_spoc = ''
            current_thema = ''
            record = [keuzelijst_uri, '{keuzelijst zelf}']
            keuzelijstwaardes_over_alle_omgevingen = []
            for branch in self.branches_dict:
                if keuzelijst_uri not in self.keuzelijsten[branch]:
                    record.append('')
                else:
                    keuzelijst_instance = self.keuzelijsten[branch][keuzelijst_uri]
                    if current_spoc == '' and keuzelijst_instance.label in kl_eigenaar_dict:
                        current_spoc, current_thema = kl_eigenaar_dict[keuzelijst_instance.label]
                    keuzelijstwaardes_over_alle_omgevingen.extend(keuzelijst_instance.keuzelijst_waardes.keys())
                    if keuzelijst_instance.status == '' or keuzelijst_instance.status is None:
                        record.append('status niet ingevuld')
                    else:
                        record.append(keuzelijst_instance.status)

            self.calculate_change_needed(record)

            record.append(current_spoc)
            record.append(current_thema)
            record.append('')  # persistent column 1
            record.append('')  # persistent column 2

            records.append(record)

            for keuzelijstwaarde in sorted(set(keuzelijstwaardes_over_alle_omgevingen)):
                record = [keuzelijst_uri, keuzelijstwaarde]
                for branch in self.branches_dict:
                    if keuzelijst_uri not in self.keuzelijsten[branch]:
                        record.append('')
                    elif keuzelijstwaarde not in self.keuzelijsten[branch][keuzelijst_uri].keuzelijst_waardes:
                        record.append('')
                    else:
                        kl_object = self.keuzelijsten[branch][keuzelijst_uri].keuzelijst_waardes[keuzelijstwaarde]
                        if kl_object.status == '' or kl_object.status is None:
                            record.append('status niet ingevuld')
                        else:
                            record.append(kl_object.status)

                self.calculate_change_needed(record)

                record.append(current_spoc)
                record.append(current_thema)
                record.append('')  # persistent column 1
                record.append('')  # persistent column 2

                records.append(record)

        return records

    @staticmethod
    def calculate_change_needed(record):
        statussen = set(record[-3:])
        if 'status niet ingevuld' in statussen:
            statussen.add('ingebruik')
            statussen.remove('status niet ingevuld')
        if len(statussen) > 1:
            record.append('ja')
        else:
            record.append('nee')

    def update_differences_with_persistent_data(self, differences, existing_data):
        persistent_data = list(filter(lambda x: len(x) > 8, existing_data))
        for persistent_row in persistent_data:
            i = self.find_difference_row_index(differences, persistent_row[0], persistent_row[1])
            if i == -1:
                continue
            diff_row = differences[i]
            if len(persistent_row) >= 9:
                diff_row[8] = persistent_row[8]
            if len(persistent_row) >= 10:
                diff_row[9] = persistent_row[9]

            differences[i] = diff_row

        return differences

    def find_difference_row_index(self, differences, param1, param2):
        for i, row in enumerate(differences):
            if row[0] == param1 and row[1] == param2:
                return i
        return -1
