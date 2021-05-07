from MasyuExceptions import *
from Utilities import *

# Orphaned regions are formed by continuous lines which come in contact with two
# of the edges of the puzzle board.  Depending upon how the line continues after
# contacting the edge of the puzzle board, and depending upon whether there are
# circles inside, outside or both inside and outside the orphaned region, the
# puzzle may be deemed invalid.
#
# Orphaned regions are identified by scanning the puzzle board (top->bottom and
# left-> right).  This means that the START point for the region (where it first
# made contact with the edge of the puzzle board) always comes before the END
# point (where it again makes contact with the edge of the  puzzle board).

class OrphanedRegions():

    # Region point identifiers
    START = 0       # First point in orphaned region
    END = 1         # Last point in orphaned region

    # Edges where the orphaned regions makes contact
    TOP = 0             # Both start and end contact top edge
    BOTTOM = 1          # Both start and end contact bottom edge
    LEFT = 2            # Both start and end contact left edge
    RIGHT = 3           # Both start and end contact right edge
    TOP_RIGHT = 4       # Start contacts top; end contacts right edge
    TOP_LEFT = 5        # Start contacts top; end contacts left edge
    BOTTOM_RIGHT = 6    # Start contacts right; end contacts bottom edge
    BOTTOM_LEFT = 7     # Start contacts left; end contacts bottom edge
    TOP_BOTTOM = 8      # Start contacts top; end contacts bottom edge
    LEFT_RIGHT = 9      # Start contacts left; end contacts right edge

    # Quadrant identifiers
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

    # These identify the boundary we are checking for orphaned regions to be starting in
    TOP_ROW = 0
    BOTTOM_ROW = 1
    LEFT_COLUMN = 2
    RIGHT_COLUMN = 3

    # Based on whether this is the start or end point, and the edges of
    # contact, this method checks to see if the specified endpoint travels
    # away from (out) the interior of the orphaned region
    def hasLineOut(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_RIGHT)):
                return(pb.hasLineLeft(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or (edges == self.BOTTOM_RIGHT)):
                return(pb.hasLineUp(rowNum, colNum))
            elif ((edges == self.TOP_LEFT) or (edges == self.TOP_BOTTOM)):
                return(pb.hasLineRight(rowNum, colNum))
            elif (edges == self.LEFT_RIGHT):
                return(pb.hasLineDown(rowNum, colNum))
        else:       # (pointId == self.END)
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or (edges == self.TOP_BOTTOM)):
                return(pb.hasLineRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or
                  (edges == self.TOP_RIGHT) or (edges == self.LEFT_RIGHT)):
                return(pb.hasLineDown(rowNum, colNum))
            elif (edges == self.BOTTOM_RIGHT):
                return(pb.hasLineLeft(rowNum, colNum))

        # Never should reach here!!
        raise MasyuSolverException("hasLineOut(): unexpected condition encountered!!\n" + \
                                   "pointId=" + str(pointId) + "\n" + \
                                   "edges=" + str(edges), (rowNum, colNum))

    # Based on whether this is the start or end point, and the edges of
    # contact, this method checks to see if the specified endpoint travels
    # towards (into) the interior of the orphaned region
    def hasLineIn(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_RIGHT)):
                return (pb.hasLineRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or (edges == self.BOTTOM_RIGHT)):
                return (pb.hasLineDown(rowNum, colNum))
            elif ((edges == self.TOP_LEFT) or (edges == self.TOP_BOTTOM)):
                return (pb.hasLineLeft(rowNum, colNum))
            elif (edges == self.LEFT_RIGHT):
                return (pb.hasLineUp(rowNum, colNum))
        else:  # (pointId == self.END)
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or (edges == self.TOP_BOTTOM)):
                return (pb.hasLineLeft(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or (edges == self.TOP_RIGHT) or
                  (edges == self.LEFT_RIGHT)):
                return (pb.hasLineUp(rowNum, colNum))
            elif (edges == self.BOTTOM_RIGHT):
                return (pb.hasLineRight(rowNum, colNum))

        # Never should reach here!!
        raise MasyuSolverException("hasLineIn(): unexpected condition encountered!!\n" + \
                                   "pointId=" + str(pointId) + "\n" + \
                                   "edges=" + str(edges), (rowNum, colNum))

    # Based on whether this is the start or end point, and the edges of
    # contact, this method checks to see if the specified endpoint is open
    # (end where it comes in contact with the edge, meaning it still could
    # travel into or away from the interior of the orphaned region)
    def isOpen(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_LEFT) or
                    (edges == self.TOP_RIGHT) or (edges == self.TOP_BOTTOM)):
                return (pb.isOpenLeft(rowNum, colNum) and pb.isOpenRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or
                  (edges == self.BOTTOM_RIGHT) or (edges == self.LEFT_RIGHT)):
                return (pb.isOpenUp(rowNum, colNum) and pb.isOpenDown(rowNum, colNum))
        else:  # (pointId == self.END)
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or
                    (edges == self.BOTTOM_RIGHT) or (edges == self.TOP_BOTTOM)):
                return (pb.isOpenLeft(rowNum, colNum) and pb.isOpenRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or
                  (edges == self.TOP_RIGHT) or (edges == self.LEFT_RIGHT)):
                return (pb.isOpenUp(rowNum, colNum) and pb.isOpenDown(rowNum, colNum))

        # Never should reach here!!
        raise MasyuSolverException("isOpen(): unexpected condition encountered!!\n" + \
                                   "pointId=" + str(pointId) + "\n" + \
                                   "edges=" + str(edges), (rowNum, colNum))

    # Based on where the starting and endiing points are for the orphaned region,
    # determine which edges of the puzzle board the region is in contact with
    def determineEdges(self, pb, startRow, startCol, endRow, endCol):
        numRows, numCols = pb.getDimensions()

        if (((startCol == 0) and (endCol == (numCols - 1))) or
             ((startCol == (numCols - 1)) and (endCol == 0))):
            return(self.LEFT_RIGHT)
        elif (((startRow == 0) and (endRow == (numRows - 1))) or
              ((startRow == (numRows - 1)) and (endRow == 0))):
            return(self.TOP_BOTTOM)
        elif (startRow == endRow):
            if (startRow == 0):
                return(self.TOP)
            else:
                return(self.BOTTOM)
        elif (startCol == endCol):
            if (startCol == 0):
                return(self.LEFT)
            else:
                return(self.RIGHT)
        elif (startRow == 0):
            if (endCol == 0):
                return(self.TOP_LEFT)
            else:
                return(self.TOP_RIGHT)
        elif (endRow == (numRows - 1)):
            if (startCol == 0):
                return(self.BOTTOM_LEFT)
            else:
                return(self.BOTTOM_RIGHT)

        # Never should reach here!!
        raise MasyuOrphanedRegionException("determineEdges(): unexpected condition encountered!!", (startRow, startCol),
                                           (endRow, endCol))

    # The process for determining whether a point lies inside or outside an orphaned regions, involves
    # drawing a line towards the nearest corner of the puzzle board.  To determine which corner this is,
    # we need to determine which quadrant the point lies in.  The quadrants are defined as follows:
    #       Upper left = Q1
    #       Upper right = Q2
    #       Lower left = Q3
    #       Lower right = Q4
    #
    # Base on the quadrant, we will return the row and column offset needed to travel towards the
    # appropriate puzzzle board corner
    def determineQuadrant(self, numRows, numCols, rowNum, colNum):
        # Calculate the approximate center of the puzzle board
        centerR = int(numRows / 2)
        centerC = int(numCols / 2)

        if ((rowNum <= centerR) and (colNum <= centerC)):
            # Q1 - travel towards upper left corner
            return((self.Q1, -1, -1))
        elif ((rowNum <= centerR) and (colNum >= centerC)):
            # Q2 - travel towards upper right corner
            return((self.Q2, -1, 1))
        elif ((rowNum >= centerR) and (colNum <= centerC)):
            # Q3 - travel towards lower left corner
            return((self.Q3, 1, -1))
        else:
            # Q4 - travel towards lower right corner
            return((self.Q4, 1, 1))

    # Given a list of cell coordinates (rowNum, colNum), draw the corresponding
    # lines connecting the cells .. these define part of the orphaned region's
    # boundary.  This comes into play when determining whether a cell is inside
    # or outside the orphaned regions.  The remainder of the regions' boundary
    # is the "implied" boundary formed by the edges of the puzzle board.
    def drawBoundaryLine(self, pb, region):
        lineStartRow, lineStartCol = region[0]

        for i in range(1, len(region)):
            lineEndRow, lineEndCol = region[i]

            if (lineStartRow == lineEndRow):
                if (lineStartCol < lineEndCol):
                    pb.drawLineRight(lineStartRow, lineStartCol)
                else:
                    pb.drawLineLeft(lineStartRow, lineStartCol)
            else:
                if (lineStartRow < lineEndRow):
                    pb.drawLineDown(lineStartRow, lineStartCol)
                else:
                    pb.drawLineUp(lineStartRow, lineStartCol)

            lineStartRow = lineEndRow
            lineStartCol = lineEndCol

    # In order to determine whether a cell is inside or outside the
    # orphaned region, we need to mark the "implied" edges of the
    # region, as formed by the edges of the puzzle.  This method
    # takes care of marking the indicated portion of the top or
    # bottom row.  We mark the implied boundary by disabling the cells.
    def markRowImpliedBoundary(self, pb, rowNum, colStart, colEnd):
        for colNum in range(colStart, colEnd):
            pb.setCellDisabled(rowNum, colNum)

    # In order to determine whether a cell is inside or outside the
    # orphaned region, we need to mark the "implied" edges of the
    # region, as formed by the edges of the puzzle.  This method
    # takes care of marking the indicated portion of the left or
    # right column.  We mark the implied boundary by disabling the cells.
    def markColImpliedBoundary(self, pb, colNum, rowStart, rowEnd):
        for rowNum in range(rowStart, rowEnd):
            pb.setCellDisabled(rowNum, colNum)

    # Based on the edges forming the "implied" boundaries for the
    # orphaned region, we need to mark these "implied" boundaries,
    # (by disabling the cells), so that we have enough information
    # to allow us to determine cells inside or outside the region.
    def markImpliedBoundary(self, pb, edges, region):
        numRows, numCols = pb.getDimensions()
        regionStartRow, regionStartCol = region[0]
        regionEndRow, regionEndCol = region[-1]

        if (edges == self.TOP):
            # Implied boundary is in row 0
            self.markRowImpliedBoundary(pb, 0, (regionStartCol + 1), regionEndCol)
        elif (edges == self.BOTTOM):
            # Implied boundary is in the last row
            self.markRowImpliedBoundary(pb, (numRows - 1), (regionStartCol + 1), regionEndCol)
        elif (edges == self.RIGHT):
            # Implied boundary is in the last column
            self.markColImpliedBoundary(pb, (numCols - 1), (regionStartRow + 1), regionEndRow)
        elif (edges == self.LEFT):
            # Implied bounbard is in column 0
            self.markColImpliedBoundary(pb, 0, (regionStartRow + 1), regionEndRow)
        elif (edges == self.TOP_RIGHT):
            # Implied boundary is in row 0 and the last column
            self.markRowImpliedBoundary(pb, 0, (regionStartCol + 1), numCols)
            self.markColImpliedBoundary(pb, (numCols - 1), 0, regionEndRow)
        elif (edges == self.TOP_LEFT):
            # Implied boundary is in row 0 and column 0
            self.markRowImpliedBoundary(pb, 0, 0, regionStartCol)
            self.markColImpliedBoundary(pb, 0, 0, regionEndRow)
        elif (edges == self.BOTTOM_RIGHT):
            # Implied boundary is last row and last column
            self.markRowImpliedBoundary(pb, (numRows - 1), (regionEndCol + 1), numCols)
            self.markColImpliedBoundary(pb, (numCols - 1), (regionStartRow + 1), numRows)
        elif (edges == self.BOTTOM_LEFT):
            # Implied boundary is last row and column 0
            self.markRowImpliedBoundary(pb, (numRows - 1), 0, regionEndCol)
            self.markColImpliedBoundary(pb, 0, (regionStartRow + 1), numRows)
        elif (edges == self.TOP_BOTTOM):
            # Implied boundary is first and last row, and column 0
            self.markRowImpliedBoundary(pb, 0, 0, regionStartCol)
            self.markColImpliedBoundary(pb, 0, 1, (numRows - 1))
            self.markRowImpliedBoundary(pb, (numRows - 1), 0, regionEndCol)
        else:   # edges == self.LEFT_RIGHT
            # Implied boundary is first row, and first and last columns
            self.markColImpliedBoundary(pb, 0, 0, regionEndRow)
            self.markRowImpliedBoundary(pb, 0, 1, (numCols - 1))
            self.markColImpliedBoundary(pb, (numCols - 1), 0, regionEndRow)

    # The circles in the puzzle can have three different possible locations:
    #
    #       1) Inside the region (which includes the "implied" boundary lines)
    #       2) Along the boundary of the region (these are neither inside nor outside the region)
    #       3) Outside the region
    #
    # To determine whether a circle is inside or outside the region, we need to draw an
    # imaginary line from the cell to the nearest corner of the puzzle, counting the number
    # of times the imaginary line crosses the boundary (both the "hard" boundary and the
    # "implied" boundary.  If the number of line crossings is odd, then the circles lies
    # inside the region; if the value is even, then the circle is outside the region.
    #
    # This method will return a tuple:
    #
    #       number of circles on the hard boundary
    #       number of circles inside the region
    #       number of circles outside the region
    def countCirclesInOrphanedRegion(self, pb, region, edges):
        clone = pb.cloneBoardOnly()
        print("pb=", pb)
        print("clone=", clone)
        print("region=", region)
        print("edges=", edges)
        print("-------")
        Utilities.enableAllCells(clone)
        numRows, numCols = clone.getDimensions()

        # Draw the "hard" boundary lines formed by the region
        self.drawBoundaryLine(clone, region)

        # Draw the "implied" boundary lines formed by the edges of the puzzle board
        self.markImpliedBoundary(clone, edges, region)

        # Loop through each cell in the puzzle, and keep a total of where the circles lie
        circlesOnBoundary = 0
        circlesInside = 0
        circlesOutside = 0

        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                # We only care about cells which have a circle
                if not (clone.isDotAt(rowNum, colNum)):
                    # If the circle has lines, then we know that it is along the "hard" boundary.
                    # If the cell is disabled, then we know that it is along the "implied" boundary,
                    # so it is considered to be inside the region
                    numLines, l, r, u, d = clone.getLines(rowNum, colNum)
                    if (numLines > 0):
                        # Circle is on the "hard" boundary
                        circlesOnBoundary += 1
                    elif not (clone.isCellEnabled(rowNum, colNum)):
                        # Circle is on the "implied" boundary
                        circlesInside += 1
                    else:
                        # We will have to do some work to determine whether the circle is inside or outside
                        quadrant, rowDelta, colDelta = self.determineQuadrant(numRows, numCols, rowNum, colNum)

                        # Draw the imaginary line and count the boundary crossings
                        crossings = 0
                        nextCellRowNum = rowNum
                        nextCellColNum = colNum

                        while ((0 <= nextCellRowNum <= (numRows -1)) and (0 <= nextCellColNum <= (numCols - 1))):
                            # If the cell has lines, determine whether we crossed the line or not
                            numLines, l, r, u, d = clone.getLines(nextCellRowNum, nextCellColNum)
                            if (numLines > 0):
                                # If it is a straight line through the cell, then it counts as a crossing
                                if ((l and r) or (u and d)):
                                    crossings += 1
                                elif (quadrant == self.Q1):
                                    # Only certain lines are considered a crossing
                                    if ((l and u) or (r and d)):
                                        crossings += 1
                                    elif (((nextCellRowNum == 0) and ((crossings % 2) == 1) and d) or
                                          ((nextCellColNum == 0) and ((crossings % 2) == 1) and r)):
                                        # At the puzzle board boundary, if we are currently inside the
                                        # region and we cross over the boundary where the region also
                                        # meets with the boundary, then we need to count that as a crossing.
                                        crossings += 1
                                elif  (quadrant == self.Q4):
                                    # Only certain lines are considered a crossing
                                    if ((l and u) or (r and d)):
                                        crossings += 1
                                    elif (((nextCellRowNum == (numRows - 1)) and ((crossings % 2) == 1) and u) or
                                          ((nextCellColNum == (numCols - 1)) and ((crossings % 2) == 1) and l)):
                                        # At the puzzle board boundary, if we are currently inside the
                                        # region and we cross over the boundary where the region also
                                        # meets with the boundary, then we need to count that as a crossing.
                                        crossings += 1
                                elif (quadrant == self.Q2):
                                    # Only certain lines are considered a crossing
                                    if ((l and d) or (r and u)):
                                        crossings += 1
                                    elif (((nextCellRowNum == 0) and ((crossings % 2) == 1) and d) or
                                          ((nextCellColNum == (numCols - 1)) and ((crossings % 2) == 1) and l)):
                                        # At the puzzle board boundary, if we are currently inside the
                                        # region and we cross over the boundary where the region also
                                        # meets with the boundary, then we need to count that as a crossing.
                                        crossings += 1
                                elif (quadrant == self.Q3):
                                    # Only certain lines are considered a crossing
                                    if ((l and d) or (r and u)):
                                        crossings += 1
                                    elif (((nextCellRowNum == (numRows - 1)) and ((crossings % 2) == 1) and u) or
                                          ((nextCellColNum == 0) and ((crossings % 2) == 1) and r)):
                                        # At the puzzle board boundary, if we are currently inside the
                                        # region and we cross over the boundary where the region also
                                        # meets with the boundary, then we need to count that as a crossing.
                                        crossings += 1
                            elif not (clone.isCellEnabled(nextCellRowNum, nextCellColNum)):
                                # Entering a disabled cell (the "implied" boundary) counts as a crossing
                                crossings += 1

                            # Keep following the imaginary line
                            nextCellRowNum += rowDelta
                            nextCellColNum += colDelta

                        # Even number of crossing means outside the region; odd means inside
                        if ((crossings % 2) == 0):
                            circlesOutside += 1
                        else:
                            circlesInside += 1

        return((circlesOnBoundary, circlesInside, circlesOutside))

    # Given a starting cell location (which must reside at one of the puzzle board edges), follow the
    # path until either we reach another edge of the puzzle (thus forming an orphaned region), or
    # until the path ends (in which case we don't care about this pathway, because it didn't form an
    # orphaned region).  We are also provided with the row and column offsets telling us where to
    # travel to next.  To prevent a pathway from being processed again, the cells are marked as
    # 'processed' as we follow the pathway.  The starting cell will have already been marked as
    # 'processed' by the calling method.  The starting cell is the boundary cell where the pathway
    # first travels away from the puzzle board edge.
    def processPathway(self, pb, rowNum, colNum, nextCellRowOffset, nextCellColOffset, orphanedRegions):
        activePath = []
        activePath.append((rowNum, colNum))

        # Add the offsets to get the location of the next cell in the line
        rowNum += nextCellRowOffset
        colNum += nextCellColOffset

        numRows, numCols = pb.getDimensions()

        # Keep following the line until it either ends, or it reaches an edge
        while (True):
            # Mark the cell as processed
            pb.setCellProcessedFlag(rowNum, colNum)

            # Add the cell to the active pathway being followed
            activePath.append((rowNum, colNum))

            # If we reached and edge again, then we're done
            if ((rowNum == 0) or (rowNum == (numRows - 1)) or (colNum == 0) or (colNum == (numCols - 1))):
                orphanedRegions.append(activePath)
                return(orphanedRegions)
            else:
                # Keep following the line, if it continues
                numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                nextCellRowOffset, nextCellColOffset = Utilities.chooseNextLineToFollow(nextCellRowOffset, nextCellColOffset,
                                                                                        l, r, u, d)
                if ((nextCellRowOffset == -1) and (nextCellColOffset == -1)):
                    # Line ended; no region found
                    return(orphanedRegions)
                else:
                    # Line continued on, so keep followiing it
                    rowNum += nextCellRowOffset
                    colNum += nextCellColOffset

    # Orphaned regions are formed by lines (pathways) which start and end at one of the
    # puzzle board edges.  When this method is called, it is told (via the 'startingPoint' parameter),
    # which of the four puzzle board edge is to be checked.  This method ends up getting called 4
    # times; once for each edge.
    #
    # It should be noted that we don't bother checking any of the four corners!  That is because it is
    # not possible for a line originating in a corner to travel away from the puzzle board edge .. the
    # line will always continue along the edge.  Therefore, when looking for orphaned regions, we can
    # skip the cells in the corners.
    def findOrphanedRegions(self, pb, startingPoint, orphanedRegions):
        numRows, numCols = pb.getDimensions()

        # Based on which edge we are processing, set up the search constraints accordingly
        if (startingPoint == self.TOP_ROW):
            startRow = 0
            endRow = 1
            startCol = 1
            endCol = (numCols - 1)
        elif (startingPoint == self.BOTTOM_ROW):
            startRow = (numRows - 1)
            endRow = numRows
            startCol = 1
            endCol = (numCols - 1)
        elif (startingPoint == self.LEFT_COLUMN):
            startRow = 1
            endRow = (numRows - 1)
            startCol = 0
            endCol = 1
        else:        # (startingPoint == self.RIGHT_COLUMN)
            startRow = 1
            endRow = (numRows - 1)
            startCol = (numCols - 1)
            endCol = numCols

        # Look for unprocessed cells within the range of cells to be processed, which
        # lead away from the puzzle board edge; when found, the line will be followed,
        # to see if it forms an orphaned region
        for rowNum in range(startRow, endRow):
            for colNum in range(startCol, endCol):
                # Skip the cell, if it was already processed
                if (pb.wasCellProcessed(rowNum, colNum)):
                    continue

                # Mark the cell as having been processed
                pb.setCellProcessedFlag(rowNum, colNum)

                # Skip the cell if it doesn't have any lines
                numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                if (numLines == 0):
                    continue

                if (startingPoint == self.TOP_ROW):
                    # We only care about lines which turn away (down) from the top puzzle board edge
                    if (d):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, 1, 0, orphanedRegions)
                elif (startingPoint == self.BOTTOM_ROW):
                    # We only care about lines which turn away (up) from the bottom puzzle board edge
                    if (u):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, -1, 0, orphanedRegions)
                elif (startingPoint == self.LEFT_COLUMN):
                    # We only care about lines which turn away (right) from the left puzzle board edge
                    if (r):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, 0, 1, orphanedRegions)
                else:       # (startingPoiint == self.RIGHT_COLUMN)
                    # We only care about linew which turn away (left) from the right puzzle board edge
                    if (l):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, 0, -1, orphanedRegions)

        return(orphanedRegions)

    # If we detect the situation where an orphaned region is open on both ends, and there are circles outside
    # the region, but not inside, then we can block the path into the region
    def blockPathIn(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_RIGHT)):
                pb.markBlockedRight(rowNum, colNum)
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or (edges == self.BOTTOM_RIGHT)):
                pb.markBlockedDown(rowNum, colNum)
            elif ((edges == self.TOP_LEFT) or (edges == self.TOP_BOTTOM)):
                pb.markBlockedLeft(rowNum, colNum)
            elif (edges == self.LEFT_RIGHT):
                pb.markBlockedUp(rowNum, colNum)
        else:  # (pointId == self.END)
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or (edges == self.TOP_BOTTOM)):
                pb.markBlockedLeft(rowNum, colNum)
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or (edges == self.TOP_RIGHT) or
                  (edges == self.LEFT_RIGHT)):
                pb.markBlockedUp(rowNum, colNum)
            elif (edges == self.BOTTOM_RIGHT):
                pb.markBlockedRight(rowNum, colNum)

    # This method is responsible for searching the puzzle board to see if there exists any orphaned regions.
    # an orphaned region is formed when a pathway (line) forms a closed region with 1-2 sides of the region
    # being formed by the edges of the puzzle board.  Although not always a problem, they can be a problem
    # because there cannot be circles both inside and outside the orphaned regions .. this is because there
    # is no possible means for the solution path to travel into the region and back out, without forming
    # a 3-way line segment!  The situation is further complicated by how the lines travel from their
    # point of contact with the edge .. into the region, away from the region, or neither (because the line
    # stops).
    #
    # Each orphaned region starts where the line left the puzzle board edge, and ends
    # where it comes back in contact with the puzzle board edge.
    def checkForOrphanedRegions(self, pb):
        orphanedRegions = []
        changesMade = False

        # Start by marking all cells as "unprocessed"
        clone = pb.cloneAll()
        clone.clearAllCellProcessedFlags()

        # Search for orphaned regions starting in:
        #   (1) top row  (2) bottom row   (3) left column   (4) right column
        orphanedRegions = self.findOrphanedRegions(clone, self.TOP_ROW, orphanedRegions)
        orphanedRegions = self.findOrphanedRegions(clone, self.BOTTOM_ROW, orphanedRegions)
        orphanedRegions = self.findOrphanedRegions(clone, self.LEFT_COLUMN, orphanedRegions)
        orphanedRegions = self.findOrphanedRegions(clone, self.RIGHT_COLUMN, orphanedRegions)

        # If there are any orphaned regions, then check to see if they violate the puzzle rules
        totalNumCircles = Utilities.getNumberOfCircles(clone)

        for region in orphanedRegions:
            startCell = region[0]
            endCell = region[-1]
            startCellRowNum, startCellColNum = startCell
            endCellRowNum, endCellColNum = endCell

            # Determine which puzzle board edges the orphaned region comes in contact with
            edges = self.determineEdges(clone, startCellRowNum, startCellColNum, endCellRowNum, endCellColNum)

            # Determine the number of circles inside the region, outside the region, and along the boundard
            # of the region
            numBoundaryCircles, numCirclesInside, numCirclesOutside = self.countCirclesInOrphanedRegion(clone, region, edges)

            # It is never ok to have circles both inside and outside the orphaned region!
            # This check encapsulates many different situations, including case 4
            if ((numCirclesInside > 0) and (numCirclesOutside > 0)):
                raise MasyuOrphanedRegionException("Error 0 - found circles inside and outside an orphaned region",
                                                   startCell, endCell)

            # Cases 5 and 7:
            # Where one endpoint has a line heading into the region, and the other has a line
            # heading away from the region.  This is always invalid!
            if (self.hasLineIn(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineOut(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 7 - Invalid puzzle", startCell, endCell)
            elif (self.hasLineOut(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineIn(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 5 - Invalid puzzle", startCell, endCell)

            # If one or both ends of the line are open, and if there are no circles
            # inside the region, but there are circles on the outside,
            # then we can block the paths into the region, since they are invalid anyways. We
            # need to do this in the puzzle board which was passed in .. not in the clone we're
            # using to do our work in!
            if ((numCirclesInside == 0) and (numCirclesOutside > 0)):
                if (self.isOpen(clone, self.START, edges, startCellRowNum, startCellColNum)):
                    self.blockPathIn(pb, self.START, edges, startCellRowNum, startCellColNum)
                    changesMade = True

                if (self.isOpen(clone, self.END, edges, endCellRowNum, endCellColNum)):
                    self.blockPathIn(pb, self.END, edges, endCellRowNum, endCellColNum)
                    changesMade = True

            # Case 1:
            # Both ends have lines leading away from the region, but there are circles inside
            if ((numCirclesInside > 0) and self.hasLineOut(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineOut(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 1 - Invalid puzzle", startCell, endCell)

            # Case 2:
            # Start cell has a line out, the end is open, and there are circles inside
            if ((numCirclesInside > 0) and self.hasLineOut(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.isOpen(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 2 - Invalid puzzle", startCell, endCell)

            # Case 6
            # Start cell is open, end cell has a line out, and there are circles inside
            if ((numCirclesInside > 0) and self.isOpen(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineOut(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 6 - Invalid puzzle", startCell, endCell)

            # Case 3
            # Start cell is open, end cell has a line in, and there are circles outside
            if ((numCirclesOutside > 0) and self.isOpen(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineIn(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 3 - Invalid puzzle", startCell, endCell)

            # Case 8
            # Start cell has line in, end is open, and there are circles outside
            if ((numCirclesOutside > 0) and self.hasLineIn(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.isOpen(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 8 - Invalid puzzle", startCell, endCell)

            # Case 9
            # Start cell has line in, end cell has line in, and there are circles outside
            if ((numCirclesOutside > 0) and self.hasLineIn(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineIn(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 9 - Invalid puzzle", startCell, endCell)

        return(changesMade)