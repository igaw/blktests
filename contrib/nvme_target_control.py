#!/usr/bin/env python3

import argparse
import subprocess
from jinja2 import Environment, FileSystemLoader


nvmetcli='/home/wagi/work/nvmetcli/nvmetcli'
remote='http://nvmet:5000'


def gen_conf(conf):
	environment = Environment(loader=FileSystemLoader('.'))
	template = environment.get_template('nvmet-subsys.jinja2')
	filename = f'{conf["subsysnqn"]}.json'
	content = template.render(conf)
	with open(filename, mode='w', encoding='utf-8') as outfile:
		outfile.write(content)


def target_setup(args):
	conf = {
		'subsysnqn': args.subsysnqn,
		'subsys_uuid': args.subsys_uuid,
		'hostnqn': args.hostnqn,
		'allowed_hosts': args.hostnqn,
		'ctrlkey': args.ctrlkey,
		'hostkey': args.hostkey,
		'blkdev': '/dev/vdc'
	}

	gen_conf(conf)

	subprocess.call(['python3', nvmetcli, '--remote=' + remote,
					 'restore', args.subsysnqn + '.json'])


def target_cleanup(args):
	subprocess.call(['python3', nvmetcli, '--remote=' + remote,
					 'clear', args.subsysnqn + '.json'])


def build_parser():
	parser = argparse.ArgumentParser()
	sub = parser.add_subparsers(required=True)

	setup = sub.add_parser('setup')
	setup.add_argument('--subsysnqn', required=True)
	setup.add_argument('--subsys-uuid', required=True)
	setup.add_argument('--hostnqn', required=True)
	setup.add_argument('--ctrlkey', default='')
	setup.add_argument('--hostkey', default='')
	setup.set_defaults(func=target_setup)

	cleanup = sub.add_parser('cleanup')
	cleanup.add_argument('--subsysnqn', required=True)
	cleanup.set_defaults(func=target_cleanup)

	return parser


def test():
	import pdb

	pdb.set_trace()

	parser = build_parser()
	args = parser.parse_args('setup --subsysnqn blktests-subsystem-1 --subsys-uuid 91fdba0d-f87b-4c25-b80f-db7be1418b9e --blkdev=/dev/vdb'.split())
	args.func(args)


def main():
	import sys

	parser = build_parser()
	args = parser.parse_args()
	args.func(args)


if __name__ == '__main__':
	main()
