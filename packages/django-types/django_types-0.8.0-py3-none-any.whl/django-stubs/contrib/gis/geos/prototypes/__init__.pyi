from django.contrib.gis.geos.prototypes.coordseq import create_cs as create_cs
from django.contrib.gis.geos.prototypes.coordseq import cs_clone as cs_clone
from django.contrib.gis.geos.prototypes.coordseq import cs_getdims as cs_getdims
from django.contrib.gis.geos.prototypes.coordseq import cs_getordinate as cs_getordinate
from django.contrib.gis.geos.prototypes.coordseq import cs_getsize as cs_getsize
from django.contrib.gis.geos.prototypes.coordseq import cs_getx as cs_getx
from django.contrib.gis.geos.prototypes.coordseq import cs_gety as cs_gety
from django.contrib.gis.geos.prototypes.coordseq import cs_getz as cs_getz
from django.contrib.gis.geos.prototypes.coordseq import cs_is_ccw as cs_is_ccw
from django.contrib.gis.geos.prototypes.coordseq import cs_setordinate as cs_setordinate
from django.contrib.gis.geos.prototypes.coordseq import cs_setx as cs_setx
from django.contrib.gis.geos.prototypes.coordseq import cs_sety as cs_sety
from django.contrib.gis.geos.prototypes.coordseq import cs_setz as cs_setz
from django.contrib.gis.geos.prototypes.coordseq import get_cs as get_cs
from django.contrib.gis.geos.prototypes.geom import (
    create_collection as create_collection,
)
from django.contrib.gis.geos.prototypes.geom import (
    create_empty_polygon as create_empty_polygon,
)
from django.contrib.gis.geos.prototypes.geom import (
    create_linearring as create_linearring,
)
from django.contrib.gis.geos.prototypes.geom import (
    create_linestring as create_linestring,
)
from django.contrib.gis.geos.prototypes.geom import create_point as create_point
from django.contrib.gis.geos.prototypes.geom import create_polygon as create_polygon
from django.contrib.gis.geos.prototypes.geom import destroy_geom as destroy_geom
from django.contrib.gis.geos.prototypes.geom import geom_clone as geom_clone
from django.contrib.gis.geos.prototypes.geom import geos_get_srid as geos_get_srid
from django.contrib.gis.geos.prototypes.geom import geos_normalize as geos_normalize
from django.contrib.gis.geos.prototypes.geom import geos_set_srid as geos_set_srid
from django.contrib.gis.geos.prototypes.geom import geos_type as geos_type
from django.contrib.gis.geos.prototypes.geom import geos_typeid as geos_typeid
from django.contrib.gis.geos.prototypes.geom import get_dims as get_dims
from django.contrib.gis.geos.prototypes.geom import get_extring as get_extring
from django.contrib.gis.geos.prototypes.geom import get_geomn as get_geomn
from django.contrib.gis.geos.prototypes.geom import get_intring as get_intring
from django.contrib.gis.geos.prototypes.geom import get_nrings as get_nrings
from django.contrib.gis.geos.prototypes.geom import get_num_coords as get_num_coords
from django.contrib.gis.geos.prototypes.geom import get_num_geoms as get_num_geoms
from django.contrib.gis.geos.prototypes.predicates import geos_contains as geos_contains
from django.contrib.gis.geos.prototypes.predicates import geos_covers as geos_covers
from django.contrib.gis.geos.prototypes.predicates import geos_crosses as geos_crosses
from django.contrib.gis.geos.prototypes.predicates import geos_disjoint as geos_disjoint
from django.contrib.gis.geos.prototypes.predicates import geos_equals as geos_equals
from django.contrib.gis.geos.prototypes.predicates import (
    geos_equalsexact as geos_equalsexact,
)
from django.contrib.gis.geos.prototypes.predicates import geos_hasz as geos_hasz
from django.contrib.gis.geos.prototypes.predicates import (
    geos_intersects as geos_intersects,
)
from django.contrib.gis.geos.prototypes.predicates import geos_isclosed as geos_isclosed
from django.contrib.gis.geos.prototypes.predicates import geos_isempty as geos_isempty
from django.contrib.gis.geos.prototypes.predicates import geos_isring as geos_isring
from django.contrib.gis.geos.prototypes.predicates import geos_issimple as geos_issimple
from django.contrib.gis.geos.prototypes.predicates import geos_isvalid as geos_isvalid
from django.contrib.gis.geos.prototypes.predicates import geos_overlaps as geos_overlaps
from django.contrib.gis.geos.prototypes.predicates import (
    geos_relatepattern as geos_relatepattern,
)
from django.contrib.gis.geos.prototypes.predicates import geos_touches as geos_touches
from django.contrib.gis.geos.prototypes.predicates import geos_within as geos_within
