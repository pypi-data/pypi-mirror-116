#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
import jinja2
import sys
import toml
import json
import yaml
import io
import re
import os

if sys.version > '3':
    PY3 = True
    import configparser
else:
    PY3 = False
    from io import open
    import ConfigParser as configparser

class Conf(object):
    _conf_file = []

    @classmethod
    def add_conf(cls, conf):
        if os.path.isfile(conf):
            cls._conf_file.append(conf)
        elif os.path.isdir(conf):
            for i in os.listdir(conf):
                if re.match(r'.*\.(yaml|yml)', i):
                    cls._conf_file.append(os.path.join(conf, i))

    @classmethod
    def init(cls):
        setattr(cls, 'all_property', {})
        conf_dict = {}
        for c in cls._conf_file:
            if os.path.exists(c):
                conf_dict.update(yaml.load(open(c), Loader=yaml.Loader))
        for k, v in conf_dict.items():
            setattr(cls, k, v)
            cls.all_property[k] = v

    @classmethod
    def reset(cls):
        cls._conf_file = []
        cls.all_property = {}

    @classmethod
    def reload(cls, conf_file):
        cls._conf_file = []
        cls.all_property = {}
        cls.add_conf(conf_file)
        cls.init()

    @classmethod
    def debug(cls):
        return cls._conf_file


def fill_config_util(template_path, target, data, default_key=True):
    """渲染模板

        Args:
            template_path: 配置文件模板
            target: 目标文件
            data: 数据（字典）
            default_key: 是否处理默认参数
        Returns:
            None
        """
    FillConfig.load_template(template_path).generate_config(target, data, default_key)


class FillConfig:

    def __init__(self, template_path):
        self.template_path = template_path
        self.loader = FileSystemLoader(template_path)
        self.template_env = Environment(loader=self.loader, undefined=jinja2.StrictUndefined)
        self.format = ('json', 'toml', 'yaml', 'ini')
        self.template_env.filters['regex_replace'] = self._regex_replace

    def _regex_replace(self, s, find, replace):
        return re.sub(find, replace, s)

    @classmethod
    def load_template(cls, template_path):
        return FillConfig(template_path)

    def list_templates(self):
        """获取模板

        Args:
            None
        Returns:
            list
        """
        return self.loader.list_templates()

    def _dir_generate_config(self, target_path, data):
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        template_names = self.list_templates()
        for template_name in template_names:
            target_file_path = os.path.join(target_path, template_name)
            template = self.template_env.get_template(template_name)
            content = template.render(data)
            with open(target_file_path, "w", encoding='UTF-8') as f:
                r, t = self.check_format(content)
                if r:
                    f.write(content)

    def _file_generate_config(self, target_file_path, data):
        content = self.template_env.get_template('').render(data)
        if not os.path.exists(os.path.dirname(target_file_path)):
            os.makedirs(os.path.dirname(target_file_path))
        with open(target_file_path, "w", encoding='UTF-8') as f:
            f.write(content)

    def _default_key_handler(self, data, separator='Defaule'):
        return DefaultKeyHandler(data).fill_config_dict()

    def generate_config(self, target_file, data, config_has_default_key=False):
        """生成模板

        Args:
            template_name: 模板名称
            target_file: 目标文件
        Returns:
            None
        """
        if config_has_default_key:
            data = self._default_key_handler(data)

        if os.path.isdir(self.template_path):
            if os.path.isdir(target_file) or not os.path.exists(target_file):
                self._dir_generate_config(target_file, data)
            else:
                return
        elif os.path.isfile(self.template_path):
            if os.path.exists(target_file) and os.path.isdir(target_file):
                return
            self._file_generate_config(target_file, data)

    def _load_test(self, content, format):
        try:
            if format == 'yaml':
                yaml.load(content)
            elif format == 'ini':
                conf = configparser.ConfigParser()
                if PY3 is False:
                    conf.readfp(io.StringIO(content))
                else:
                    conf.read_string(content)
            elif format == 'json':
                c = re.sub(r'''/\*.*\*/.*''', '', content)
                json.loads(c)
            elif format == 'toml':
                toml.loads(content)
        except Exception:
            return False
        return True

    def check_format(self, content):
        for fm in self.format:
            if self._load_test(content, fm):
                return True, fm
        return False, None


class DefaultKeyHandler(object):

    def __init__(self, config_has_default_key, key_separator='Default'):
        self.config = config_has_default_key
        self.key_separator = key_separator

    def get_default_key(self, separator='Default'):
        """获取默认值

        Args:
            config: 配置文件列表
            split: 分隔符
        Returns:
            list
        """
        return list(filter(lambda x: x if re.search(separator, x) else None, self.config.keys()))

    def fill_config_dict(self):
        default_keys = self.get_default_key()

        for default_key in default_keys:
            default_key_prefix = default_key.split(self.key_separator)[0]
            other_keys = self.get_default_key(default_key_prefix)
            for key in self.config[default_key]:
                for other_key in other_keys:
                    if self.config[other_key] is None:
                        self.config[other_key] = {}
                    if key not in self.config[other_key]:
                        self.config[other_key][key] = self.config[default_key][key]
        return self.config
