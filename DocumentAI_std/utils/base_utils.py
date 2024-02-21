class BaseUtils:
    @staticmethod
    def X1X2_to_xywh(bbox):
        """
        Convert bounding box from x1,y1,x2,y2 format to x,y,w,h format.
        """
        x1, y1, x2, y2 = bbox
        x = x1
        y = y1
        w = x2 - x1
        h = y2 - y1
        return [x, y, w, h]

    @staticmethod
    def X1X2X3X4_to_xywh(bbox):
        """
        Converts from x1, y1, x2, y2, x3, y3, x4, y4 to x, y, w, h.
        """
        x1, y1, x2, y2, x3, y3, x4, y4 = bbox
        min_x = min(x1, x2, x3, x4)
        min_y = min(y1, y2, y3, y4)
        max_x = max(x1, x2, x3, x4)
        max_y = max(y1, y2, y3, y4)
        w = max_x - min_x
        h = max_y - min_y
        return [min_x, min_y, w, h]
