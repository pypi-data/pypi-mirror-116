

class CustObject(object):
    """
    This class is representing a shot. Each instance of this class is holding the properties of one shot.
    """

    def __init__(self, oid, fid, object_class_idx, object_class_name, object_conf, class_score, bb_x1, bb_y1, bb_x2, bb_y2):
        """
        Constructor

        :param oid [required]: iasdf
        :param fid [required]: asdf
        :param object_class_name [required]: asdf
        :param conf_score [required]: asdf
        :param bb_x1,bb_y1,bb_x2,bb_y2 [required]: asdf
        """
        #print("create instance of shot ...");
        self.oid = oid
        self.fid = fid
        self.object_class_name = object_class_name
        self.object_class_idx = object_class_idx
        self.object_conf = object_conf
        self.class_score = class_score
        self.bb_x1 = bb_x1
        self.bb_y1 = bb_y1
        self.bb_x2 = bb_x2
        self.bb_y2 = bb_y2
        self.person_classification = None

    def convert2String(self):
        """
        Method to convert class member properties in a semicolon separated string.

        :return: string holding all properties of one shot.
        """
        tmp_str = str(self.fid) + ";" + str(self.oid) + ";" + str(self.bb_x1) + ";" + \
                  str(self.bb_y1) + ";" + str(self.bb_x2) + ";" + str(self.bb_y2) + ";" + str(self.object_conf) \
                  + ";" + str(self.class_score) + ";" + str(self.object_class_name) + ";" + str(self.object_class_idx)
        return tmp_str

    def add_classification(self, classification):
        if self.object_class_name != "person":
            print("Warning: trying to set classification for a crop that is not a person")
            return
        self.person_classification = classification

    def update_according_to_person_classification(self, classification):
        if self.object_class_name != "person":
            return
        self.add_classification(classification)
        if classification != "others":
            self.object_class_name = "person ({0})".format(classification)

    def printObjectInfo(self):
        """
        Method to a print summary of shot properties.
        """
        print("------------------------")
        print("object id: " + str(self.oid))
        print("frame id: " + str(self.fid))
        print("object_class_name: " + str(self.object_class_name))
        print("object_class_idx:" + str(self.object_class_idx))
        print("object_conf: " + str(self.object_conf))
        print("class_score: " + str(self.class_score))
        print("bounding box: (" + str(self.bb_x1) + "," + str(self.bb_y1) + ","
              + str(self.bb_x2) + "," + str(self.bb_y2) + ")")
