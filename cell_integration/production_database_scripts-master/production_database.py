import json
import logging
import os
import time
from os.path import isdir
from os.path import isfile
from os.path import join
from glob import glob
import coloredlogs
import tqdm
import itk_pdb.dbAccess as dbAccess


EXISTING_COMPONENT_MODE = 'skip'  # 'skip', 'delete'


class serialNumberDuplicity(Exception):
    pass


class unassociatedStageWithTestType(Exception):
    pass


class componentTypeDaoGetByCodeFailed(Exception):
    pass


class DBAuthenticationError(Exception):
    pass


class NotDeletedError(Exception):
    pass


class FailedToRegisterError(Exception):
    pass


class SkipWafer(Exception):
    pass


class unknownDBAccessError(Exception):
    pass


class WPUploader(object):
    '''
    Main class for uploading the ITkPix wafer probing results to the production database.
    '''

    DB_BASE_URL = "https://itkpd-test.unicorncollege.cz/"

    def __init__(self, existing_component_mode='skip', debug=False, create_tmp_files=False, tmp_dir='output', tokens=None):
        '''
            Waferprobing data uploader to ITk production database
            ----------
            Parameters:
                existing_component_mode: 'skip' or 'delete'
                    What to do if an already existing component is encountered?
                    'skip' -> If a wafer already exists, the whole wafer upload process is skipped. If a chip of a wafer already exists, this chip is skipped.
                    'delete' -> Try to delete and reupload the already existing object. Only works if it is your object, still associated with your institution and not yet assembled.

                debug: bool
                    Print debug messages.

                create_tmp_files: bool
                    Save uploaded json data to files.

                tmp_dir: str
                    Where to create tmp files.
        '''
        # self.ITkPDSession = dbAccess.ITkPDSession()
        if tokens is None:
            self.access_code1 = os.getenv('TOKEN1')
            self.access_code2 = os.getenv('TOKEN2')
        else:
            self.access_code1 = tokens[0]
            self.access_code2 = tokens[1]
        self.token = dbAccess.authenticate(accessCode1=self.access_code1, accessCode2=self.access_code2)
        self.existing_component_mode = existing_component_mode
        self.create_tmp_files = create_tmp_files
        self.tmp_dir = tmp_dir
        if self.create_tmp_files:
            if not isdir(tmp_dir):
                os.mkdir(tmp_dir)

        loglevel = logging.DEBUG if debug else logging.INFO

        fmt = '%(asctime)s - [%(name)-15s] - %(levelname)-7s %(message)s'
        self.log = logging.getLogger('WPUploader')
        self.log.setLevel(loglevel)
        coloredlogs.install(fmt=fmt, milliseconds=False, loglevel=loglevel)
        self.fh = logging.FileHandler(time.strftime("%Y%m%d_%H%M%S") + '_waferprobing_upload.log')
        self.fh.setLevel(loglevel)
        self.fh.setFormatter(logging.Formatter(fmt))
        self.log.addHandler(self.fh)

        self.log.info('Waferprobing Uploader started...')

        self.log.debug('existing_component_mode = {}'.format(self.existing_component_mode))
        if self.existing_component_mode not in ['skip', 'delete']:
            raise AttributeError("Invalid existing_component_mode '{}'. Must be 'skip' or 'delete'.".format(self.existing_component_mode))
        if self.existing_component_mode == 'delete':
            self.log.warning("CAUTION! existing_component_mode 'delete' will delete and reupload existing objects!")
            time.sleep(3)

        self.reset()

    def reset(self):
        self.wafer_data = {}
        self.chip_data = {}

        self.data_dir = None
        self.wafer_no = None
        self.wafer_sn_itk = None
        self.wafer_sn_tsmc = None
        self.institute = None
        self.wafer_type = None
        self.wafer_tmp_dir = None

        # self.db_client = itkdb.Client()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log.removeHandler(self.fh)

    def _access_db(self, action, data, method, attachments=None, url=None):
        # action, data = None, url = None, method = None, attachments = None
        '''
            Wrapping itkdb.Client.get/post for uniform error handling
        '''

        self.token = dbAccess.authenticate(accessCode1=self.access_code1, accessCode2=self.access_code2)

        if url is None:
            baseName = self.DB_BASE_URL
        else:
            baseName = url

        baseName += action

        if attachments is not None:
            # No encoding of data, as this is passed as k,v pairs
            headers = {"Authorization": "Bearer %s" % self.token}
            return dbAccess.doMultiSomething(baseName, paramdata=data,
                                             headers=headers,
                                             method=method, attachments=attachments)

        if data is not None:
            if type(data) is bytes:
                reqData = data
            else:
                reqData = dbAccess.to_bytes(json.dumps(data))
            if url is None:  # Default
                pass  # print("data is: ", reqData)
        else:
            reqData = None

        headers = {'Content-Type': 'application/json'}
        headers.update({"Accept-Encoding": "gzip, deflate"})
        # Header, token
        if self.token is not None:
            headers["Authorization"] = "Bearer %s" % self.token
        # print("baseName", baseName)
        # print("reqData", reqData)
        # print("headers", headers)
        # print("method", method)

        # for _ in range(10):
        #     try:
        result = dbAccess.doRequest(baseName, data=reqData, headers=headers, method=method)
        #     break
        # except Exception as e:
        #     print(e)
        #     time.sleep(1)
        #     result = e
        time.sleep(0.5)
        return result

    def load_data(self, data_dir):
        self.reset()
        self.data_dir = data_dir
        for f in os.listdir(data_dir):
            full_f = join(data_dir, f)
            if isfile(full_f) and '_probing_results.json' in f:
                try:
                    wafer_no = int(f.split('_')[1])
                except Exception as e:
                    self.log.warning(e)
                    wafer_no = int(f.split('_')[1], 16)
                with open(full_f) as jf:
                    data = json.load(jf)
                break
        else:
            raise RuntimeError('No input JSON file found!')

        self.wafer_no = wafer_no
        self.wafer_sn_itk = '20UPGFW{0:07d}'.format(wafer_no)
        self.wafer_sn_tsmc = data['Wafer_ID']
        self.institute = data['institution']
        self._set_wafer_type()

        self.wafer_tmp_dir = join(self.tmp_dir, 'output_{}'.format(self.wafer_no))
        if self.create_tmp_files:
            if not isdir(self.wafer_tmp_dir):
                os.mkdir(self.wafer_tmp_dir)

        self._make_chip_jsons(data)
        self._make_summary_json(data)

    def _set_wafer_type(self):
        # SN convention might change in the future
        waferhex = format(self.wafer_no, '#05x')
        if waferhex[2] == '0':
            self.wafer_type = 'RD53A'
        elif waferhex[2] == '1':
            self.wafer_type = 'ITKPIX_V11'
        else:
            raise AttributeError('Cannot determine wafer type!')

    def _make_chip_jsons(self, data):
        for chip_sn, chip_data in data['chips'].items():
            chip_sn_itk = '20UPGFC{0:07d}'.format(int(chip_sn, 16))

            chip_json = {}
            chip_json['component'] = chip_sn_itk
            chip_json.update(chip_data)

            try:
                del chip_json['comment']
                comment = chip_data['comment']
                chip_json['comments'] = [comment]
                if 'short' in comment:
                    defect_name = 'short'
                    failuremode = 1
                else:
                    defect_name = 'other'
                    failuremode = 3
                chip_json['defects'] = [{'name': defect_name, 'description': comment, 'properties': {'failuremode': failuremode}}]
            except KeyError:
                pass

            self.chip_data[chip_sn_itk] = chip_json

            if self.create_tmp_files:
                chip_file = join(self.wafer_tmp_dir, '{}.json'.format(chip_sn_itk))
                with open(chip_file, 'w') as cf:
                    json.dump(chip_json, cf, indent=4)

    def _make_summary_json(self, data):
        summary_data = {'component': self.wafer_sn_itk, 'testType': 'WAFER_PROBING'}
        summary_data['institution'] = data['institution']
        summary_data['runNumber'] = data['runNumber']
        summary_data['date'] = data['date']
        summary_data['passed'] = 'true'
        summary_data['problems'] = 'false'
        summary_data['results'] = {'WAFER_YIELD': data['yield'] / 100}

        self.wafer_data = summary_data

        if self.create_tmp_files:
            summary_file = join(self.wafer_tmp_dir, 'summary.json')
            with open(summary_file, 'w') as sf:
                json.dump(summary_data, sf, indent=4)

    def _delete_component(self, itk_sn):
        self.log.warning('Deleting component {}'.format(itk_sn))

        # Safety checks:
        ret = self._access_db(action='getComponent', method='GET', data={'component': itk_sn})

        if ret['assembled']:    # Only delete components that are not assembled yet
            raise NotDeletedError('Component {} is already assembled!'.format(itk_sn))

        if ret['currentStage']['order'] > 2 or ret['currentStage']['order'] == 6:    # Only delete components in stage 1 or 2 (before or after wafer probing)
            raise NotDeletedError('Component {0} is already in test stage {1}!'.format(itk_sn, ret['currentStage']['order']))

        if ret['institution']['code'] != self.wafer_data['institution']:    # Only delete components that belong to your institution
            raise NotDeletedError('Component {0} does not belong to your institution ({1}), but to {2}!'.format(itk_sn, self.wafer_data['institution'], ret['institution']['code']))

        # if ret['user']['userIdentity'] != self.db_client.user.identity:  # Only delete components that belong to you
        #     raise NotDeletedError('Component {0} does not belong to you, but to user {1}!'.format(itk_sn, ret['user']))

        self._access_db(action='deleteComponent', method='POST', data={'component': itk_sn})
        self.log.debug('Successfully deletec component {}'.format(itk_sn))

    def delete_wafer(self, wafer_id):
        list_json = self._access_db(action="getComponent", method="GET", data={"component": wafer_id})
        chiplist = []
        chipsubstring = '20UPGFC'
        for child in list_json["children"]:
            if child["component"]:
                chipsn = child["component"]["serialNumber"]
                if chipsubstring in chipsn:
                    try:
                        self._delete_component(chipsn)
                    except Exception as e:
                        print("no such chip", chipsn)
                        print(e)
                    chiplist.append(chipsn)
        self._delete_component(wafer_id)
        return chiplist

    def register_wafer(self):
        self.log.info('Registering wafer {}...'.format(self.wafer_no))
        hex_wafer_id = hex(self.wafer_no).upper().replace('X', 'x')
        post_data = {'serialNumber': self.wafer_sn_itk,
                     'componentType': 'FE_WAFER',
                     'type': self.wafer_type,
                     'project': 'P',
                     'subproject': 'PG',
                     'institution': self.institute,
                     'properties': {'ID': self.wafer_sn_tsmc,
                                    'RAW_DATA_LINK': 'https://itkpix.web.cern.ch/' + hex_wafer_id}}

        self.log.debug('post data for registerComponent: {}'.format(post_data))
        try:
            ret = self._access_db(action='registerComponent', method='POST', data=post_data)
            component_code = ret['component']['code']
            self.log.info('Registered wafer with SN {0} as component code {1}'.format(self.wafer_sn_itk, component_code))
            self.log.info('View at {0}componentView?code={1}'.format(self.DB_BASE_URL, component_code))
            return component_code
        except dbAccess.dbAccessError as e:
            print("hi", e)
            if self.existing_component_mode == 'skip':
                self.log.error('Wafer with SN {} already exists! Skipping...'.format(self.wafer_sn_itk))
                # raise SkipWafer()
                return 0
            elif self.existing_component_mode == 'delete':
                self.log.warning('Wafer with SN {} already exists! Deleting...'.format(self.wafer_sn_itk))
                for _ in range(10):
                    try:
                        self.delete_wafer(self.wafer_sn_itk)
                        break
                    except Exception as e:
                        self.log.warning(e)
                        time.sleep(1)
                ret = self._access_db(action='registerComponent', method='POST', data=post_data)
                component_code = ret['component']['code']
                self.log.info('Registered wafer with SN {0} as component code {1}'.format(self.wafer_sn_itk, component_code))
                self.log.info('View at {0}componentView?code={1}'.format(self.DB_BASE_URL, component_code))
                return component_code

    def register_chips(self):
        self.log.info('Registering chips...')
        self.log.info('Accessing DB to get wafer children IDs...')
        ret = self._access_db(action='getComponent', method='GET', data={'component': self.wafer_sn_itk})
        chip_slots = [c['id'] for c in ret['children']]

        self.log.info('Found {0} chip slots for wafer {1}.'.format(len(chip_slots), self.wafer_sn_itk))
        if len(chip_slots) != len(self.chip_data):
            raise AttributeError('Number of chips ({0}) does not match available chip slots ({1})!')

        self.log.info('Start registering {} chips...'.format(len(self.chip_data)))
        registered_chips, chips_failed_to_register = [], []
        pbar = tqdm.tqdm(total=len(chip_slots), unit='chips')
        for i, (chip_sn_itk, chip_json) in enumerate(self.chip_data.items()):
            fin_color = chip_json['results']['OVERALL_RESULT']
            post_data = {'serialNumber': chip_sn_itk,
                         'componentType': 'FE_CHIP',
                         'type': self.wafer_type,
                         'project': 'P',
                         # 'stage': 'HYBRIDISATION',
                         'subproject': 'PG',
                         'institution': self.institute}
            if fin_color == 'yellow':
                post_data['flag'] = 'YELLOW_AT_TESTINGONWAFER'
            elif fin_color == 'red':
                post_data['flag'] = 'BAD_AT_TESTINGONWAFER'
            self.log.debug('post data for registerComponent: {}'.format(post_data))

            try:
                self._access_db(action='registerComponent', method='POST', data=post_data)
            except Exception:
                if self.existing_component_mode == 'skip':
                    self.log.error('Chip with SN {} already exists! Igoring...'.format(chip_sn_itk))
                    chips_failed_to_register.append(chip_sn_itk)
                    continue
                elif self.existing_component_mode == 'delete':
                    self.log.warning('Chip with SN {} already exists! Deleting...'.format(chip_sn_itk))
                    for n in range(10):
                        try:
                            self._delete_component(chip_sn_itk)
                            break
                        except Exception as e:
                            self.log.warning(e)
                            time.sleep(1)
                    for n in range(10):
                        try:
                            self._access_db(action='registerComponent', method='POST', data=post_data)
                            break
                        except Exception as e:
                            self.log.warning(e)
                            time.sleep(1)
            post_data = {'parent': self.wafer_sn_itk,
                         'slot': chip_slots[i],
                         'child': chip_sn_itk}
            for n in range(10):
                try:
                    self._access_db(action='assembleComponentBySlot', method='POST', data=post_data)
                    break
                except Exception as e:
                    self.log.warning(e)
                    time.sleep(1)
            registered_chips.append(chip_sn_itk)
            pbar.update(1)

        pbar.close()
        self.log.info('Sucessfully registered {0} chips.'.format(len(registered_chips)))
        if len(chips_failed_to_register) != 0:
            self.log.error('Failed to register data for {0} chips: {1}'.format(len(chips_failed_to_register), chips_failed_to_register))

        return registered_chips, chips_failed_to_register

    def upload_wafer(self):
        self.log.info('Uploading wafer result...')
        try:
            ret = self._access_db(action='uploadTestRunResults', method='POST', data=self.wafer_data)
            test_id = ret['testRun']['id']
        except unassociatedStageWithTestType:
            self.log.error('Wafer with SN {} is in wrong test stage!'.format(self.wafer_sn_itk))

        self.log.debug('Creating wafer attachment...')
        summary_pdf = join(self.data_dir, 'wafer_summary_0x{0:X}.pdf'.format(self.wafer_no))
        print("hoho", summary_pdf)
        if not isfile(summary_pdf):
            raise FileNotFoundError('Summary pdf file not found at {}'.format(summary_pdf))
        meta_data = {'testRun': test_id,
                     'title': 'wafer plots',
                     'description': 'Plotted results from chip on wafer test',
                     'type': 'file'}
        self.log.debug('Meta data for attachment upload: {}'.format(meta_data))
        self._access_db(action='createTestRunAttachment', method='POST', data=meta_data, attachments={'data': open(summary_pdf, 'rb')})

        summary_xlsx = join(self.data_dir, 'wafer_summary_0x{0:X}.xlsx'.format(self.wafer_no))
        if not isfile(summary_xlsx):
            raise FileNotFoundError('Summary xlsx file not found at {}'.format(summary_xlsx))
        meta_data = {'testRun': test_id,
                     'title': 'wafer summary',
                     'description': 'Summary of results from chip on wafer test',
                     'type': 'file'}
        self.log.debug('Meta data for attachment upload: {}'.format(meta_data))
        self._access_db(action='createTestRunAttachment', method='POST', data=meta_data, attachments={'data': open(summary_xlsx, 'rb')})

        summary_xlsx = glob(join(self.data_dir, 'wafer_map_*.pdf'))[0]
        if not isfile(summary_xlsx):
            raise FileNotFoundError('Vendor Map file not found at {}'.format(summary_xlsx))
        meta_data = {'testRun': test_id,
                     'title': 'vendor map',
                     'description': 'Wafer Map with just the final results',
                     'type': 'file'}
        self.log.debug('Vendor Map for attachment upload: {}'.format(meta_data))
        self._access_db(action='createTestRunAttachment', method='POST', data=meta_data, attachments={'data': open(summary_xlsx, 'rb')})

        summary_xlsx = glob(join(self.data_dir, '*' + summary_xlsx[-10:-4] + '*.xlsx'))[0]
        if not isfile(summary_xlsx):
            raise FileNotFoundError('Vendor summary file not found at {}'.format(summary_xlsx))
        meta_data = {'testRun': test_id,
                     'title': 'vendor summary',
                     'description': 'Summary of just the final results from chip on wafer test',
                     'type': 'file'}
        self.log.debug('Vendor summary for attachment upload: {}'.format(meta_data))
        self._access_db(action='createTestRunAttachment', method='POST', data=meta_data, attachments={'data': open(summary_xlsx, 'rb')})

        self.log.info('Global wafer data upload complete.')

    def upload_chips(self):
        self.log.info('Uploading chip results...')
        uploaded_chips, chips_failed_to_upload = [], []
        pbar = tqdm.tqdm(total=len(self.chip_data), unit='chips')
        for chip_sn_itk, data in self.chip_data.items():
            chip_sn_rd53 = '0x' + hex(int(chip_sn_itk[-7:]))[2:].upper()

            self.log.debug('Uploading test results for chip {0} ({1})...'.format(chip_sn_itk, chip_sn_rd53))
            for _ in range(10):
                try:
                    try:
                        ret = self._access_db(action='uploadTestRunResults', method='POST', data=data)
                        test_id = ret['testRun']['id']
                        break
                    except unassociatedStageWithTestType:
                        self.log.error('Chip with SN {} is in wrong test stage!'.format(chip_sn_itk))
                        chips_failed_to_upload.append(chip_sn_itk)
                        continue
                except Exception as e:
                    self.log.warning(e)

            iv_curve_pdf_meta_data = {'testRun': test_id,
                                      'title': 'Regulator IV curve',
                                      'description': 'Regulator IV curves from chip on wafer test',
                                      'type': 'file'}
            chip_json = self._access_db(action="getComponent", method="GET", data={"component": chip_sn_itk})
            chipcode = chip_json['code']
            if data['results']['OVERALL_RESULT'] != "green":
                self._access_db(action="setComponentStage", method="POST", data={"component": chip_sn_itk, "stage": "UNUSABLE"})
                flag = "BAD_AT_TESTINGONWAFER"
                if data['results']['OVERALL_RESULT'] == "yellow":
                    flag = "YELLOW_AT_TESTINGONWAFER"
                self._access_db(action="addComponentFlag", method="POST", data={"component": chipcode, "flag": flag})

            self.log.debug('Meta data for attachment upload: {}'.format(iv_curve_pdf_meta_data))
            iv_curve_pdf = join(self.data_dir, 'db_attachments', '{}_iv.pdf'.format(chip_sn_rd53))
            if isfile(iv_curve_pdf):
                self._access_db(action='createTestRunAttachment', method='POST', data=iv_curve_pdf_meta_data, attachments={'data': open(iv_curve_pdf, 'rb')})
                self.log.debug('Successfully uploaded IV curve pdf file for chip {0} ({1})'.format(chip_sn_itk, chip_sn_rd53))
            else:
                self.log.warning('IV curves PDF file for chip {0} ({1}) does not exist.'.format(chip_sn_itk, chip_sn_rd53))

            uploaded_chips.append(chip_sn_itk)
            pbar.update(1)
            self.log.debug('Data for chip {0} ({1}) uploaded to testRunID {2}.'.format(chip_sn_itk, chip_sn_rd53, test_id))

        pbar.close()
        self.log.info('Sucessfully uploaded {0} chips.'.format(len(uploaded_chips)))
        if len(chips_failed_to_upload) != 0:
            self.log.error('Failed to upload data for {0} chips: {1}'.format(len(chips_failed_to_upload), chips_failed_to_upload))

    def run(self):
        try:
            self.register_wafer()
        except SkipWafer:
            return

        self.register_chips()

        self.upload_wafer()
        self.upload_chips()


if __name__ == '__main__':
    DATA_DIR = 'path to the folder where all analyzed data files are stored e.g. /wp_analysis/0x???/'
    with WPUploader(existing_component_mode=EXISTING_COMPONENT_MODE) as uploader:
        uploader.load_data(DATA_DIR)
        uploader.run()
