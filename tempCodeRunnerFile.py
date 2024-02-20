def loadJsonFile(self):
        f = open(self.jfile)
        data = json.load(f)

        self.saveJsonData(data)

        for label, points in self.points_with_labels:
            group_label = []
            for point in points:
                group_point = []
                group_point.append(point.x())
                group_point.append(point.y())
                group_label.append(group_point)
            self.coordinates.append(group_label)

        f.close()