#!/usr/bin/env python3

import sys, os, re
from docutils import nodes, utils
from docutils.parsers.rst.directives import images
from docutils.transforms import TransformError, Transform, parts
from docutils.parsers.rst import Directive, directives, states, roles
from docutils.writers.html4css1 import HTMLTranslator

import PIL


class video(nodes.General, nodes.Inline, nodes.Element): pass
class media(nodes.General, nodes.Inline, nodes.Element): pass
class figref(nodes.Inline, nodes.TextElement): pass


# --- Figure references -------------------------------------------------------
#
# This class solves pending figure references throughout the whole document
#
# TODO: Use "section.subsection.number" format.
class FigureReferences(Transform):
    default_priority = 260
    def apply(self):
        num = 0
        numbers = {}

        for node in self.document.traverse(nodes.figure):
            if node['label'] is not None:
                num += 1
                node['number'] = num
                numbers[node['label']] = num
            else:
                node['number'] = None

        for node in self.document.traverse(figref):
            if node['target'] not in numbers:
                continue
            num = '(%d)' % numbers[node['target']]
            node[0] = nodes.Text(num, num)

# --- video directive ---------------------------------------------------------
#
# Video inclusion
#
class Video(images.Image):
    """ Video inclusion """
    def align(argument):
        return directives.choice(argument, images.Image.align_h_values)
    option_spec = {'autoplay': directives.flag,
                   'loop': directives.flag,
                   'controls': directives.flag,
                   'height': directives.length_or_unitless,
                   'width': directives.length_or_percentage_or_unitless,
                   'align': align,
                   'class': directives.class_option}
    def run(self):
        old_image_node = nodes.image
        nodes.image = video
        node = images.Image.run(self)
        nodes.image = old_image_node
        return node
directives.register_directive('video', Video)

# --- media directive ---------------------------------------------------------
#
# Video or image (based on uri extension)
#
class Media(Video,images.Image):
    ''' Media inclusion '''
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = images.Image.option_spec.copy()
    option_spec.update(Video.option_spec.copy())
    def run(self):
        uri = directives.uri(self.arguments[0])
        if uri.split('.')[-1] in ['ogg', 'mpg', 'mp4', 'avi', 'mpeg', 'webm']:
            return Video.run(self)
        else:
            return images.Image.run(self)
directives.register_directive('media', Media)

# --- figure directive --------------------------------------------------------
#
# figure redefinition to include image or movie inside
#
class Figure(Media):
    """ Figure with caption """
    def align(argument):
        return directives.choice(argument, directives.images.Image.align_h_values)
    def figwidth_value(argument):
        if argument.lower() == 'image':
            return 'image'
        else:
            return directives.length_or_percentage_or_unitless(argument, 'px')
    option_spec = Media.option_spec.copy()
    option_spec['label'] = directives.unchanged_required
    option_spec['figwidth'] = figwidth_value
    option_spec['figclass'] = directives.class_option
    option_spec['align'] = align
    has_content = True
    def run(self):
        figwidth = self.options.pop('figwidth', None)
        figclasses = self.options.pop('figclass', ["right"])
        align = self.options.pop('align', None)
        (media_node,) = Media.run(self)
        if isinstance(media_node, nodes.system_message):
            return [media_node]
        figure_node = nodes.figure('', media_node)
        if figwidth == 'image':
            if PIL and self.state.document.settings.file_insertion_enabled:
                # PIL doesn't like Unicode paths:
                try:
                    i = PIL.open(str(media_node['uri']))
                except (IOError, UnicodeError):
                    pass
                else:
                    self.state.document.settings.record_dependencies.add(
                        media_node['uri'])
                    figure_node['width'] = i.size[0]
        elif figwidth is not None:
            figure_node['width'] = figwidth
        if figclasses:
            figure_node['classes'] += figclasses
        if align:
            figure_node['align'] = align
        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if isinstance(first_node, nodes.paragraph):
                caption = nodes.caption(first_node.rawsource, '',
                                        *first_node.children)
                figure_node += caption
            elif not (isinstance(first_node, nodes.comment)
                      and len(first_node) == 0):
                error = self.state_machine.reporter.error(
                      'Figure caption must be a paragraph or empty comment.',
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                return [figure_node, error]
            if len(node) > 1:
                figure_node += nodes.legend('', *node[1:])
        node = figure_node

        node['label'] = self.options.get('label', None)
        if not node['label']:
            node['label'] = self.options.get('uri')
        node['number'] = None
        ret = [node]
        if node['label']:
            key = node['label']
            tnode = nodes.target('', '', ids=['figure-' + node['label']])
            self.state.document.note_explicit_target(tnode)
            ret.insert(0, tnode)
        return ret
directives.register_directive('figure', Figure)


# --- fig role ----------------------------------------------------------------
#
# `fig` role allows to refer to a figure identified by a label
#
def fig_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    node = figref('(?)', '(?)', target=text)
    pending = nodes.pending(FigureReferences)
    inliner.document.note_pending(pending)
    return [node], []
fig_role.content = True
roles.register_canonical_role('fig', fig_role)


# --- html figref --------------------------------------------------------------
def html_visit_figref(self, node):
    self.body.append('<a href="#figure-%s">' % node['target'])
def html_depart_figref(self, node):
    self.body.append('</a>')
HTMLTranslator.visit_figref = html_visit_figref
HTMLTranslator.depart_figref = html_depart_figref

# --- html video --------------------------------------------------------------
def html_visit_video(self, node):
    atts = {}
    if 'controls' in node:
        atts['controls'] = True
    if 'loop' in node:
        atts['loop'] = True
    if 'autoplay' in node:
        atts['autoplay'] = True
    if 'width' in node:
        atts['width'] = node['width']
    if 'height' in node:
        atts['height'] = node['height']
    style = []
    for att_name in 'width', 'height':
        if att_name in atts:
            if re.match(r'^[0-9.]+$', atts[att_name]):
                # Interpret unitless values as pixels.
                atts[att_name] += 'px'
            style.append('%s: %s;' % (att_name, atts[att_name]))
            del atts[att_name]
    if style:
        atts['style'] = ' '.join(style)
    if (isinstance(node.parent, nodes.TextElement) or
        (isinstance(node.parent, nodes.reference) and
         not isinstance(node.parent.parent, nodes.TextElement))):
        # Inline context or surrounded by <a>...</a>.
        suffix = ''
    else:
        suffix = '\n'
    if 'classes' in node and 'align-center' in node['classes']:
        node['align'] = 'center'
    if 'align' in node:
        if node['align'] == 'center':
            # "align" attribute is set in surrounding "div" element.
            self.body.append('<div align="center" class="align-center">')
            self.context.append('</div>\n')
            suffix = ''
        else:
            # "align" attribute is set in "img" element.
            atts['align'] = node['align']
            self.context.append('')
        atts['class'] = 'align-%s' % node['align']
    else:
        self.context.append('')
    self.body.append(self.starttag(node, 'video', suffix, **atts))
    for filename in node['uri'].split(','):
        self.body.append(self.starttag(node, 'source', '', **{'src' : filename}))
        self.body.append('</source>\n')

def html_depart_video(self, node):
    self.body.append('</video>\n')
    self.body.append(self.context.pop())

HTMLTranslator.visit_video = html_visit_video
HTMLTranslator.depart_video = html_depart_video



from docutils.core import publish_cmdline, default_description
description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)
publish_cmdline(writer_name='html', description=description)
