import os
from icoextract import IconExtractor, IconExtractorError


def extract_icon_path(executable_path):
    try:
        extractor = IconExtractor(executable_path)
        icon_file = os.path.join(os.path.dirname(executable_path), "icon.ico")
        extractor.export_icon(icon_file, num=0)
        return icon_file
    except IconExtractorError:
        print("No icons available, or the resource is malformed")
        pass
