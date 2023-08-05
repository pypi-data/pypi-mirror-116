
import cv2
import numpy as np
from skimage import transform as trans

from .scrfd import SCRFD

class FaceDetector:
    def __init__(self, detect_onnx_path):
        self.face_detection = SCRFD(detect_onnx_path)
        self.img_thumb_width = 320 #640#480
        self.img_thumb_height = 400 #640#270
        self.detect_img_size = 112
        self.batch_size = 4

        self.margin_time = 1.25#0.7

        self.detect_sensitive_low = 0.5
        self.detect_sensitive_norm = 0.65
        self.detect_sensitive_high = 0.8
    def detect_face(self, img_file_path):

        img1 = cv2.imread(img_file_path)
        results2 = self.face_detection.detect(img1)
        detections = results2[0]
        landmarks = results2[1]

        scale_width = 1
        scale_height = 1

        outbboxes = None
        outlandmarks = None
        max_size = 0
        for i, result in enumerate(detections):
            result[0] = result[0] * scale_width
            result[2] = result[2] * scale_width
            result[1] = result[1] * scale_height
            result[3] = result[3] * scale_height
            result = [round(x) for x in result]
            landmark = np.asarray(landmarks[i])

            landmark[:, 0] = landmark[:, 0] * scale_width
            landmark[:, 1] = landmark[:, 1] * scale_height
            tem_size = ((result[2] - result[0]) + (result[3] - result[1])) / 2
            if tem_size > max_size:
                max_size = tem_size
                outbboxes = result.copy()
                outlandmarks = landmark.copy()
        return outbboxes, np.asarray(outlandmarks).astype(np.int)
    
    def get_face_img(self, img1):
        results2 = self.face_detection.detect(img1)
        detections = results2[0]

        scale_width = 1
        scale_height = 1

        outbboxes = None
        max_size = 0
        for _, result in enumerate(detections):
            result[0] = result[0] * scale_width
            result[2] = result[2] * scale_width
            result[1] = result[1] * scale_height
            result[3] = result[3] * scale_height
            result = [round(x) for x in result]

            tem_size = ((result[2] - result[0]) + (result[3] - result[1])) / 2
            if tem_size > max_size:
                max_size = tem_size
                outbboxes = result.copy()

        img_dis = None
        if np.shape(outbboxes) !=():
            img_dis = self.get_thumb(img1, outbboxes)
        return img_dis
    def detect_face_img(self, img1):
        img1 = np.transpose(img1, (1 ,2, 0))
        img_shape = np.shape(img1)
        y_cen = img_shape[0]/2
        x_cen = img_shape[1]/2
        results2 = self.face_detection.detect(img1)
        detections = results2[0]
        landmarks = results2[1]

        scale_width = 1
        scale_height = 1

        outbboxes = None
        outlandmarks = None
        dis_cen = 10000
        for i, result in enumerate(detections):
            result[0] = result[0] * scale_width
            result[2] = result[2] * scale_width
            result[1] = result[1] * scale_height
            result[3] = result[3] * scale_height
            result = [round(x) for x in result]
            landmark = np.asarray(landmarks[i])

            landmark[:, 0] = landmark[:, 0] * scale_width
            landmark[:, 1] = landmark[:, 1] * scale_height
            x_cen_tem = (result[2] + result[0])/2
            y_cen_tem = (result[3] + result[1])/2
            tem_size = np.sqrt((x_cen_tem -x_cen)*(x_cen_tem -x_cen) + (y_cen_tem - y_cen)*(y_cen_tem - y_cen))
            if tem_size < dis_cen:
                dis_cen = tem_size
                outbboxes = result.copy()
                outlandmarks = landmark.copy()
        if np.shape(outlandmarks) !=():
            outlandmarks =np.asarray(outlandmarks).astype(np.int)
        return outbboxes, outlandmarks


    def align_face(self, img, bbox, landmark):
        warp_img = self.preprocess_detect(img, bbox=bbox, landmark=landmark,
                                          img_size=str(self.detect_img_size)+','+str(self.detect_img_size))
        return warp_img

    def get_norm_from_thumb(self, img, bbox, landmark_points):
        img = np.transpose(img, (1, 2, 0))
        img_align = self.align_face(img, bbox, landmark_points)
        return img_align

    def get_thumb(self, img, bbox):
        (x, y, x2, y2, score) = bbox
        img_size = np.asarray(img.shape)[0:2]
        margin_x = int(self.margin_time * (x2 - x) / 2)
        margin_y = int(self.margin_time * (y2 - y) / 2)
        x_dis = int(np.maximum(x - margin_x, 0))
        y_dis = int(np.maximum(y - margin_y, 0))
        x_dis2 = int(np.minimum(x2 + margin_x, img_size[1]))
        y_dis2 = int(np.minimum(y2 + margin_y, img_size[0]))

        img_thumb = img[y_dis:y_dis2, x_dis:x_dis2, :]
        img_thumb = cv2.resize(img_thumb, (self.img_thumb_width, self.img_thumb_height))
        return img_thumb
    ## From origin full images
    def detect_and_align(self, img):
        ## Detect thumb imgs
        shape_img = np.shape(img)
        if shape_img[0] == self.img_thumb_height and shape_img[1] == self.img_thumb_width:
            img_thumb_tem = img.copy()
        else:
            img_thumb_tem = self.get_face_img(img)
        if np.shape(img_thumb_tem) ==():
            img_thumb_tem = cv2.resize(img, (self.img_thumb_width, self.img_thumb_height))
        ## Detect landmark, align
        bbox, img_align, score = self.get_align_from_thumb(img_thumb_tem)
        return bbox, img_align, img_thumb_tem, score
    ## From thumb images
    def get_align_from_thumb(self, img_thumb_tem):
        bbox = None
        score = 0.0
        img_thumb_tem = np.transpose(img_thumb_tem, (2, 0, 1))
        info, landmark = self.detect_face_img(img_thumb_tem)
        if np.shape(landmark) !=():
            bbox = info[:4]
            score = info[4]
            img_align = self.get_norm_from_thumb(img_thumb_tem, bbox, landmark)
        else:
            img_align = cv2.resize(img_thumb_tem, (self.detect_img_size, self.detect_img_size))
        return bbox, img_align, float(score)

    def preprocess_detect(self, img, landmark=None, bbox=None, **kwargs):
        image_size = [112, 112]
        M = None
        if landmark is not None:
            assert len(image_size) == 2
            src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041]], dtype=np.float32)
            if image_size[1] == 112:
                src[:, 0] += 8.0
            dst = landmark.astype(np.float32)

            tform = trans.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2, :]

        if M is None:
            if bbox is None:  # use center crop
                det = np.zeros(4, dtype=np.int32)
                det[0] = int(img.shape[1] * 0.0625)
                det[1] = int(img.shape[0] * 0.0625)
                det[2] = img.shape[1] - det[0]
                det[3] = img.shape[0] - det[1]
            else:
                det = bbox
            margin = kwargs.get('margin', 44)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2, 0)
            bb[1] = np.maximum(det[1] - margin / 2, 0)
            bb[2] = np.minimum(det[2] + margin / 2, img.shape[1])
            bb[3] = np.minimum(det[3] + margin / 2, img.shape[0])
            ret = img[bb[1]:bb[3], bb[0]:bb[2], :]
            if len(image_size) > 0:
                ret = cv2.resize(ret, (image_size[1], image_size[0]))
            return ret
        else:  # do align using landmark
            assert len(image_size) == 2
            warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)

            return warped
