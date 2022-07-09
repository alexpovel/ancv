from ancv.visualization.skeletons import BerlinSkeleton
from ancv.visualization.themes import Basic, Plain, Theme


class BerlinPlain(BerlinSkeleton):
    @property
    def theme(self) -> Theme:
        return Plain()


class BerlinBasic(BerlinSkeleton):
    @property
    def theme(self) -> Theme:
        return Basic()
