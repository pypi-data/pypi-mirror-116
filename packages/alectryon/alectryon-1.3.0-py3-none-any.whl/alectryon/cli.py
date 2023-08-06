# Copyright © 2019 Clément Pit-Claudel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import inspect
import os
import os.path
import shutil
import sys

from . import __version__, core

# Pipelines
# =========

def read_plain(_, fpath, fname):
    if fname == "-":
        return sys.stdin.read()
    with open(fpath, encoding="utf-8") as f:
        return f.read()

def read_json(_, fpath, fname):
    from json import load
    if fname == "-":
        return load(sys.stdin)
    with open(fpath, encoding="utf-8") as f:
        return load(f)

def parse_coq_plain(contents, fpath):
    return [core.PosStr(contents, core.Position(fpath, 1, 1), 0)]

def _catch_parsing_errors(fpath, k, *args):
    from .literate import ParsingError
    try:
        return k(*args)
    except ParsingError as e:
        raise ValueError("{}: {}".format(fpath, e)) from e

def coq_to_rst(coq, fpath, point, marker):
    from .literate import coq2rst_marked
    return _catch_parsing_errors(fpath, coq2rst_marked, coq, point, marker)

def rst_to_coq(coq, fpath, point, marker):
    from .literate import rst2coq_marked
    return _catch_parsing_errors(fpath, rst2coq_marked, coq, point, marker)

def annotate_chunks(chunks, fpath, cache_directory, cache_compression, sertop_args):
    from .core import SerAPI, annotate
    from .json import Cache
    metadata = {"sertop_args": sertop_args}
    cache = Cache(cache_directory, fpath, metadata, cache_compression)
    return cache.update(chunks, lambda c: annotate(c, sertop_args), SerAPI.version_info())

def register_docutils(v, ctx):
    from . import docutils

    docutils.AlectryonTransform.SERTOP_ARGS = ctx["sertop_args"]
    docutils.CACHE_DIRECTORY = ctx["cache_directory"]
    docutils.CACHE_COMPRESSION = ctx["cache_compression"]
    docutils.HTML_MINIFICATION = ctx["html_minification"]
    docutils.LONG_LINE_THRESHOLD = ctx["long_line_threshold"]
    docutils.setup()

    # The encoding/decoding dance below happens because setting output_encoding
    # to "unicode" causes reST to generate a bad <meta> tag, and setting
    # input_encoding to "unicode" breaks the ‘.. include’ directive.

    # Setting ``traceback`` unconditionally allows us to catch and report errors
    # from our own docutils components and avoid asking users to make a report
    # to the docutils mailing list.

    ctx["docutils_settings_overrides"] = {
        'traceback': True,
        'stylesheet_path': None,
        'input_encoding': 'utf-8',
        'output_encoding': 'utf-8',
        'alectryon_banner': ctx["include_banner"],
        'alectryon_vernums': ctx["include_vernums"],
        'alectryon_webpage_style': ctx["webpage_style"],
    }

    return v

def _gen_docutils(source, fpath,
                  Parser, Reader, Writer,
                  settings_overrides):
    from docutils.core import publish_string

    parser = Parser()
    return publish_string(
        source=source.encode("utf-8"),
        source_path=fpath, destination_path=None,
        reader=Reader(parser), reader_name=None,
        parser=parser, parser_name=None,
        writer=Writer(), writer_name=None,
        settings_overrides=settings_overrides,
        enable_exit_status=True).decode("utf-8")

def _resolve_dialect(backend, html_dialect, latex_dialect):
    return {"webpage": html_dialect, "latex": latex_dialect}.get(backend, None)

def _record_assets(assets, path, names):
    for name in names:
        assets.append((path, name))

def gen_docutils(src, frontend, backend, fpath, dialect,
                 docutils_settings_overrides, assets):
    from .docutils import get_pipeline

    pipeline = get_pipeline(frontend, backend, dialect)
    _record_assets(assets, pipeline.translator.ASSETS_PATH, pipeline.translator.ASSETS)

    return _gen_docutils(src, fpath,
                         pipeline.parser, pipeline.reader, pipeline.writer,
                         docutils_settings_overrides)

def _docutils_cmdline(description, frontend, backend):
    import locale
    locale.setlocale(locale.LC_ALL, '')

    from docutils.core import publish_cmdline, default_description
    from .docutils import setup, get_pipeline

    setup()

    dialect = _resolve_dialect(backend, "html4", "pdflatex")
    pipeline = get_pipeline(frontend, backend, dialect)
    publish_cmdline(
        parser=pipeline.parser(), writer=pipeline.writer(),
        settings_overrides={'stylesheet_path': None},
        description="{} {}".format(description, default_description)
    )

def lint_docutils(source, fpath, frontend, docutils_settings_overrides):
    from docutils.core import publish_doctree
    from .docutils import get_parser, LintingReader

    parser = get_parser(frontend)()
    reader = LintingReader(parser)

    publish_doctree(
        source=source.encode("utf-8"), source_path=fpath,
        reader=reader, reader_name=None,
        parser=parser, parser_name=None,
        settings_overrides=docutils_settings_overrides,
        enable_exit_status=True)

    return reader.error_stream.getvalue() # FIXME exit code

def _scrub_fname(fname):
    import re
    return re.sub("[^-a-zA-Z0-9]", "-", fname)

def apply_transforms(annotated):
    from .transforms import default_transform
    for fragments in annotated:
        yield default_transform(fragments)

def gen_html_snippets(annotated, fname, html_minification):
    from .html import HtmlGenerator
    from .pygments import highlight_html
    fname = _scrub_fname(fname)
    return HtmlGenerator(highlight_html, fname, html_minification).gen(annotated)

def gen_latex_snippets(annotated):
    from .latex import LatexGenerator
    from .pygments import highlight_latex
    return LatexGenerator(highlight_latex).gen(annotated)

COQDOC_OPTIONS = ['--body-only', '--no-glob', '--no-index', '--no-externals',
                  '-s', '--html', '--stdout', '--utf8']

def _run_coqdoc(coq_snippets, coqdoc_bin=None):
    """Get the output of coqdoc on coq_code."""
    from shutil import rmtree
    from tempfile import mkstemp, mkdtemp
    from subprocess import check_output
    coqdoc_bin = coqdoc_bin or os.path.join(os.getenv("COQBIN", ""), "coqdoc")
    dpath = mkdtemp(prefix="alectryon_coqdoc_")
    fd, filename = mkstemp(prefix="alectryon_coqdoc_", suffix=".v", dir=dpath)
    try:
        for snippet in coq_snippets:
            os.write(fd, snippet.encode("utf-8"))
            os.write(fd, b"\n(* --- *)\n") # Separator to prevent fusing
        os.close(fd)
        coqdoc = [coqdoc_bin, *COQDOC_OPTIONS, "-d", dpath, filename]
        return check_output(coqdoc, cwd=dpath, timeout=10).decode("utf-8")
    finally:
        rmtree(dpath)

def _gen_coqdoc_html(coqdoc_fragments):
    from bs4 import BeautifulSoup
    coqdoc_output = _run_coqdoc(fr.contents for fr in coqdoc_fragments)
    soup = BeautifulSoup(coqdoc_output, "html.parser")
    docs = soup.find_all(class_='doc')
    coqdoc_comments = [c for c in coqdoc_fragments if not c.special]
    if len(docs) != len(coqdoc_comments):
        from pprint import pprint
        print("Coqdoc mismatch:", file=sys.stderr)
        pprint(list(zip(coqdoc_comments, docs)))
        raise AssertionError()
    return docs

def _gen_html_snippets_with_coqdoc(annotated, fname, html_minification):
    from dominate.util import raw
    from .html import HtmlGenerator
    from .pygments import highlight_html
    from .transforms import isolate_coqdoc, default_transform, CoqdocFragment

    fname = _scrub_fname(fname)
    writer = HtmlGenerator(highlight_html, fname, html_minification)

    parts = [part for fragments in annotated
             for part in isolate_coqdoc(fragments)]
    coqdoc = [part for part in parts
              if isinstance(part, CoqdocFragment)]
    coqdoc_html = iter(_gen_coqdoc_html(coqdoc))

    for part in parts:
        if isinstance(part, CoqdocFragment):
            if not part.special:
                yield [raw(str(next(coqdoc_html, None)))]
        else:
            fragments = default_transform(part.fragments)
            yield writer.gen_fragments(fragments)

def gen_html_snippets_with_coqdoc(annotated, html_classes, fname, html_minification):
    html_classes.append("coqdoc")
    # ‘return’ instead of ‘yield from’ to update html_classes eagerly
    return _gen_html_snippets_with_coqdoc(annotated, fname, html_minification)

def copy_assets(state, assets, copy_fn, output_directory):
    if copy_fn is None:
        return state

    for (path, name) in assets:
        src = os.path.join(path, name)
        dst = os.path.join(output_directory, name)
        if copy_fn is not shutil.copy:
            try:
                os.unlink(dst)
            except FileNotFoundError:
                pass
        try:
            copy_fn(src, dst)
        except (shutil.SameFileError, FileExistsError):
            pass

    return state

def dump_html_standalone(snippets, fname, webpage_style,
                         html_minification, include_banner, include_vernums,
                         assets, html_classes):
    from dominate import tags, document
    from dominate.util import raw
    from . import GENERATOR
    from .core import SerAPI
    from .pygments import HTML_FORMATTER
    from .html import ASSETS, ADDITIONAL_HEADS, JS_UNMINIFY, gen_banner, wrap_classes

    doc = document(title=fname)
    doc.set_attribute("class", "alectryon-standalone")

    doc.head.add(tags.meta(charset="utf-8"))
    doc.head.add(tags.meta(name="generator", content=GENERATOR))

    for hd in ADDITIONAL_HEADS:
        doc.head.add(raw(hd))
    if html_minification:
        doc.head.add(raw(JS_UNMINIFY))
    for css in ASSETS.ALECTRYON_CSS:
        doc.head.add(tags.link(rel="stylesheet", href=css))
    for link in (ASSETS.IBM_PLEX_CDN, ASSETS.FIRA_CODE_CDN):
        doc.head.add(raw(link))
    for js in ASSETS.ALECTRYON_JS:
        doc.head.add(tags.script(src=js))

    _record_assets(assets, ASSETS.PATH, ASSETS.ALECTRYON_CSS)
    _record_assets(assets, ASSETS.PATH, ASSETS.ALECTRYON_JS)

    pygments_css = HTML_FORMATTER.get_style_defs('.highlight')
    doc.head.add(tags.style(pygments_css, type="text/css"))

    if html_minification:
        html_classes.append("minified")

    cls = wrap_classes(webpage_style, *html_classes)
    root = doc.body.add(tags.article(cls=cls))
    if include_banner:
        root.add(raw(gen_banner(SerAPI.version_info(), include_vernums)))
    for snippet in snippets:
        root.add(snippet)

    return doc.render(pretty=False)

def prepare_json(obj):
    from .json import PlainSerializer
    return PlainSerializer.encode(obj)

def dump_json(js):
    from json import dumps
    return dumps(js, indent=4)

def dump_html_snippets(snippets):
    s = ""
    for snippet in snippets:
        s += snippet.render(pretty=True)
        s += "<!-- alectryon-block-end -->\n"
    return s

def dump_latex_snippets(snippets):
    s = ""
    for snippet in snippets:
        s += str(snippet)
        s += "\n%% alectryon-block-end\n"
    return s

def strip_extension(fname):
    for ext in EXTENSIONS:
        if fname.endswith(ext):
            return fname[:-len(ext)]
    return fname

def write_output(ext, contents, fname, output, output_directory):
    if output == "-" or (output is None and fname == "-"):
        sys.stdout.write(contents)
    else:
        if not output:
            output = os.path.join(output_directory, strip_extension(fname) + ext)
        with open(output, mode="w", encoding="utf-8") as f:
            f.write(contents)

def write_file(ext):
    return lambda contents, fname, output, output_directory: \
        write_output(ext, contents, fname, output, output_directory)

# No ‘apply_transforms’ in JSON pipelines: (we save the prover output without
# modifications).
PIPELINES = {
    'json': {
        'json':
        (read_json, annotate_chunks,
         prepare_json, dump_json, write_file(".io.json")),
        'snippets-html':
        (read_json, annotate_chunks, apply_transforms, gen_html_snippets,
         dump_html_snippets, write_file(".snippets.html")),
        'snippets-latex':
        (read_json, annotate_chunks, apply_transforms, gen_latex_snippets,
         dump_latex_snippets, write_file(".snippets.tex"))
    },
    'coq': {
        'null':
        (read_plain, parse_coq_plain, annotate_chunks),
        'webpage':
        (read_plain, parse_coq_plain, annotate_chunks, apply_transforms,
         gen_html_snippets, dump_html_standalone, copy_assets,
         write_file(".v.html")),
        'snippets-html':
        (read_plain, parse_coq_plain, annotate_chunks, apply_transforms,
         gen_html_snippets, dump_html_snippets, write_file(".snippets.html")),
        'snippets-latex':
        (read_plain, parse_coq_plain, annotate_chunks, apply_transforms,
         gen_latex_snippets, dump_latex_snippets, write_file(".snippets.tex")),
        'lint':
        (read_plain, register_docutils, lint_docutils,
         write_file(".lint.json")),
        'rst':
        (read_plain, coq_to_rst, write_file(".v.rst")),
        'json':
        (read_plain, parse_coq_plain, annotate_chunks, prepare_json,
         dump_json, write_file(".io.json"))
    },
    'coq+rst': {
        'webpage':
        (read_plain, register_docutils, gen_docutils, copy_assets,
         write_file(".html")),
        'latex':
        (read_plain, register_docutils, gen_docutils, copy_assets,
         write_file(".tex")),
        'lint':
        (read_plain, register_docutils, lint_docutils,
         write_file(".lint.json")),
        'rst':
        (read_plain, coq_to_rst, write_file(".v.rst"))
    },
    'coqdoc': {
        'webpage': # transforms applied later
        (read_plain, parse_coq_plain, annotate_chunks,
         gen_html_snippets_with_coqdoc, dump_html_standalone,
         copy_assets, write_file(".html")),
    },
    'rst': {
        'webpage':
        (read_plain, register_docutils, gen_docutils, copy_assets,
         write_file(".html")),
        'latex':
        (read_plain, register_docutils, gen_docutils, copy_assets,
         write_file(".tex")),
        'lint':
        (read_plain, register_docutils, lint_docutils,
         write_file(".lint.json")),
        'coq':
        (read_plain, rst_to_coq, write_file(".v")),
        'coq+rst':
        (read_plain, rst_to_coq, write_file(".v"))
    },
    'md': {
        'webpage':
        (read_plain, register_docutils, gen_docutils, copy_assets,
         write_file(".html")),
        'latex':
        (read_plain, register_docutils, gen_docutils, copy_assets,
         write_file(".tex")),
        'lint':
        (read_plain, register_docutils, lint_docutils,
         write_file(".lint.json"))
    }
}

# CLI
# ===

EXTENSIONS = ['.v', '.json', '.v.rst', '.rst', '.md']
FRONTENDS_BY_EXTENSION = [
    ('.v', 'coq+rst'), ('.json', 'json'), ('.rst', 'rst'), ('.md', 'md')
]
BACKENDS_BY_EXTENSION = [
    ('.v', 'coq'), ('.json', 'json'), ('.rst', 'rst'),
    ('.lint.json', 'lint'),
    ('.snippets.html', 'snippets-html'),
    ('.snippets.tex', 'snippets-latex'),
    ('.v.html', 'webpage'), ('.html', 'webpage'),
    ('.v.tex', 'latex'), ('.tex', 'latex')
]

DEFAULT_BACKENDS = {
    'json': 'json',
    'coq': 'webpage',
    'coqdoc': 'webpage',
    'coq+rst': 'webpage',
    'rst': 'webpage',
    'md': 'webpage',
}

def infer_mode(fpath, kind, arg, table):
    for (ext, mode) in table:
        if fpath.endswith(ext):
            return mode
    MSG = """{}: Not sure what to do with {!r}.
Try passing {}?"""
    raise argparse.ArgumentTypeError(MSG.format(kind, fpath, arg))

def infer_frontend(fpath):
    return infer_mode(fpath, "input", "--frontend", FRONTENDS_BY_EXTENSION)

def infer_backend(frontend, out_fpath):
    if out_fpath:
        return infer_mode(out_fpath, "output", "--backend", BACKENDS_BY_EXTENSION)
    return DEFAULT_BACKENDS[frontend]

def resolve_pipeline(fpath, args):
    frontend = args.frontend or infer_frontend(fpath)

    assert frontend in PIPELINES
    supported_backends = PIPELINES[frontend]

    backend = args.backend or infer_backend(frontend, args.output)
    if backend not in supported_backends:
        MSG = """argument --backend: Frontend {!r} does not support backend {!r}: \
expecting one of {}"""
        raise argparse.ArgumentTypeError(MSG.format(
            frontend, backend, ", ".join(map(repr, supported_backends))))

    return frontend, backend, supported_backends[backend]

COPY_FUNCTIONS = {
    "copy": shutil.copy,
    "symlink": os.symlink,
    "hardlink": os.link,
    "none": None
}

def post_process_arguments(parser, args):
    if len(args.input) > 1 and args.output:
        parser.error("argument --output: Not valid with multiple inputs")

    if args.stdin_filename and "-" not in args.input:
        parser.error("argument --stdin-filename: input must be '-'")

    for dirpath in args.coq_args_I:
        args.sertop_args.extend(("-I", dirpath))
    for pair in args.coq_args_R:
        args.sertop_args.extend(("-R", ",".join(pair)))
    for pair in args.coq_args_Q:
        args.sertop_args.extend(("-Q", ",".join(pair)))

    # argparse applies ‘type’ before ‘choices’, so we do the conversion here
    args.copy_fn = COPY_FUNCTIONS[args.copy_fn]

    args.point, args.marker = args.mark_point
    if args.point is not None:
        try:
            args.point = int(args.point)
        except ValueError:
            MSG = "argument --mark-point: Expecting a number, not {!r}"
            parser.error(MSG.format(args.point))

    args.pipelines = [(fpath, *resolve_pipeline(fpath, args))
                      for fpath in args.input]

    return args

def build_parser():
    parser = argparse.ArgumentParser(
        description="""\
Annotate segments of Coq code with responses and goals.
Take input in Coq, reStructuredText, Markdown, or JSON \
and produce reStructuredText, HTML, LaTeX, or JSON output.""",
        fromfile_prefix_chars='@')

    VERSION_HELP = "Print version and exit."
    parser.add_argument("--version", action="version",
                        version="Alectryon v{}".format(__version__),
                        help=VERSION_HELP)

    in_ = parser.add_argument_group("Input configuration")

    INPUT_FILES_HELP = "Input files"
    in_.add_argument("input", nargs="+", help=INPUT_FILES_HELP)

    INPUT_STDIN_NAME_HELP = "Name of file passed on stdin, if any"
    in_.add_argument("--stdin-filename", default=None,
                     help=INPUT_STDIN_NAME_HELP)

    FRONTEND_HELP = "Choose a frontend. Defaults: "
    FRONTEND_HELP += "; ".join("{!r} → {}".format(ext, frontend)
                               for ext, frontend in FRONTENDS_BY_EXTENSION)
    FRONTEND_CHOICES = sorted(PIPELINES.keys())
    in_.add_argument("--frontend", default=None, choices=FRONTEND_CHOICES,
                     help=FRONTEND_HELP)


    out = parser.add_argument_group("Output configuration")

    BACKEND_HELP = "Choose a backend. Supported: "
    BACKEND_HELP += "; ".join(
        "{} → {{{}}}".format(frontend, ", ".join(sorted(backends)))
        for frontend, backends in PIPELINES.items())
    BACKEND_CHOICES = sorted(set(b for _, bs in PIPELINES.items() for b in bs))
    out.add_argument("--backend", default=None, choices=BACKEND_CHOICES,
                     help=BACKEND_HELP)

    OUT_FILE_HELP = "Set the output file (default: computed based on INPUT)."
    out.add_argument("-o", "--output", default=None,
                     help=OUT_FILE_HELP)

    OUT_DIR_HELP = "Set the output directory (default: same as each INPUT)."
    out.add_argument("--output-directory", default=None,
                     help=OUT_DIR_HELP)

    COPY_ASSETS_HELP = ("Chose the method to use to copy assets " +
                        "along the generated file(s) when creating webpages.")
    out.add_argument("--copy-assets", choices=list(COPY_FUNCTIONS.keys()),
                     default="copy", dest="copy_fn",
                     help=COPY_ASSETS_HELP)

    MARK_POINT_HELP = "Mark a point in the output with a given marker."
    out.add_argument("--mark-point", nargs=2, default=(None, None),
                     metavar=("POINT", "MARKER"),
                     help=MARK_POINT_HELP)

    NO_HEADER_HELP = "Do not insert a header with usage instructions in webpages."
    out.add_argument("--no-header", action='store_false',
                     dest="include_banner", default="True",
                     help=NO_HEADER_HELP)

    NO_VERSION_NUMBERS = "Omit version numbers in meta tags and headers."
    out.add_argument("--no-version-numbers", action='store_false',
                     dest="include_vernums", default=True,
                     help=NO_VERSION_NUMBERS)

    cache_out = parser.add_argument_group("Cache configuration")

    CACHE_DIRECTORY_HELP = ("Cache prover output in DIRECTORY.")
    cache_out.add_argument("--cache-directory", default=None, metavar="DIRECTORY",
                           help=CACHE_DIRECTORY_HELP)

    CACHE_COMPRESSION_HELP = ("Compress caches.")
    CACHE_COMPRESSION_CHOICES = ("none", "gzip", "xz")
    cache_out.add_argument("--cache-compression", nargs='?',
                           default=None, const="xz",
                           choices=CACHE_COMPRESSION_CHOICES,
                           help=CACHE_COMPRESSION_HELP)

    html_out = parser.add_argument_group("HTML output configuration")

    WEBPAGE_STYLE_HELP = "Choose a style for standalone webpages."
    WEBPAGE_STYLE_CHOICES = ("centered", "floating", "windowed")
    html_out.add_argument("--webpage-style", default="centered",
                          choices=WEBPAGE_STYLE_CHOICES,
                          help=WEBPAGE_STYLE_HELP)

    HTML_MINIFICATION_HELP = (
        "Minify HTML files using backreferences for repeated content. "
        "(Backreferences are automatically expanded on page load,"
        " using a very small amount of JavaScript code.)"
    )
    html_out.add_argument("--html-minification", action='store_true',
                          default=False,
                          help=HTML_MINIFICATION_HELP)

    HTML_DIALECT_HELP = "Choose which HTML dialect to use."
    HTML_DIALECT_CHOICES = ("html4", "html5")
    html_out.add_argument("--html-dialect", default="html4",
                          choices=HTML_DIALECT_CHOICES,
                          help=HTML_DIALECT_HELP)

    latex_out = parser.add_argument_group("LaTeX output configuration")

    LATEX_DIALECT_HELP = "Choose which LaTeX dialect to use."
    LATEX_DIALECT_CHOICES = ("pdflatex", "xelatex", "lualatex")
    latex_out.add_argument("--latex-dialect", default="pdflatex",
                           choices=LATEX_DIALECT_CHOICES,
                           help=LATEX_DIALECT_HELP)

    subp = parser.add_argument_group("SerAPI process configuration")

    SERTOP_ARGS_HELP = "Pass a single argument to SerAPI (e.g. -Q dir,lib)."
    subp.add_argument("--sertop-arg", dest="sertop_args",
                      action="append", default=[],
                      metavar="SERAPI_ARG",
                      help=SERTOP_ARGS_HELP)

    I_HELP = "Pass -I DIR to the SerAPI subprocess."
    subp.add_argument("-I", "--ml-include-path", dest="coq_args_I",
                      metavar="DIR", nargs=1, action="append",
                      default=[], help=I_HELP)

    Q_HELP = "Pass -Q DIR COQDIR to the SerAPI subprocess."
    subp.add_argument("-Q", "--load-path", dest="coq_args_Q",
                      metavar=("DIR", "COQDIR"), nargs=2, action="append",
                      default=[], help=Q_HELP)

    R_HELP = "Pass -R DIR COQDIR to the SerAPI subprocess."
    subp.add_argument("-R", "--rec-load-path", dest="coq_args_R",
                      metavar=("DIR", "COQDIR"), nargs=2, action="append",
                      default=[], help=R_HELP)

    warn_out = parser.add_argument_group("Warnings configuration")

    LL_THRESHOLD_HELP = "Warn on lines longer than this threshold (docutils)."
    warn_out.add_argument("--long-line-threshold", type=int,
                          default=72, help=LL_THRESHOLD_HELP)

    debug = parser.add_argument_group("Debugging options")

    EXPECT_UNEXPECTED_HELP = "Ignore unexpected output from SerAPI."
    debug.add_argument("--expect-unexpected", action="store_true",
                       default=False, help=EXPECT_UNEXPECTED_HELP)

    DEBUG_HELP = "Print communications with prover process."
    debug.add_argument("--debug", action="store_true",
                       default=False, help=DEBUG_HELP)

    TRACEBACK_HELP = "Print error traces."
    debug.add_argument("--traceback", action="store_true",
                       default=False, help=TRACEBACK_HELP)

    return parser

def parse_arguments():
    parser = build_parser()
    return post_process_arguments(parser, parser.parse_args())


# Entry point
# ===========

def call_pipeline_step(step, state, ctx):
    params = list(inspect.signature(step).parameters.keys())[1:]
    return step(state, **{p: ctx[p] for p in params})

def build_context(fpath, args, frontend, backend):
    if fpath == "-":
        fname, fpath = "-", (args.stdin_filename or "-")
    else:
        fname = os.path.basename(fpath)

    dialect = _resolve_dialect(backend, args.html_dialect, args.latex_dialect)
    ctx = {**vars(args),
           "fpath": fpath, "fname": fname,
           "frontend": frontend, "backend": backend, "dialect": dialect,
           "assets": [], "html_classes": []}
    ctx["ctx"] = ctx

    if args.output_directory is None:
        if fname == "-":
            ctx["output_directory"] = "."
        else:
            ctx["output_directory"] = os.path.dirname(os.path.abspath(fpath))

    return ctx

def except_hook(etype, value, tb):
    from traceback import TracebackException
    for line in TracebackException(etype, value, tb, capture_locals=True).format():
        print(line, file=sys.stderr)

def process_pipelines(args):
    if args.debug:
        core.DEBUG = True

    if args.traceback:
        core.TRACEBACK = True
        sys.excepthook = except_hook

    if args.expect_unexpected:
        core.SerAPI.EXPECT_UNEXPECTED = True

    if args.output_directory:
        os.makedirs(os.path.realpath(args.output_directory), exist_ok=True)

    for fpath, frontend, backend, pipeline in args.pipelines:
        state, ctx = None, build_context(fpath, args, frontend, backend)
        for step in pipeline:
            state = call_pipeline_step(step, state, ctx)

def main():
    try:
        args = parse_arguments()
        process_pipelines(args)
    except (ValueError, FileNotFoundError, ImportError, argparse.ArgumentTypeError) as e:
        if core.TRACEBACK:
            raise e
        MSG = "Exiting early due to an error; use --traceback to diagnose:"
        print(MSG, file=sys.stderr)
        print(core.indent(str(e), "  "), file=sys.stderr)
        sys.exit(1)

# Alternative CLIs
# ================

def rstcoq2html():
    DESCRIPTION = 'Build an HTML document from an Alectryon Coq file.'
    _docutils_cmdline(DESCRIPTION, "coq+rst", "webpage")

def coqrst2html():
    DESCRIPTION = 'Build an HTML document from an Alectryon reStructuredText file.'
    _docutils_cmdline(DESCRIPTION, "rst", "webpage")

def rstcoq2latex():
    DESCRIPTION = 'Build a LaTeX document from an Alectryon Coq file.'
    _docutils_cmdline(DESCRIPTION, "coq+rst", "latex")

def coqrst2latex():
    DESCRIPTION = 'Build a LaTeX document from an Alectryon reStructuredText file.'
    _docutils_cmdline(DESCRIPTION, "rst", "latex")
