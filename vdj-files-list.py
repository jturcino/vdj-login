#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--projectfile', dest = 'projectfile', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile', dest = 'jobfile', default = '', nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    # cache and query
    projects_cache = './.vdjprojects'

    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    uuid = vdjpy.get_uuid(args.project, my_agave)
    if uuid is None:
        sys.exit()
    uuid = str(uuid)

    # -l (for listMetadata)
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)
    kwargs['limit'] = args.limit

    # -o (for listMetadata)
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # set filetype to None; replace with projectFile or projectJobFile if -f or -j specified
    filetype = None
    if args.projectfile is not '':
	filetype = 'projectFile'
    elif args.jobfile is not '':
	filetype = 'projectJobFile'

    # get files for metadata
    files = vdjpy.get_project_files(uuid, filetype, kwargs, my_agave)


    # filter to one file if name specified; quit if file not found
    if args.projectfile is not None and filetype == 'projectFile':
	files = vdjpy.get_file_metadata(files, args.projectfile)
    elif args.jobfile is not None and filetype == 'projectJobFile':
	files = vdjpy.get_file_metadata(files, args.jobfile)
    if files is None:
	sys.exit()

    # if -v or specific file given
    if args.verbose is True or type(files) is not list:
        print json.dumps(files, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v and files is a list
    else:
        for item in files:
            print item['value']['name']
