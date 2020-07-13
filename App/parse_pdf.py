import pdfminer
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams


class Doc:
    """A class that uses Font-Size, Case to classify pdf data"""

    def __init__(self, filename):
        self.filename = filename
        self.outfile = 'outfile.html'
        self.font_sizes = defaultdict(lambda: 0)
        self.nodes = []
        self.__font_size = None

        self.pdf2html()

        self.output = ' '.join(filename.split('/')[-1].split('.')[:-1]) + '.txt'
        self.spans = BeautifulSoup(open(self.outfile, encoding='utf-8'), 'html.parser').find_all('span')

        self.generate_nodes(self.spans)

        os.remove(self.outfile)

    def show_spans(self):
        return '\n'.join([s.text for s in self.spans])

    def pdf2html(self):
        infile = open(self.filename, 'rb')
        outfile = open(self.outfile, 'wb')
        laparams = LAParams(
            word_margin=0.1,
            char_margin=2.0,
            line_margin=0.5,
            boxes_flow=0.5
        )
        extract_text_to_fp(
            infile,
            outfile,
            output_type='html',
            codec='utf-8',
            laparams=laparams,
            maxpages=30,
        )
        infile.close()
        outfile.close()

    def generate_nodes(self, spans):
        _style = ''
        _node_text = ''

        # for each node
        __text = ''
        __style = ''

        def add_node():
            _style_ = defaultdict(lambda: '')
            for attr, val in [tuple(style_.split(':')) for style_ in _style.split(';') if len(style_.split(':')) is 2]:
                _style_[attr.strip()] = val.strip()

            __key_ = _style_['font-size']
            if __key_:
                self.font_sizes[__key_] = self.font_sizes[__key_] + len(_node_text)
                self.nodes.append(Node(_node_text, _style_))

        for span in spans:
            __text = span.text
            __style = span.attrs['style'].strip()

            if __style != _style:
                add_node()
                _node_text = ''
                _style = __style
            __text = [sent for sent in __text.strip().split('\n')]
            __text_ = ''
            for line in __text:
                if re.findall(r'[.?!]', line.strip()[-2:]):
                    __text_ += line.strip() + '\n'
                else:
                    __text_ += line.strip() + ' '

            _node_text += __text_
        add_node()

    def parse_nodes(self):
        """Special Props Ignored.... For Now"""

        def pixel_to_int(pixel):
            return int(re.findall(r'[0-9]+', pixel)[0])

        outfile = open(self.output, mode='wt', encoding='utf-8')
        normal_font = pixel_to_int(sorted(list(self.font_sizes.items()), key=lambda x: x[1])[-1][0])
        __last_op_vip = False
        for node in self.nodes:
            __font_size_ = pixel_to_int(node.attributes['font-size'])
            if __font_size_ > normal_font and node.vip_case():
                outfile.write('' if __last_op_vip else '\n' + node.text.upper() + '\n')
                __last_op_vip = True
            else:
                outfile.write(' ' + node.text.strip() + '\n')

        outfile.close()


class Node:
    def __init__(self, text, styles):
        self.text = text
        self.attributes = styles

    def vip_case(self):
        _txt = self.text.strip()

        def vip():
            return not bool(re.findall(r'[.!?]', _txt[-1])) and bool(re.findall(r'[0-9A-Z]', _txt[0]))

        def is_title():
            for word in _txt.split():
                if word[0].islower():
                    return False
            return True

        return _txt.isupper() or is_title() or vip()
