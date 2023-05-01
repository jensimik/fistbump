from urllib.parse import urlparse, urlunparse, urljoin
from typing import Set, Union, List, MutableMapping, Optional, NewType, TYPE_CHECKING

from pyquery import PyQuery

from lxml.html.clean import Cleaner
import lxml
from lxml import etree
from lxml.html import HtmlElement
from lxml.html import tostring as lxml_html_tostring
from lxml.html.soupparser import fromstring as soup_parse
from parse import search as parse_search
from parse import findall, Result
from w3lib.encoding import html_to_unicode

if TYPE_CHECKING:
    _Attrs = MutableMapping
    _Containing = Union[str, List[str]]
    _Encoding = NewType("_Encoding", str)
    _Find = Union[List["Element"], "Element"]
    _Html = Union[str, bytes]
    _Links = Set[str]
    _Result = Union[List["Result"], "Result"]
    _Text = NewType("_Text", str)
    _Url = NewType("_Url", str)
    _XPath = Union[List[str], List["Element"], str, "Element"]

DEFAULT_ENCODING = "utf-8"
DEFAULT_URL = "https://example.org/"

cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True


class MaxRetries(Exception):
    def __init__(self, message):
        self.message = message


class BaseParser:
    """A basic HTML/Element Parser, for Humans.

    :param element: The element from which to base the parsing upon.
    :param default_encoding: Which encoding to default to.
    :param html: HTML from which to base the parsing upon (optional).
    :param url: The URL from which the HTML originated, used for ``absolute_links``.
    """

    __slots__ = (
        "element",
        "url",
        "skip_anchors",
        "default_encoding",
        "_encoding",
        "_html",
        "_lxml",
        "_pq",
    )

    def __init__(
        self,
        *,
        element,
        default_encoding: Optional[str] = None,
        html: "_Html" = None,
        url: "_Url",
    ) -> None:
        self.element = element
        self.url = url
        self.skip_anchors = True
        self.default_encoding = default_encoding
        self._encoding = None
        self._html = html.encode(DEFAULT_ENCODING) if isinstance(html, str) else html
        self._lxml = None
        self._pq = None

    @property
    def raw_html(self) -> bytes:
        """Bytes representation of the HTML content."""
        if self._html:
            return self._html
        else:
            return (
                etree.tostring(self.element, encoding="unicode")
                .strip()
                .encode(self.encoding)
            )

    @raw_html.setter
    def raw_html(self, html: bytes) -> None:
        self._html = html

    @property
    def html(self) -> str:
        """Unicode representation of the HTML content"""
        if self._html:
            return self.raw_html.decode(self.encoding, errors="replace")
        else:
            return etree.tostring(self.element, encoding="unicode").strip()

    @html.setter
    def html(self, html: str) -> None:
        self._html = html.encode(self.encoding)

    @property
    def encoding(self) -> "_Encoding":
        """The encoding string to be used, extracted from the HTML and
        :class:`HTMLResponse <HTMLResponse>` headers.
        """
        # scan meta tags for charset
        if not self._encoding and self._html:
            self._encoding = html_to_unicode(self.default_encoding, self._html)[0]
            # fall back to httpx's detected encoding if decode fails
            try:
                self.raw_html.decode(self.encoding, errors="replace")
            except UnicodeDecodeError:
                self._encoding = self.default_encoding

        return self._encoding if self._encoding else self.default_encoding

    @encoding.setter
    def encoding(self, enc: str) -> None:
        self._encoding = enc

    @property
    def pq(self) -> PyQuery:
        """`PyQuery <https://github.com/gawel/pyquery/>`_ representation
        of the :class:`Element <Element>` or :class:`HTML <HTML>`.
        """
        if self._pq is None:
            self._pq = PyQuery(self.lxml)

        return self._pq

    @property
    def lxml(self) -> HtmlElement:
        """`lxml <https://lxml.de>`_ representation of the
        :class:`Element <Element>` or :class:`HTML <HTML>`.
        """
        if self._lxml is None:
            try:
                self._lxml = soup_parse(self.html, features="html.parser")
            except ValueError:
                self._lxml = lxml.html.fromstring(self.raw_html)

        return self._lxml

    @property
    def text(self) -> "_Text":
        """The text content of the :class:`Element <Element>` or :class:`HTML <HTML>`."""
        return self.pq.text()

    @property
    def full_text(self) -> "_Text":
        """The full text content (including links) of the :class:`Element <Element>`
        or :class:`HTML <HTML>`.
        """
        return self.lxml.text_content()

    def find(
        self,
        selector: str = "*",
        *,
        containing: "_Containing" = None,
        clean: bool = False,
        first: bool = False,
        _encoding: str = None,
    ) -> "_Find":
        """Given a CSS Selector, returns a list of :class:`Element <Element>`
        objects or a single one.

        :param selector: CSS Selector to use.
        :param clean: Whether or not to sanitize the found HTML of ``<script>`` and
            ``<style>`` tags.
        :param containing: If specified, only return elements that contain the provided text.
        :param first: Whether or not to return just the first result.
        :param _encoding: The encoding format.

        Example CSS Selectors:

        - ``a``
        - ``a.someClass``
        - ``a#someID``
        - ``a[target=_blank]``

        See W3School's `CSS Selectors Reference
        <https://www.w3schools.com/cssref/css_selectors.asp>`_
        for more details.

        If ``first`` is ``True``, only returns the first :class:`Element <Element>` found.
        """

        # Convert a single containing into a list.
        if isinstance(containing, str):
            containing = [containing]

        encoding = _encoding or self.encoding
        elements = [
            Element(element=found, url=self.url, default_encoding=encoding)
            for found in self.pq(selector)
        ]

        if containing:
            # elements_copy = elements.copy()
            # elements = []

            # for element in elements_copy:
            #     if any([c.lower() in element.full_text.lower() for c in containing]):
            #         elements.append(element)
            elements = [
                e
                for e in elements
                if any(c.lower() in e.full_text.lower() for c in containing)
            ]
            elements.reverse()

        # Sanitize the found HTML.
        if clean:
            elements_copy = elements.copy()
            elements = []

            for element in elements_copy:
                element.raw_html = lxml_html_tostring(cleaner.clean_html(element.lxml))
                elements.append(element)

        return _get_first_or_list(elements, first)

    def xpath(
        self,
        selector: str,
        *,
        clean: bool = False,
        first: bool = False,
        _encoding: Optional[str] = None,
    ) -> "_XPath":
        """Given an XPath selector, returns a list of :class:`Element <Element>` objects
        or a single one.

        :param selector: XPath Selector to use.
        :param clean: Whether or not to sanitize the found HTML of ``<script>`` and
            ``<style>`` tags.
        :param first: Whether or not to return just the first result.
        :param _encoding: The encoding format.

        If a sub-selector is specified (e.g. ``//a/@href``), a simple list of results is
        returned.

        See W3School's `XPath Examples
        <https://www.w3schools.com/xml/xpath_examples.asp>`_
        for more details.

        If ``first`` is ``True``, only returns the first :class:`Element <Element>` found.
        """
        selected = self.lxml.xpath(selector)

        elements = [
            Element(
                element=selection,
                url=self.url,
                default_encoding=_encoding or self.encoding,
            )
            if not isinstance(selection, etree._ElementUnicodeResult)
            else str(selection)
            for selection in selected
        ]  # type: List[Element]

        # Sanitize the found HTML
        if clean:
            elements_copy = elements.copy()
            elements = []

            for element in elements_copy:
                element.raw_html = lxml_html_tostring(cleaner.clean_html(element.lxml))
                elements.append(element)

        return _get_first_or_list(elements, first)

    def search(self, template: str) -> Result:
        """Search the :class:`Element <Element>` for the given Parse template.

        :param template: The Parse template to use.
        """

        return parse_search(template, self.html)

    def search_all(self, template: str) -> "_Result":
        """Search the :class:`Element <Element>` (multiple times) for the given parse
        template.

        :param template: The Parse template to use.
        """
        return [r for r in findall(template, self.html)]

    @property
    def links(self) -> "_Links":
        """All found links on page, in as–is form."""

        def gen():
            for link in self.find("a"):
                try:
                    href = link.attrs["href"].strip()
                    if (
                        href
                        and not (href.startswith("#") and self.skip_anchors)
                        and not href.startswith(("javascript:", "mailto:"))
                    ):
                        yield href
                except KeyError:
                    pass

        return set(gen())

    def _make_absolute(self, link):
        """Makes a given link absolute."""
        # Parse the link with stdlib.
        parsed = urlparse(link)._asdict()

        # If link is relative, then join it with base_url.
        if not parsed["netloc"]:
            return urljoin(self.base_url, link)

        # Link is absolute; if it lacks a scheme, add one from base_url.
        if not parsed["scheme"]:
            parsed["scheme"] = urlparse(self.base_url).scheme

            # Reconstruct the URL to incorporate the new scheme.
            parsed = (v for v in parsed.values())
            return urlunparse(parsed)

        # Link is absolute and complete with scheme; nothing to be done here.
        return link

    @property
    def absolute_links(self) -> "_Links":
        """All found links on page, in absolute form
        (`learn more <https://www.navegabem.com/absolute-or-relative-links.html>`_).
        """

        def gen():
            for link in self.links:
                yield self._make_absolute(link)

        return set(gen())

    @property
    def base_url(self) -> "_Url":
        """The base URL for the page. Supports the ``<base>`` tag
        (`learn more <https://www.w3schools.com/tags/tag_base.asp>`_)."""

        # support for <base> tag
        base = self.find("base", first=True)
        if base:
            result = base.attrs.get("href", "").strip()
            if result:
                return result

        # parse the url to separate out the path
        parsed = urlparse(self.url)._asdict()

        # remove any part of the path after the last '/'
        parsed["path"] = "/".join(parsed["path"].split("/")[:-1]) + "/"

        # reconstruct the url with the modified path
        parsed = (v for v in parsed.values())
        url = urlunparse(parsed)

        return url


class Element(BaseParser):
    """An element of HTML.

    :param element: The element from which to base the parsing upon.
    :param url: The URL from which the HTML originated, used for ``absolute_links``.
    :param default_encoding: Which encoding to default to.
    """

    __slots__ = "tag", "lineno", "_attrs"  # , 'session'

    def __init__(
        self,
        *,
        element,
        url: "_Url",
        default_encoding: Optional[str] = None,
    ) -> None:
        super().__init__(element=element, url=url, default_encoding=default_encoding)
        self.element = element
        self.tag = element.tag
        self.lineno = element.sourceline
        self._attrs = None

    def __repr__(self) -> str:
        attrs = [f"{a}={self.attrs[a]!r}" for a in self.attrs]
        return f'<Element {self.element.tag!r} {" ".join(attrs)}>'

    @property
    def attrs(self) -> "_Attrs":
        """Returns a dictionary of the attributes of the :class:`Element <Element>`
        (`learn more <https://www.w3schools.com/tags/ref_attributes.asp>`_).
        """
        if self._attrs is None:
            self._attrs = {k: v for k, v in self.element.items()}

            # split class and rel up, as there are usually many of them
            for attr in ["class", "rel"]:
                if attr in self._attrs:
                    self._attrs[attr] = tuple(self._attrs[attr].split())

        return self._attrs


class HTML(BaseParser):
    """An HTML document, ready for parsing.

    :param url: The URL from which the HTML originated, used for ``absolute_links``.
    :param html: HTML from which to base the parsing upon (optional).
    :param default_encoding: Which encoding to default to.
    """

    __slots__ = "session", "page", "next_symbol"

    def __init__(
        self,
        *,
        url: str = DEFAULT_URL,
        html: "_Html",
        default_encoding: Optional[str] = DEFAULT_ENCODING,
    ) -> None:
        # convert incoming unicode HTML into bytes
        if isinstance(html, str):
            html = html.encode(DEFAULT_ENCODING)

        pq = PyQuery(html)
        super().__init__(
            element=pq("html") or pq.wrapAll("<html></html>")("html"),
            html=html,
            url=url,
            default_encoding=default_encoding,
        )

    def __repr__(self) -> str:
        return f"<HTML url={self.url!r}>"


def _get_first_or_list(lst, first=False):
    if first:
        try:
            return lst[0]
        except IndexError:
            return None
    else:
        return lst
