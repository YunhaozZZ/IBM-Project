from identification.ObjectIdentifier import ObjectIdentifier
from identification.ContourMerger import ContourMerger
from identification.Labels import TrashTypes
#Not Finished
# Concrete class for object identification by the 6 colors: red, green, blue, yellow, purple, orange
class TrashObjectIdentifier(ObjectIdentifier):

    # List with metal glass paper plastic food textile
    TrashTypes = TrashTypes.labels

    def identifyObjects(self, image):
        pass