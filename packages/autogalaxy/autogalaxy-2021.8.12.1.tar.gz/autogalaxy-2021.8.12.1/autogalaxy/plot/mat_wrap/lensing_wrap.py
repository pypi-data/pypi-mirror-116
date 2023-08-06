from autoarray.plot.mat_wrap.wrap import wrap_1d, wrap_2d


class HalfLightRadiusAXVLine(wrap_1d.AXVLine):
    pass


class EinsteinRadiusAXVLine(wrap_1d.AXVLine):
    pass


class ModelFluxesYXScatter(wrap_1d.YXScatter):
    pass


class LightProfileCentresScatter(wrap_2d.GridScatter):
    pass


class MassProfileCentresScatter(wrap_2d.GridScatter):
    pass


class MultipleImagesScatter(wrap_2d.GridScatter):
    pass


class CriticalCurvesPlot(wrap_2d.GridPlot):
    pass


class CausticsPlot(wrap_2d.GridPlot):
    pass
