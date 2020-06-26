# layout.py - logiic for flexibly drawing core sections and their columns


# Dataset {name, scale, data_pairs}
# A core-level dataset
class Dataset:
    def __init__(self, name, data_range, data_pairs):
        self.name = name # core name
        self.data_range = data_range # (data min, data max)
        self.data_pairs = data_pairs

## Columns: responsible for drawing themselves given origin/params

# PlotColumn displays one or more Datasets
# - each Dataset has a show/hide state, color, draw order, etc.
class PlotColumn:
    def __init__(self, datasets):
        # (dataset, show/hide state)
        self.datasets = [(ds, True) for ds in datasets]

    def draw(self, dc, origin, height, width):
        for ds in self.datasets:
            dc.DrawText("{}".format(ds.name), origin[0] + 5, origin[0] + 5)


# ImageColumn displays one image fit to available space
# - name, source_file(?)

# SpliceColumn...special case of PlotColumn? Selection, etc, different logic
# Splice really a special case of hole? SpliceHoleLayout?

# Maybe skip a level of this hierarchy? Section/Core/Hole Layout all very similar

# Needed? depth/data pairs are grouped at core, not section, level
# SectionLayout displays one or more columns in order
# - for each column, pass draw origin, add width, draw
class SectionLayout:
    def __init__(self, cols):
        self.cols = cols

    def draw(self, dc, origin, height, width):
        for col in self.cols:
            col.draw(dc, origin, height, width)


# CoreLayout displays one or more SectionLayouts in order
# - draws section boundaries if enabled
# class CoreLayout:
#     def __init__(self, secs):
#         self.secs = secs

#     def draw(self, dc, origin, height, width):
#         for sec in self.secs:
#             sec.draw(dc, origin, height, width)
#             # pull SectionSummary and draw boundaries + names

class CoreLayout:
    def __init__(self, cols):
        self.cols = cols

    def draw(self, dc, origin, height, width):
        for col in self.cols:
            col.draw(dc, origin, height, width)
            # adjust origin for next column
        # draw section boundaries and names
        # draw images (section-based)


# HoleLayout displays one or more CoreLayouts in order
# - this level determines the visible depth ranges and draws only CoreLayouts
# in that range.
# - no need for show/hide here?
# - Display HoleHeader
class HoleLayout:
    def __init__(self, cores, header):
        self.cores = cores
        self.header = header

    def draw(self, dc, origin, height, width):
        # draw header at specified height
        # draw dotted line at left edge of hole plot area if self.showHoleGrid = True
        for core in self.cores:
            core.draw(dc, origin, height, width)
            # draw core markers


# HoleHeader displays id and other metadata for the displayed data types in the hole
# - hole-level data display at this point
class HoleHeader:
    # def __init__(self, name, datasets):
        # self.datatypes = datatypes # TODO support for multiple datatypes

    def __init__(self, holeName, holeDatatype, holeRange):
        self.name = holeName # hole name e.g. 341-U1351B
        self.datatype = holeDatatype
        self.range = holeRange

    # TODO? Handle multiple datatypes if needed, fit to available space with
    # height and width
    def draw(self, dc, origin, height, width):
        # dc.SetFont(font) use custom header font
        x = origin[0]
        y = origin[1] + 3
        lineSpacing = 13 # fudge factor, looks good on Win and Mac
        dc.DrawText(self.name, x, y)
        dc.DrawText(self.datatype, x, y + lineSpacing)
        dc.DrawText(self.range, x, y + lineSpacing * 2)


# Display a depth scale ruler
# class RulerLayout(self):
    # def __init__

# SiteLayout displays one or more HoleLayouts in order
# - master drawer for the DataCanvas (ignoring Splice for now)
# - show/hide HoleLayouts
# - draw each in turn, providing origin/params
# - knows which layout mouse is over
# - all assumes Vertical for now...could eventually do VerticalSiteLayout
# and HorizontalSiteLayout
class SiteLayout:
    def __init__(self, holes, height, width, hole_width):
        self.holes = [(h, True) for h in holes] # (hole, show/hide state)
        self.height = height
        self.width = width
        self.hole_width = hole_width # fixed for now

    def draw(self, dc, origin): # height?
        self.drawRuler(dc, origin)
        pos = origin[0] # track width of layouts drawn
        pos += 50 # ruler width
        for hole, show in self.holes:
            # if pos in range
            h_origin = (pos, origin[1])
            if show and self.visible(h_origin, self.hole_width):
                # clip?
                h.draw(dc, h_origin, self.height, self.hole_width)
                pos += self.hole_width
            if pos > self.width:
                break
        
        # done drawing holes, draw filler if needed?
    
    def drawRuler(self, dc, origin):
        pass

    def visible(self, x, width=0):
        return x < self.width and x + width >= 0

    def addHoleLayout(self, holeLayout):
        self.holes.append((holeLayout, True))