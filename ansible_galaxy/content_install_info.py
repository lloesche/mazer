import logging
import os

import yaml

import attr

from ansible_galaxy.models.content_install_info import ContentInstallInfo

log = logging.getLogger(__name__)


def load(data_or_file_object):
    log.debug('loading content install info from %s', data_or_file_object)

    info_dict = yaml.safe_load(data_or_file_object)

    log.debug('info_dict: %s', info_dict)
    install_info = ContentInstallInfo(version=info_dict.get('version', None),
                                      install_date=info_dict.get('install_date', None),
                                      install_date_iso=info_dict.get('install_date_iso', None))

    log.debug('install_info: %s', install_info)
    return install_info


def save(install_info, filename):
    log.debug('saving install info to %s', filename)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w+') as f:
        # FIXME: just return the install_info dict (or better, build it elsewhere and pass in)
        # FIXME: stop minging self state
        try:
            install_info_ = yaml.safe_dump(attr.asdict(install_info), f, default_flow_style=False)
        except Exception as e:
            log.warn('unable to serialize .galaxy_install_info to filename=%s for data=%s', filename, install_info_)
            log.exception(e)
            return False

    log.debug('wrote galaxy_install_info to %s', filename)
    return True


