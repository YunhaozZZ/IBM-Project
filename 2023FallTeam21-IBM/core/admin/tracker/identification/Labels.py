class Colors():
    labels = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    def labelColor(label):
        # Switch case on label
        # return an rgb tuple
        if label == 'red':
            return (0, 0, 255)
        elif label == 'green':
            return (0, 255, 0)
        elif label == 'blue':
            return (255, 0, 0)
        elif label == 'yellow':
            return (0, 255, 255)
        elif label == 'purple':
            return (255, 0, 255)
        elif label == 'orange':
            return (0, 150, 255)
        else:
            return (0, 0, 0)

class TrashTypes():
    labels = ['metal', 'glass', 'paper', 'plastic', 'food', 'textile']
    def labelColor(label):
        # Switch case on label
        # return an rgb tuple
        if label == 'metal':
            return (255, 0, 0)
        elif label == 'glass':
            return (0, 255, 0)
        elif label == 'paper':
            return (0, 0, 255)
        elif label == 'plastic':
            return (255, 255, 0)
        elif label == 'food':
            return (255, 0, 255)
        elif label == 'textile':
            return (0, 255, 255)
        else:
            return (0, 0, 0)
    