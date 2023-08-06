import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.mmi1x2 import mmi1x2
from gdsfactory.types import ComponentFactory


@gf.cell
def splitter_chain(
    splitter: ComponentFactory = mmi1x2, n_devices: int = 3, **kwargs
) -> Component:
    """Chain of splitters

    .. code::

                __
             __|
          __|  |__
        _|  |__
         |__


    """
    c = gf.Component()
    splitter_component = gf.call_if_func(splitter, **kwargs)
    cref = c.add_ref(splitter_component)

    bend = gf.components.bezier()
    c.add_port(name="W0", port=cref.ports["W0"])
    c.add_port(name="E0", port=cref.ports["E0"])

    for i in range(1, n_devices):
        bref = c.add_ref(bend)
        bref.connect(port="1", destination=cref.ports["E1"])

        cref = c.add_ref(splitter_component)

        cref.connect(port="W0", destination=bref.ports["0"])
        c.add_port(name="E{}".format(i), port=cref.ports["E0"])

    c.add_port(name="E{}".format(n_devices), port=cref.ports["E1"])
    c.settings["component"] = splitter_component.get_settings()
    return c


if __name__ == "__main__":
    component = splitter_chain(splitter=gf.components.mmi1x2, n_devices=4)
    component.show()
    component.pprint()
