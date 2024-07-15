/*
Language: Turtle
Author: Mark Ellis <mark.ellis@stardog.com>, Vladimir Alexiev <vladimir.alexiev@ontotext.com>
Category: common
Description: Terse RDF Triple Language for the semantic web
Website: https://www.w3.org/TR/turtle/
*/

function hljsDefineTurtle(hljs) {
  const KEYWORDS = {
    keyword: 'base|10 prefix|10 @base|10 @prefix|10',
    literal: 'true|0 false|0',
    built_in: 'a|0',
  };

  const IRI_LITERAL = {
    // https://www.w3.org/TR/turtle/#grammar-production-IRIREF
    className: 'literal',
    relevance: 1, // XML tags look also like relative IRIs
    begin: /</,
    end: />/,
    illegal: /[^\x00-\x20<>"{}|^`]/, // TODO: https://www.w3.org/TR/turtle/#grammar-production-UCHAR
  };

  // https://www.w3.org/TR/turtle/#terminals
  const PN_CHARS_BASE =
    'A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\u10000-\uEFFFF';
  const PN_CHARS_U = PN_CHARS_BASE + '_';
  const PN_CHARS = '-' + PN_CHARS_U + '0-9\u00B7\u0300-\u036F\u203F-\u2040';
  const BLANK_NODE_LABEL = '_:[' + PN_CHARS_U + '0-9]([' + PN_CHARS + '.]*[' + PN_CHARS + '])?';
  const PN_PREFIX = '[' + PN_CHARS_BASE + ']([' + PN_CHARS + '.]*[' + PN_CHARS + '])?';
  const PERCENT = '%[0-9A-Fa-f][0-9A-Fa-f]';
  const PN_LOCAL_ESC = "\\\\[_~.!$&'()*+,;=/?#@%-]";
  const PLX = PERCENT + '|' + PN_LOCAL_ESC;
  const PNAME_NS = '(' + PN_PREFIX + ')?:';
  const PN_LOCAL =
    '([' +
    PN_CHARS_U +
    ':0-9]|' +
    PLX +
    ')([' +
    PN_CHARS +
    '.:]|' +
    PLX +
    ')*([' +
    PN_CHARS +
    ':]|' +
    PLX +
    ')?';
  const PNAME_LN = PNAME_NS + PN_LOCAL;
  const PNAME_NS_or_LN = PNAME_NS + '(' + PN_LOCAL + ')?';

  const PNAME = {
    begin: PNAME_NS_or_LN,
    relevance: 0,
    className: 'symbol',
  };

  const BLANK_NODE = {
    begin: BLANK_NODE_LABEL,
    relevance: 10,
    className: 'template-variable',
  };

  const LANGTAG = {
    begin: /@[a-zA-Z]+([a-zA-Z0-9-]+)*/,
    className: 'type',
    relevance: 5, // also catches objectivec keywords like: @protocol, @optional
  };

  const DATATYPE = {
    begin: '\\^\\^' + PNAME_LN,
    className: 'type',
    relevance: 10,
  };

  const TRIPLE_APOS_STRING = {
    begin: /'''/,
    end: /'''/,
    className: 'string',
    relevance: 0,
  };

  const TRIPLE_QUOTE_STRING = {
    begin: /"""/,
    end: /"""/,
    className: 'string',
    relevance: 0,
  };

  const APOS_STRING_LITERAL = JSON.parse(JSON.stringify(hljs.APOS_STRING_MODE));
  APOS_STRING_LITERAL.relevance = 0;

  const QUOTE_STRING_LITERAL = JSON.parse(JSON.stringify(hljs.QUOTE_STRING_MODE));
  QUOTE_STRING_LITERAL.relevance = 0;

  const NUMBER = JSON.parse(JSON.stringify(hljs.C_NUMBER_MODE));
  NUMBER.relevance = 0;

  return {
    case_insensitive: true,
    keywords: KEYWORDS,
    aliases: ['turtle', 'ttl', 'n3', 'ntriples'],
    contains: [
      LANGTAG,
      DATATYPE,
      IRI_LITERAL,
      BLANK_NODE,
      PNAME,
      TRIPLE_APOS_STRING,
      TRIPLE_QUOTE_STRING, // order matters
      APOS_STRING_LITERAL,
      QUOTE_STRING_LITERAL,
      NUMBER,
      hljs.HASH_COMMENT_MODE,
    ],
    exports: {
      LANGTAG: LANGTAG,
      DATATYPE: DATATYPE,
      IRI_LITERAL: IRI_LITERAL,
      BLANK_NODE: BLANK_NODE,
      PNAME: PNAME,
      TRIPLE_APOS_STRING: TRIPLE_APOS_STRING,
      TRIPLE_QUOTE_STRING: TRIPLE_QUOTE_STRING,
      APOS_STRING_LITERAL: APOS_STRING_LITERAL,
      QUOTE_STRING_LITERAL: QUOTE_STRING_LITERAL,
      NUMBER: NUMBER,
      KEYWORDS: KEYWORDS,
    },
  };
}

export default function (hljs) {
  hljs.registerLanguage('turtle', hljsDefineTurtle);
}
