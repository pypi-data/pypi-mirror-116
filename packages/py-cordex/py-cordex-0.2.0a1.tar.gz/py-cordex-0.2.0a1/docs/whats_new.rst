.. currentmodule:: cordex

What's New
==========

.. ipython:: python
   :suppress:

    import pyremo 

v0.2.0 (unreleased)
-------------------

New Features
~~~~~~~~~~~~
- Included new sub regions (germany and prudence) for masking and analysis.
- Included function ``map_crs`` for coordinate transformations using cartopy.
  
Internal Changes
~~~~~~~~~~~~~~~~
- Tables are removed from the package and stored in an extra github repo.
- Tables are download at first access using pooch.

v0.1.2 (3 June 2021)
--------------------

This is a major restructuring release. The code base has been reduced significantly
and the main data structure are now xarray's datarrays. Several new domains have been
added.
