# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

import pytest

from antsibull_docs.markup import dom
from antsibull_docs.markup.parser import parse, CommandParser, Context, Parser


TEST_PARSE_DATA: t.List[t.Tuple[t.Union[str, t.List[str]], Context, t.Dict[str, t.Any], t.List[dom.Paragraph]]] = [
    ('', Context(), {}, []),
    ([''], Context(), {}, [[]]),
    ('test', Context(), {}, [[dom.TextPart(text='test')]]),
    ('test', Context(), {}, [[dom.TextPart(text='test')]]),
    # classic markup:
    (
        'foo I(bar) baz C( bam ) B( ( boo ) ) U(https://example.com/?foo=bar)HORIZONTALLINE L(foo ,  https://bar.com) R( a , b )M(foo.bar.baz)HORIZONTALLINEx M(foo.bar.baz.bam)',
        Context(),
        {},
        [
            [
                dom.TextPart(text='foo '),
                dom.ItalicPart(text='bar'),
                dom.TextPart(text=' baz '),
                dom.CodePart(text=' bam '),
                dom.TextPart(text=' '),
                dom.BoldPart(text=' ( boo '),
                dom.TextPart(text=' ) '),
                dom.URLPart(url='https://example.com/?foo=bar'),
                dom.HorizontalLinePart(),
                dom.TextPart(text=' '),
                dom.LinkPart(text='foo', url='https://bar.com'),
                dom.TextPart(text=' '),
                dom.RSTRefPart(text=' a', ref='b '),
                dom.ModulePart(fqcn='foo.bar.baz'),
                dom.TextPart(text='HORIZONTALLINEx '),
                dom.ModulePart(fqcn='foo.bar.baz.bam'),
            ],
        ],
    ),
    (
        'foo I(bar) baz C( bam ) B( ( boo ) ) U(https://example.com/?foo=bar)HORIZONTALLINE L(foo ,  https://bar.com) R( a , b )M(foo.bar.baz)HORIZONTALLINEx M(foo.bar.baz.bam)',
        Context(),
        dict(only_classic_markup=True),
        [
            [
                dom.TextPart(text='foo '),
                dom.ItalicPart(text='bar'),
                dom.TextPart(text=' baz '),
                dom.CodePart(text=' bam '),
                dom.TextPart(text=' '),
                dom.BoldPart(text=' ( boo '),
                dom.TextPart(text=' ) '),
                dom.URLPart(url='https://example.com/?foo=bar'),
                dom.HorizontalLinePart(),
                dom.TextPart(text=' '),
                dom.LinkPart(text='foo', url='https://bar.com'),
                dom.TextPart(text=' '),
                dom.RSTRefPart(text=' a', ref='b '),
                dom.ModulePart(fqcn='foo.bar.baz'),
                dom.TextPart(text='HORIZONTALLINEx '),
                dom.ModulePart(fqcn='foo.bar.baz.bam'),
            ],
        ],
    ),
    # semantic markup:
    (
        'foo E(a\\),b) P(foo.bar.baz#bam) baz V( b\\,\\na\\)\\\\m\\, ) O(foo) ',
        Context(),
        {},
        [
            [
                dom.TextPart(text='foo '),
                dom.EnvVariablePart(name='a),b'),
                dom.TextPart(text=' '),
                dom.PluginPart(plugin=dom.PluginIdentifier(fqcn='foo.bar.baz', type='bam')),
                dom.TextPart(text=' baz '),
                dom.OptionValuePart(value=' b,na)\\m, '),
                dom.TextPart(text=' '),
                dom.OptionNamePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value=None),
                dom.TextPart(text=' '),
            ],
        ],
    ),
    # semantic markup option name:
    ('O(foo)', Context(), {}, [
      [
        dom.OptionNamePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('O(ignore:foo)', Context(current_plugin=dom.PluginIdentifier('foo.bar.baz', type='bam')), {}, [
      [
        dom.OptionNamePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('O(foo)', Context(current_plugin=dom.PluginIdentifier('foo.bar.baz', type='bam')), {}, [
      [
        dom.OptionNamePart(plugin=dom.PluginIdentifier('foo.bar.baz', type='bam'), entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('O(foo.bar.baz#bam:foo)', Context(), {}, [
      [
        dom.OptionNamePart(plugin=dom.PluginIdentifier('foo.bar.baz', type='bam'), entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('O(foo=bar)', Context(), {}, [
      [
        dom.OptionNamePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value='bar'),
      ],
    ]),
    ('O(foo.baz=bam)', Context(), {}, [
      [
        dom.OptionNamePart(plugin=None, entrypoint=None, link=['foo', 'baz'], name='foo.baz', value='bam'),
      ],
    ]),
    ('O(foo[1].baz[bam.bar.boing].boo)', Context(), {}, [
      [
        dom.OptionNamePart(plugin=None, entrypoint=None, link=['foo', 'baz', 'boo'], name='foo[1].baz[bam.bar.boing].boo', value=None),
      ],
    ]),
    ('O(bar.baz.bam.boo#lookup:foo[1].baz[bam.bar.boing].boo)', Context(), {}, [
      [
        dom.OptionNamePart(plugin=dom.PluginIdentifier('bar.baz.bam.boo', type='lookup'), entrypoint=None, link=['foo', 'baz', 'boo'], name='foo[1].baz[bam.bar.boing].boo', value=None),
      ],
    ]),
    # semantic markup return value name:
    ('RV(foo)', Context(), {}, [
      [
        dom.ReturnValuePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('RV(ignore:foo)', Context(current_plugin=dom.PluginIdentifier('foo.bar.baz', type='bam')), {}, [
      [
        dom.ReturnValuePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('RV(foo)', Context(current_plugin=dom.PluginIdentifier('foo.bar.baz', type='bam')), {}, [
      [
        dom.ReturnValuePart(plugin=dom.PluginIdentifier('foo.bar.baz', type='bam'), entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('RV(foo.bar.baz#bam:foo)', Context(), {}, [
      [
        dom.ReturnValuePart(plugin=dom.PluginIdentifier('foo.bar.baz', type='bam'), entrypoint=None, link=['foo'], name='foo', value=None),
      ],
    ]),
    ('RV(foo=bar)', Context(), {}, [
      [
        dom.ReturnValuePart(plugin=None, entrypoint=None, link=['foo'], name='foo', value='bar'),
      ],
    ]),
    ('RV(foo.baz=bam)', Context(), {}, [
      [
        dom.ReturnValuePart(plugin=None, entrypoint=None, link=['foo', 'baz'], name='foo.baz', value='bam'),
      ],
    ]),
    ('RV(foo[1].baz[bam.bar.boing].boo)', Context(), {}, [
      [
        dom.ReturnValuePart(plugin=None, entrypoint=None, link=['foo', 'baz', 'boo'], name='foo[1].baz[bam.bar.boing].boo', value=None),
      ],
    ]),
    ('RV(bar.baz.bam.boo#lookup:foo[1].baz[bam.bar.boing].boo)', Context(), {}, [
      [
        dom.ReturnValuePart(plugin=dom.PluginIdentifier('bar.baz.bam.boo', type='lookup'), entrypoint=None, link=['foo', 'baz', 'boo'], name='foo[1].baz[bam.bar.boing].boo', value=None),
      ],
    ]),
    # bad parameter parsing (no escaping, error message):
    ('M(', Context(), {}, [
      [dom.ErrorPart(message='While parsing M() at index 1: Cannot find closing ")" after last parameter')],
    ]),
    ('M(foo', Context(), dict(errors='message'), [
      [dom.ErrorPart(message='While parsing M() at index 1: Cannot find closing ")" after last parameter')],
    ]),
    ('L(foo)', Context(), dict(errors='message'), [
      [
        dom.ErrorPart(message='While parsing L() at index 1: Cannot find comma separating parameter 1 from the next one'),
      ],
    ]),
    ('L(foo,bar', Context(), dict(errors='message'), [
      [dom.ErrorPart(message='While parsing L() at index 1: Cannot find closing ")" after last parameter')],
    ]),
    ('L(foo), bar', Context(), dict(errors='message'), [
      [dom.ErrorPart(message='While parsing L() at index 1: Cannot find closing ")" after last parameter')],
    ]),
    ('P(', Context(), {}, [
      [dom.ErrorPart(message='While parsing P() at index 1: Cannot find closing ")" after last parameter')],
    ]),
    ('P(foo', Context(), dict(errors='message'), [
      [dom.ErrorPart(message='While parsing P() at index 1: Cannot find closing ")" after last parameter')],
    ]),
    # bad module ref (error message):
    ('M(foo)', Context(), {}, [
      [dom.ErrorPart(message='While parsing M() at index 1: Module name "foo" is not a FQCN')],
    ]),
    (' M(foo.bar)', Context(), dict(errors='message'), [
      [
        dom.TextPart(text=' '),
        dom.ErrorPart(message='While parsing M() at index 2: Module name "foo.bar" is not a FQCN'),
      ],
    ]),
    ('  M(foo. bar.baz)', Context(), dict(errors='message'), [
      [
        dom.TextPart(text='  '),
        dom.ErrorPart(message='While parsing M() at index 3: Module name "foo. bar.baz" is not a FQCN'),
      ],
    ]),
    ('   M(foo) baz', Context(), dict(errors='message'), [
      [
        dom.TextPart(text='   '),
        dom.ErrorPart(message='While parsing M() at index 4: Module name "foo" is not a FQCN'),
        dom.TextPart(text=' baz'),
      ],
    ]),
    # bad plugin ref (error message):
    ('P(foo)', Context(), {}, [
      [
        dom.ErrorPart(message='While parsing P() at index 1: Parameter "foo" is not of the form FQCN#type'),
      ],
    ]),
    ('P(f o.b r.b z#bar)', Context(), dict(errors='message'), [
      [
        dom.ErrorPart(message='While parsing P() at index 1: Plugin name "f o.b r.b z" is not a FQCN'),
      ],
    ]),
    ('P(foo.bar.baz#b m)', Context(), dict(errors='message'), [
      [
        dom.ErrorPart(message='While parsing P() at index 1: Plugin type "b m" is not valid'),
      ],
    ]),
    # bad option name/return value (error message):
    ('O(f o.b r.b z#bam:foobar)', Context(), {}, [
      [
        dom.ErrorPart(message='While parsing O() at index 1: Plugin name "f o.b r.b z" is not a FQCN'),
      ],
    ]),
    ('O(foo.bar.baz#b m:foobar)', Context(), dict(errors='message'), [
      [
        dom.ErrorPart(message='While parsing O() at index 1: Plugin type "b m" is not valid'),
      ],
    ]),
    ('O(foo:bar:baz)', Context(), dict(errors='message'), [
      [
        dom.ErrorPart(message='While parsing O() at index 1: Invalid option/return value name "foo:bar:baz"'),
      ],
    ]),
    # bad parameter parsing (no escaping, ignore error):
    ('M(', Context(), dict(errors='ignore'), [[]]),
    ('M(foo', Context(), dict(errors='ignore'), [[]]),
    ('L(foo)', Context(), dict(errors='ignore'), [[]]),
    ('L(foo,bar', Context(), dict(errors='ignore'), [[]]),
    ('L(foo), bar', Context(), dict(errors='ignore'), [[]]),
    ('P(', Context(), dict(errors='ignore'), [[]]),
    ('P(foo', Context(), dict(errors='ignore'), [[]]),
    # bad module ref (ignore error):
    ('M(foo)', Context(), dict(errors='ignore'), [[]]),
    (' M(foo.bar)', Context(), dict(errors='ignore'), [[dom.TextPart(text=' ')]]),
    ('  M(foo. bar.baz)', Context(), dict(errors='ignore'), [[dom.TextPart(text='  ')]]),
    ('   M(foo) baz', Context(), dict(errors='ignore'), [
      [
        dom.TextPart(text='   '),
        dom.TextPart(text=' baz'),
      ],
    ]),
    # bad plugin ref (ignore error):
    ('P(foo#bar)', Context(), dict(errors='ignore'), [[]]),
    ('P(f o.b r.b z#bar)', Context(), dict(errors='ignore'), [[]]),
    ('P(foo.bar.baz#b m)', Context(), dict(errors='ignore'), [[]]),
    # bad option name/return value (ignore error):
    ('O(f o.b r.b z#bam:foobar)', Context(), dict(errors='ignore'), [[]]),
    ('O(foo.bar.baz#b m:foobar)', Context(), dict(errors='ignore'), [[]]),
    ('O(foo:bar:baz)', Context(), dict(errors='ignore'), [[]]),
]


@pytest.mark.parametrize('paragraphs, context, kwargs, expected', TEST_PARSE_DATA)
def test_parse(paragraphs: t.Union[str, t.List[str]], context: Context, kwargs: t.Dict[str, t.Any], expected: t.List[dom.Paragraph]) -> None:
    result = parse(paragraphs, context, **kwargs)
    print(result)
    assert result == expected


TEST_PARSE_THROW_DATA: t.List[t.Tuple[t.Union[str, t.List[str]], Context, t.Dict[str, t.Any], str]] = [
    # bad parameter parsing (no escaping, throw error):
    ('M(', Context(), dict(errors='exception'),
      'While parsing M() at index 1: Cannot find closing ")" after last parameter',
    ),
    ('M(foo', Context(), dict(errors='exception'),
      'While parsing M() at index 1: Cannot find closing ")" after last parameter',
    ),
    ('L(foo)', Context(), dict(errors='exception'),
      'While parsing L() at index 1: Cannot find comma separating parameter 1 from the next one',
    ),
    ('L(foo,bar', Context(), dict(errors='exception'),
      'While parsing L() at index 1: Cannot find closing ")" after last parameter',
    ),
    ('L(foo), bar', Context(), dict(errors='exception'),
      'While parsing L() at index 1: Cannot find closing ")" after last parameter',
    ),
    ('P(', Context(), dict(errors='exception'),
      'While parsing P() at index 1: Cannot find closing ")" after last parameter',
    ),
    ('P(foo', Context(), dict(errors='exception'),
      'While parsing P() at index 1: Cannot find closing ")" after last parameter',
    ),
    # bad module ref (throw error):
    ('M(foo)', Context(), dict(errors='exception'),
      'While parsing M() at index 1: Module name "foo" is not a FQCN',
    ),
    (' M(foo.bar)', Context(), dict(errors='exception'),
      'While parsing M() at index 2: Module name "foo.bar" is not a FQCN',
    ),
    ('  M(foo. bar.baz)', Context(), dict(errors='exception'),
      'While parsing M() at index 3: Module name "foo. bar.baz" is not a FQCN',
    ),
    ('   M(foo)', Context(), dict(errors='exception'),
      'While parsing M() at index 4: Module name "foo" is not a FQCN',
    ),
    # bad plugin ref (throw error):
    ('P(foo)', Context(), dict(errors='exception'),
      'While parsing P() at index 1: Parameter "foo" is not of the form FQCN#type',
    ),
    ('P(f o.b r.b z#bar)', Context(), dict(errors='exception'),
      'While parsing P() at index 1: Plugin name "f o.b r.b z" is not a FQCN',
    ),
    ('P(foo.bar.baz#b m)', Context(), dict(errors='exception'),
      'While parsing P() at index 1: Plugin type "b m" is not valid',
    ),
    # bad option name/return value (throw error):
    ('O(f o.b r.b z#bam:foobar)', Context(), dict(errors='exception'),
      'While parsing O() at index 1: Plugin name "f o.b r.b z" is not a FQCN',
    ),
    ('O(foo.bar.baz#b m:foobar)', Context(), dict(errors='exception'),
      'While parsing O() at index 1: Plugin type "b m" is not valid',
    ),
    ('O(foo:bar:baz)', Context(), dict(errors='exception'),
      'While parsing O() at index 1: Invalid option/return value name "foo:bar:baz"',
    ),
]


@pytest.mark.parametrize('paragraphs, context, kwargs, exc_message', TEST_PARSE_THROW_DATA)
def test_parse_bad(paragraphs: t.Union[str, t.List[str]], context: Context, kwargs: t.Dict[str, t.Any], exc_message: str) -> None:
    with pytest.raises(ValueError) as exc:
        parse(paragraphs, context, **kwargs)
    assert str(exc.value) == exc_message


TEST_TRIVIAL_PARSER = [
    '',
    'foo',
    'I(foo) B(bar) HORIZONTALLINE C(baz)'
]


@pytest.mark.parametrize('input', TEST_TRIVIAL_PARSER)
def test_trivial_parser(input: str) -> None:
    parser = Parser([])
    result = parser.parse_string(input, Context())
    expected = [dom.TextPart(text=input)] if input else []
    assert result == expected
