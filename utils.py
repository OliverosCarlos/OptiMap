import math
from PyQt5.QtCore import QPointF

class Utils:
    def __init__(self):
        self.name = ""
        
    def getGroupCount(self, grp, width):
        return [(x,x+width) for x in range(0, math.ceil(grp)*width , width) ]
    
    def getVerticalCoords(self, items_count, offset):
        gap=50
        vr_z = math.ceil(items_count*offset+gap*items_count)
        return ( [x for x in range(0, vr_z, offset+gap) ], vr_z )
    
    def getCenterPointLine(self, boundingRect) -> QPointF:
        return QPointF( boundingRect.topRight().x(), (boundingRect.bottomRight().y()-boundingRect.topRight().y())/2 )