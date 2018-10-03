# -*- coding: utf-8 -*-

import argparse
import os

from ge.bpmc.utilities.profiling import reflect

mapping = {
    'api': {
        'root': 'ge.bpmc.app.apis',
        'opts': {
            'public': 'PublicApi',
            'storage': 'StorageApi',
            'available': 'AvailableApi',
            'crud': 'CRUDApi'
        }
    },
    'worker': {
        'root': 'ge.bpmc.app.workers',
        'opts': {
            'processing': 'ProcessingWorker',
            'periodic': 'PeriodicWorker',
            'matching': 'MatchingWorker'
        }
    },
    'beater': {
        'root': 'ge.bpmc.app.beaters',
        'opts': {
            'periodic': 'PeriodicBeater'
        }
    }
}

TYPES = mapping.keys()


def get_opts():
    opts = []
    for key in TYPES:
        opts.append('%(key)s:[%(options)s]' % ({
            'key': key,
            'options': ','.join(mapping[key]['opts'].keys()),
        }))
    return ', '.join(opts)


def get_parser():
    parser = argparse.ArgumentParser()
    type_help = (
        'The type of application you want to launch, can be:' +
        ' %s' % (','.join(TYPES)))
    parser.add_argument(
        'type', type=str, choices=TYPES, help=type_help)
    opt_help = 'Options available:%(linesep)s %(opts)s' % ({
        'linesep': os.linesep,
        'opts': get_opts()})
    parser.add_argument('opt', type=str,
                        help=opt_help)
    config_help = (
        """Path to configuration file,
        see docs/app/config.cfg.example"""
    )
    parser.add_argument(
        'config', type=str,
        help=config_help)
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    type_ = args.type
    if args.opt not in mapping[type_]['opts']:
        print(('%(file)s error: argument type: invalid choice: %(choice)s ' +
              'choose from %(choices)s') % ({
                'file': __file__,
                'choice': args.opt,
                'choices': ', '.join(
                    ['\'%s\'' % x for x in mapping[type_]['opts']])
              }))
    application = reflect('%s.%s' % (
        mapping[type_]['root'], mapping[type_]['opts'][args.opt]))
    application(args.config)
