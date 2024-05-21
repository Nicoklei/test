from bdaq53.waferprobing.analysis.ITkPix.production_database import WPUploader, SkipWafer


# choose EXISTING_COMPONENT_MODE from ['skip', 'delete']
def main(wafers, institute, tokens, EXISTING_COMPONENT_MODE='skip'):
    for wafer_sn, wafer_sn_tsmc in wafers.items():
        wafer_no = int(wafer_sn, 16)
        with WPUploader(existing_component_mode=EXISTING_COMPONENT_MODE, tokens=tokens) as uploader:
            print(wafer_no)
            uploader.wafer_no = wafer_no
            uploader.wafer_sn_itk = '20UPGFW{0:07d}'.format(wafer_no)
            uploader.wafer_sn_tsmc = wafer_sn_tsmc
            uploader.wafer_type = 'ITKPIX_V2'
            uploader.institute = institute
            try:
                uploader.register_wafer()
            except SkipWafer:
                return
            # uploader.register_chips()


if __name__ == '__main__':
    wafers = {
                "0x201": "N60V01-02B7",
                "0x202": "N60V01-03B2",
                "0x203": "N60V01-04A5",
                "0x204": "N60V01-05A0",
                "0x205": "N60V01-06G6",
                # "0x206": "N60V01-07G1",
                # "0x207": "N60V01-08F4",
                # "0x208": "N60V01-09E7",
                # "0x209": "N60V01-10F4",
                # "0x20A": "N60V01-11E7",
                # "0x20B": "N60V01-12E2",
                # "0x20C": "N60V01-13D5",
                # "0x20D": "N60V01-14D0",
                # "0x20E": "N60V01-15C3",
                # "0x20F": "N60V01-16B6",
        }
    institute = 'BONN'
    tokens = ['xxxxxxxx', 'xxxxxxxx']
    main(wafers, institute, tokens)
