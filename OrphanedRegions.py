from MasyuExceptions import *

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
                return (pb.IsOpenUp(rowNum, colNum) and pb.isOpenDown(rowNum, colNum))
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