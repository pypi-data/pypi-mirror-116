# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

import os

from hplrv.rendering import TemplateRenderer

###############################################################################
# Constants
###############################################################################

KEY = 'haros_plugin_hplrv'

EMPTY_DICT = {}

# Python 2/3 compatible
if not hasattr(__builtins__, 'basestring'): basestring = (str, bytes)


################################################################################
# Plugin Entry Point
################################################################################

def package_analysis(iface, pkg):
    if not pkg.nodes:
        iface.log_debug('package {} has no nodes'.format(pkg.name))
        return
    r = TemplateRenderer()
    for node in pkg.nodes:
        if not _has_parsed_properties(node):
            iface.log_debug(
                '"{}" has no parsed properties'.format(node.node_name))
            continue
        topics = _get_node_topics(node)
        try:
            iface.log_debug('{}\n{}'.format(node.hpl_properties, topics))
            code = r.render_rospy_node(node.hpl_properties, topics)
            filename = node.node_name.replace('/', '.') + '.rv.py'
            with open(filename, 'w') as f:
                f.write(code)
            mode = os.stat(filename).st_mode
            mode |= (mode & 0o444) >> 2
            os.chmod(filename, mode)
            iface.export_file(filename)
        except Exception as e:
            iface.log_error(e)


def configuration_analysis(iface, config):
    if not _has_parsed_properties(config):
        iface.log_debug('"{}" has no parsed properties'.format(config.name))
        return
    settings = config.user_attributes.get(KEY, EMPTY_DICT)
    _validate_settings(iface, settings)
    topics = _get_config_topics(config)
    try:
        r = TemplateRenderer()
        code = r.render_rospy_node(config.hpl_properties, topics)
        filename = config.name + '.rv.py'
        with open(filename, 'w') as f:
            f.write(code)
        iface.export_file(filename)
    except Exception as e:
        iface.log_error(repr(e))


################################################################################
# Helper Functions
################################################################################

def _validate_settings(iface, settings):
    pass

def _get_node_topics(node):
    topics = {}
    for call in node.advertise + node.subscribe:
        name = call.full_name
        rostype = call.rostype or ''
        if not '/' in rostype:
            continue
        topics[name] = rostype
    return topics

def _get_config_topics(config):
    topics = {}
    for topic in config.topics:
        name = topic.rosname.full
        rostype = topic.type
        if '?' in name or '?' in rostype:
            continue
        topics[name] = rostype
    return topics

def _has_parsed_properties(target):
    for p in target.hpl_properties:
        if not isinstance(p, basestring):
            return True
    return False
