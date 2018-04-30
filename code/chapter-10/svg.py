# -----------------------------------------------------------------------------
# Copyright (c) 2017, Nicolas P. Rougier. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
import re
import bezier
import numpy as np
from lxml import etree
from matplotlib.path import Path

MOVETO = 1
LINETO = 2
CURVE4 = 3
CURVE3 = 4
CLOSE  = 5

def get(filename, name):
    """
    Read a given element from an SVG file
    """
    root = etree.parse(filename).getroot()
    return root.xpath("//*[@id='%s']" % name)[0].get("d")


def path(filename, name):
    """
    Read and convert an SVG path command into a path representation
    """
    path = get(filename, name)
    verts, codes = convert(path)
    verts, codes = tesselate(verts, codes)
    return verts, codes


def convert(path):
    """
    Parse and convert an SVG path command into a path representation

    Parameters
    ----------
    path : string
        A valid SVG path command
    """

    # First we separate tokens inside the path
    tokens = []
    COMMANDS = set('MmZzLlHhVvCcSsQqTtAa')
    COMMAND_RE = re.compile("([MmZzLlHhVvCcSsQqTtAa])")
    FLOAT_RE = re.compile("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")
    for x in COMMAND_RE.split(path):
        if x in COMMANDS:
            tokens.append(x)
        for token in FLOAT_RE.findall(x):
            tokens.append(float(token))

    # Then we process and convert commands
    # (Note that not all commands have been implemented)
    commands = { 'M': [MOVETO, 2],
                 'm': [MOVETO, 2],
                 'L': [LINETO, 2],
                 'l': [LINETO, 2], 
                 # 'V': [Path.LINETO, 1],
                 # 'v': [Path.LINETO, 1],
                 # 'H': [Path.LINETO, 1],
                 # 'h': [Path.LINETO, 1], 
                 'C': [CURVE4, 6],
                 'c': [CURVE4, 6],
                 # 'S': [Path.CURVE4, 4],
                 # 's': [Path.CURVE4, 4],
                 'Q': [CURVE3, 4],
                 'q': [CURVE3, 4],
                 # 'T': [Path.CURVE3, 2],
                 # 't': [Path.CURVE3, 2],
                 # 'A': [None,        7],
                 # 'a': [None,        7],
                 'Z': [CLOSE, 0],
                 'z': [CLOSE, 0] }
    index = 0
    codes, verts = [], []
    last_vertice = np.array([[0, 0]])
    while index < len(tokens):
        # Token is a command
        # (else, we re-use last command because
        #   SVG allows to omit command when it is the same as the last command)
        if isinstance(tokens[index], str):
            last_command = tokens[index]
            code, n = commands[last_command]
            index += 1
        if n > 0:
            vertices = np.array(tokens[index:index+n]).reshape(n//2,2)
            if last_command.islower():
                vertices += last_vertice
            last_vertice = vertices[-1]
            codes.extend([code,]*len(vertices))
            verts.extend(vertices.tolist())
            index += n
        else:
            codes.append(code)
            verts.append(last_vertice.tolist())

        # A 'M/m' follows by several vertices means implicit 'L/l' for
        # subsequent vertices
        if last_command == 'm':
            last_command, code = 'l', LINETO
        elif last_command == 'M':
            last_command, code = 'L', LINETO

    return np.array(verts), codes


def tesselate(verts, codes):
    """
    Tesselate a matplotlib path with the given vertices and codes.

    Parameters
    ----------
    vertices : array_like
        The ``(n, 2)`` float array or sequence of pairs representing the
        vertices of the path.

    codes : array_like
        n-length array integers representing the codes of the path.
    """
    
    tesselated_verts = []
    tesselated_codes = []
    index = 0 
    while index < len(codes):
        if codes[index] in [MOVETO, LINETO]:
            tesselated_codes.append(codes[index])
            tesselated_verts.append(verts[index])
            index += 1
        elif codes[index] == CURVE3:
            p1, p2, p3 = verts[index-1:index+2]
            V = bezier.quadratic(p1,p2,p3)
            C = [LINETO,]*len(V)
            tesselated_codes.extend(C[1:])
            tesselated_verts.extend(V[1:])
            index += 2
        elif codes[index] == CURVE4:
            p1, p2, p3, p4 = verts[index-1:index+3]
            V = bezier.cubic(p1,p2,p3,p4)
            C = [LINETO,]*len(V)
            tesselated_codes.extend(C[1:])
            tesselated_verts.extend(V[1:])
            index += 3
        elif codes[index] == CLOSE:
            index += 1
        else:
            index += 1

    verts = tesselated_verts
    codes = tesselated_codes
    return np.array(verts), codes
