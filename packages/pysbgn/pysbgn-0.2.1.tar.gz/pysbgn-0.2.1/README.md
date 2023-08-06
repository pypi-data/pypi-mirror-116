## pysbgn: supporting SBGN-ML v0.3 in Python


This package provides support for writing and reading [SBGN-ML](https://sbgn.github.io/specifications) v0.3 files. The code is auto-generated using [generateDS](https://pypi.org/project/generateDS/) with a few code fixes and modifications making it compatible with [libsbgn-python](https://github.com/matthiaskoenig/libsbgn-python) (which supports only SBGN-ML v0.2).


## Requirements

python 3.5+


## Installation

`pip install pysbgn`


## Examples

The read/write API is the same as in `libsbgn-python` so you can use the examples from [libsbgn-python documentation](https://libsbgn-python.readthedocs.io/en/latest/examples.html#Create-SBGN). Just make sure that the import statements are compatible with `libsbgn-python` as shown below. Note, however, that additional modules of `libsbgn-python` such as `utils` and `render` are not provided.

```python
from pysbgn import sbgn_core as libsbgn
from pysbgn.sbgn_core import notesType as Notes
from pysbgn.sbgn_core import extensionType as Extension
from pysbgn.sbgn_types import Language, Orientation, GlyphClass, ArcClass, Name, Version, ArcGroupClass
```


#### A simple example

Note: this example is taken from [`libsbgn-python`](https://libsbgn-python.readthedocs.io/en/latest/examples.html#Create-SBGN) and shortened to included only three glyphs and two arcs.

```python
from pysbgn import sbgn_core as libsbgn
from pysbgn.sbgn_types import Language, GlyphClass, ArcClass, Orientation

sbgn = libsbgn.sbgn()
map = libsbgn.map()
map.set_language(Language.PD)
sbgn.set_map(map)

# create a bounding box for the map
box = libsbgn.bbox(x=0, y=0, w=363, h=253)
map.set_bbox(box)

# two glyphs with labels
g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph1')
g.set_label(libsbgn.label(text='Ethanol'))
g.set_bbox(libsbgn.bbox(x=40, y=120, w=60, h=60))
map.add_glyph(g)

g = libsbgn.glyph(class_=GlyphClass.SIMPLE_CHEMICAL, id='glyph_ethanal')
g.set_label(libsbgn.label(text='Ethanal'))
g.set_bbox(libsbgn.bbox(x=220, y=110, w=60, h=60))
map.add_glyph(g)

# glyph with ports (process)
g = libsbgn.glyph(class_=GlyphClass.PROCESS, id='pn1', orientation=Orientation.HORIZONTAL)
g.set_bbox(libsbgn.bbox(x=148, y=168, w=24, h=24))
g.add_port(libsbgn.port(x=136, y=180, id="pn1.1"))
map.add_glyph(g)

# arcs
a = libsbgn.arc(class_=ArcClass.CONSUMPTION, source="glyph1", target="pn1.1", id="a01")
a.set_start(libsbgn.startType(x=98, y=160))
a.set_end(libsbgn.endType(x=136, y=180))
map.add_arc(a)

a = libsbgn.arc(class_=ArcClass.PRODUCTION, source="pn1.1", target="glyph_ethanal", id="a05")
a.set_start(libsbgn.startType(x=184, y=180))
a.set_end(libsbgn.endType(x=224, y=154))
map.add_arc(a)

sbgn.export('result.xml')
```

## Author

Vid Podpečan (vid.podpecan@ijs.si)

## License

MIT
