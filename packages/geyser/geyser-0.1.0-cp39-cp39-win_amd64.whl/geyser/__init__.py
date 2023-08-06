__version__ = '0.1.0'
__all__ = [
    'Geyser'
]

import argparse
from io import FileIO
from typing import Text, Callable
from pathlib import Path
from sys import path as sys_path
from inspect import signature, Parameter

from _geysercpp import *


class Geyser:
    _core = Core()

    @classmethod
    def version(cls) -> Text:
        return __version__

    @classmethod
    def core_build(cls) -> Text:
        return cls._core.compiler

    @classmethod
    def _register_class(cls, name: Text, clazz: type, auto_compose: bool):
        name = clazz.__name__ if name is None else name
        if auto_compose:
            new_dict = {}
            new_dict.update(clazz.__dict__)
            new_dict['__init__'] = Composable.__dict__['__init__']
            clazz = type(name, (Composable,), new_dict)
        return cls._core.register_class(name, clazz)

    @classmethod
    def _build_executable(cls, name: Text, func: Callable):
        name = ''.join(map(
            lambda it: it.capitalize(),
            func.__name__.split('_'),
        )) if name is None else name
        clazz = type(name, (Composable,), {
            '__call__': func,
            '__module__': func.__module__,
            '__init__': Composable.__init__,
        })
        return clazz

    @classmethod
    def _parse_profile(cls, format, fp) -> dict:
        if format == 'json':
            import json
            return json.load(fp)
        elif format == 'yaml':
            from ruamel import yaml
            return yaml.load(fp, yaml.SafeLoader)
        elif format == 'toml':
            import toml
            return toml.load(fp)
        else:
            raise ValueError('Unsupported format of profile')

    @classmethod
    def composable(cls, clazz=None, name: Text = None, auto_compose: bool = True, **kwargs):
        if clazz is None:
            def wrapper(clz):
                cls._register_class(name, clz, auto_compose)
                return clz

            return wrapper
        else:
            new_clazz = cls._safe_init_class(clazz)
            cls._register_class(name, new_clazz, False)

    @classmethod
    def _safe_init_class(cls, clazz):
        def safe_init(self, *args, **kwargs):
            in_args = kwargs.pop('__args__') if '__args__' in kwargs else []
            params = signature(clazz).parameters
            args_slot = None

            missing = []
            undefined = []

            for key, param in params.items():
                if param.kind == Parameter.POSITIONAL_OR_KEYWORD or param.kind == Parameter.KEYWORD_ONLY:
                    if param.name not in kwargs and param.name is Parameter.empty:
                        missing.append(param)
                elif param.kind == Parameter.POSITIONAL_ONLY:
                    if args_slot is None:
                        args_slot = []
                    args_slot.append(param)
                elif param.kind == Parameter.VAR_POSITIONAL:
                    args_slot = param

            for key, value in kwargs.items():
                if key not in params.keys():
                    undefined.append(key)

            for key, value in params.items():
                if value.kind == Parameter.VAR_KEYWORD:
                    undefined.clear()

            fill_args, fill_kwargs = [], {}

            if isinstance(args_slot, list) and len(args_slot) != len(in_args):
                raise ValueError(f'{len(args_slot)} argument(s) are/is needed, input {len(in_args)} argument(s).')
            else:
                fill_args.extend(in_args)

            if len(missing) > 0:
                missing_names = list(map(
                    lambda param: param.name,
                    missing
                ))
                raise ValueError(f'Argument(s) named {", ".join(missing_names)} is/are missing.')
            if len(undefined) > 0:
                fill_kwargs.update(filter(
                    lambda it: it[0] not in undefined,
                    kwargs.items()
                ))
            else:
                fill_kwargs.update(kwargs.items())
            clazz.__init__(self, *fill_args, **fill_kwargs)

        new_clazz = type(clazz.__name__, (clazz,), {
            '__init__': safe_init,
            '__module__': clazz.__module__
        })
        return new_clazz

    @classmethod
    def executable(cls, function=None, name: Text = None, **kwargs):
        if function is None:
            def wrapper(func):
                clz = cls._build_executable(name, func)
                cls._register_class(clz.__name__, clz, False)
                return clz

            return wrapper
        else:
            clz = cls._build_executable(name, function)
            cls._register_class(clz.__name__, clz, False)

    @classmethod
    def access(cls, reference: Text) -> type:
        return cls._core[reference]

    @classmethod
    def entry(cls):
        sys_path.append(str(Path('.').absolute()))
        parser = argparse.ArgumentParser(
            'geyser', description='Geyser: compose & execute python objects.'
        )
        parser.add_argument(
            'profile',
            nargs=1,
            type=argparse.FileType('r', encoding='utf8'),
            help='compose this profile'
        )
        parser.add_argument('-v', '--version', action='version', version=f'{__version__}')
        ns = parser.parse_args()
        if len(ns.profile) > 0:
            profile_file: FileIO = ns.profile[0]
            format_name = profile_file.readline().strip('\r\n #/')
            profile = cls._parse_profile(format_name, profile_file)
            compose = profile['__compose__']
            for key, value in compose.items():
                cls._core.compose(key, compose)
            execute = profile['__execute__']
            cls._core.execute(execute)

    @classmethod
    def object_count(cls):
        return cls._core.object_count

    @classmethod
    def class_count(cls):
        return cls._core.class_count

    @classmethod
    def references(cls):
        return cls._core.references


class Composable:
    def __init__(self, *args, **kwargs):
        for key, item in kwargs.items():
            setattr(self, key, item)

    def __mod__(self, item) -> bool:
        return hasattr(self, item)

    def __bool__(self) -> bool:
        return hasattr(self, '__call__')
