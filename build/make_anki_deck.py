import codecs
import sys
from xml.etree import ElementTree


def visit_commercial_examples(t):
    res = ''
    if t is None:
        return res
    pattern = u'{0.text}<br/>'
    for eg in t.findall('commercial_example'):
        res += pattern.format(eg)
    return res


def visit_vital_statistics(t):
    res = ''
    if t is None:
        return res
    pattern = u'{0}: {1[low]}-{1[high]}<br/>'
    text = u'{0}'
    for s in t:
        if s.tag == 'paragraph':
            res += text.format(s.text)
            continue
        stat_name = s.tag
        sdict = s.attrib
        try:
            res += pattern.format(stat_name, sdict)
        except KeyError:
            res += text.format(s.text)
    return res


def visit_tags(t):
    res = ''
    if t is None:
        return res
    pattern = u'{0.text} '
    for tag in t.findall('tag'):
        res += pattern.format(tag)
    return res


def write_line(out, cat, style):
    pattern = u"""\
{0[name]}\t{0[desc]}\t{0[number]}\t\
{1[id]}\t{1[name]}\t{1[overall_impression]}\t\
{1[aroma]}\t{1[apperance]}\t{1[flavor]}\t{1[mouthfeel]}\t{1[comments]}\t\
{1[history]}\t{1[characteristic_ingredients]}\t{1[style_comparison]}\t\
{1[vital_statistics]}\t{1[commercial_examples]}\t{1[tags]}
"""
    line = pattern.format(cat, style)
    out.write(line)


def main():
    fname = sys.argv[1]
    root = ElementTree.parse(fname).getroot()

    cat = root[0]
    cdict = dict(
        name=cat.get('name'),
        number=cat.get('number'),
        desc=cat.findtext('paragraph'),
    )

    out = codecs.open('anki/%s_anki_deck.txt' % cdict['name'], 'w', 'utf-8')
    for style in cat.findall('style'):
        sdict = dict(
            id=style.get('style_id'),
            name=style.get('style_name'),
            overall_impression=style.findtext('overallimpression/paragraph'),
            aroma=style.findtext('aroma/paragraph'),
            apperance=style.findtext('apperance/paragraph'),
            flavor=style.findtext('flavor/paragraph'),
            mouthfeel=style.findtext('mouthfeel/paragraph'),
            comments=style.findtext('comments/paragraph'),
            history=style.findtext('history/paragraph'),
            characteristic_ingredients=style.findtext(
                'characteristicingredients/paragraph'),
            style_comparison=style.findtext('stylecomparison/paragraph'),
            vital_statistics=visit_vital_statistics(
                style.find('vitalstatistics')),
            commercial_examples=visit_commercial_examples(
                style.find('commercialexamples')),
            tags=visit_tags(style.find('tags')))
        write_line(out, cdict, sdict)
    out.close()


if __name__ == "__main__":
    main()
