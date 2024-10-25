# Frequently Asked Questions

## API Results

#### 1. The address of my search results contains far-away places that don't belong there.

The endpoints computes the address from two sources in the OpenStreetMap data:
from administrative boundaries and from place nodes. Boundaries are the more
useful source. They precisely describe an area. So it is very clear for
the endpoints if a point belongs to an area or not. Place nodes are more complicated.
These are only points without any precise extent. So it has to take a
guess and assume that an address belongs to the closest place node it can find.
In an ideal world, the endpoints would not need the place nodes but there are
many places on earth where there are no precise boundaries available for
all parts that make up an address. This is in particular true for the more
local address parts, like villages and suburbs. Therefore it is not possible
to completely dismiss place nodes. And sometimes they sneak in where they
don't belong.

As a OpenStreetMap mapper, you can improve the situation in two ways: if you
see a place node for which already an administrative area exists, then you
should _link_ the two by adding the node with a 'label' role to the boundary
relation. If there is no administrative area, you can add the approximate
extent of the place and tag it place=<something> as well.

#### 2. When doing reverse search, the address details have parts that don't contain the point I was looking up.

There is a common misconception how the reverse API call works.
Reverse does not give you the address of the point you asked for. Reverse
returns the closest object to the point you asked for and then returns the
address of that object. Now, if you are close to a border, then the closest
object may be across that border. When it then returns the address,
it contains the county/state/country across the border.

#### 3. I get different counties/states/countries when I change the zoom parameter in the reverse query. How is that possible?

This is basically the same problem as in the previous answer.
The zoom level influences at which search rank it starts looking
for the closest object. So the closest house number maybe on one side of the
border while the closest street is on the other. As the address details contain
the address of the closest object found, you might sometimes get one result,
sometimes the other for the closest point.

#### 4. Can you return the continent?

The endpoint assigns each map feature one country. Those outside any administrative
boundaries are assigned a special no-country. Continents or other super-national
administrations (e.g. European Union, NATO, Custom unions) are not supported.

#### 5. My result has a wrong postcode. Where does it come from?

Most places in OSM don't have a postcode, so the endpoint tries to interpolate
one. It first look at all the places that make up the address of the place.
If one of them has a postcode defined, this is the one to be used. When
none of the address parts has a postcode either, the endpoint interpolates one
from the surrounding objects. If the postcode is for your result is one, then
most of the time there is an OSM object with the wrong postcode nearby.
