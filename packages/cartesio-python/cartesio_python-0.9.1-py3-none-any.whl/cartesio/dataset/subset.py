
class Subset(object):
    def __init__(self):
        self.x = []
        self.y = []
        self.preview_images = []

    def append(self, x, y):
        self.x.append(x)
        self.y.append(y)
    '''
    def rescale(self, factor):
        self.x = self.__rescale(self.x, factor)
        self.y = self.__rescale(self.y, factor)
        self.y = self.__rescale(self.y, 1. / factor)
        self.preview_images = [cv2.resize(pi, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA) for pi in self.preview_images]
        self.preview_images = [cv2.resize(pi, None, fx=1./factor, fy=1./factor, interpolation=cv2.INTER_CUBIC) for pi in self.preview_images]
    '''
    '''
    def __rescale(self, to_rescale, factor):
        new_x = []
        for x in to_rescale:
            sub_new_x = []
            for xi in x:
                if type(xi) == int:
                    sub_new_x.append(xi)
                else:
                    if factor > 1.:
                        sub_new_x.append(cv2.resize(xi, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC))
                    else:
                        sub_new_x.append(cv2.resize(xi, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA))
            new_x.append(sub_new_x)
        return new_x
    '''