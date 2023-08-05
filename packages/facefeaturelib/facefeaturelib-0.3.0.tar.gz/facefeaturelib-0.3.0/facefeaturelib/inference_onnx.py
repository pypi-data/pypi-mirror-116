import os
import cv2
import numpy as np
import onnxruntime as nxrun
from .face_detector import FaceDetector

class ImageFeatureGenerator:
    def __init__(self, ident_onnx_path, quality_onnx_path, detect_onnx_path, face_id_tflite_path):
        self._ident_onnx_path = ident_onnx_path
        self._quality_onnx_path =  quality_onnx_path
        self._face_id_tflite_path = face_id_tflite_path
        self._face_detector = FaceDetector(detect_onnx_path)
    
    # get align face
    def _detect_face(self, image):
        # print(image.shape)
        _, align_face,_,_ = self._face_detector.detect_and_align(image)
        if align_face.shape[2] != 3:
            return []
        return align_face
    def detect_face(self, image):
        # print(image.shape)
        bbox, align_face, thumb_face,score = self._face_detector.detect_and_align(image)
        if align_face.shape[2] != 3:
            return []
        return bbox, align_face, thumb_face, score
    # generete feature from align face
    def generate_feature(self, img):
        sess = nxrun.InferenceSession(self._ident_onnx_path)
        
        img = cv2.resize(img, (112,112))
        img = img[:, :, ::-1]
        
        input_data = np.array([img], dtype=np.float32)
        input_data = np.transpose(input_data, (0,3,1,2))
        input_name = sess.get_inputs()[0].name
        feature = sess.run(None, {input_name: input_data})[0][0]
        
        del sess
        
        return feature

    def generate_feature_128(self, img):
        import tensorflow as tf
        interpreter = tf.lite.Interpreter(model_path=self._face_id_tflite_path)

        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        img = cv2.resize(img, (112,112))
        img = img[:, :, ::-1]
        
        input_data = np.array([img], dtype=np.float32)
        # input_data = np.transpose(input_data, (0,3,1,2))

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        return output_data[0]

    def get_align_face(self, image_path):
        img = cv2.imread(image_path)
        align_face = self._detect_face(img)
        return align_face

    def get_quality(self, img):
        labels = ["bad", "good", "mask", "very_good"]
        sess = nxrun.InferenceSession(self._quality_onnx_path)
        img = cv2.resize(img, (112,112))
        img = img / 127.5
        img = img - 1
        img = img[:, :, ::-1]
        input_data = np.array([img], dtype=np.float32)
        input_data = np.transpose(input_data, (0,3,1,2))
        input_name = sess.get_inputs()[0].name
        result = sess.run(None, {input_name: input_data})[0][0]
        predict = np.argmax(result)
        del sess
        return predict, labels[predict]

    def get_face_quality(self, image_path):
        img = self.get_align_face(image_path)
        if img == []:
            return -1, -1
        idx, label = self.get_quality(img)
        return idx, label

    # case: receive base64 or array image
    def get_feature(self, img):
        pass
    
    # case: receive image_path from somewhere such as minio
    def get_feature_from_path(self, image_path):
        img = cv2.imread(image_path)
        align_face = self._detect_face(img)
        if align_face == []:
            return -1
        feature = self.generate_feature(align_face)
        return feature
    
    def get_feature_128_from_path(self, image_path):
        img = cv2.imread(image_path)
        align_face = self._detect_face(img)
        if align_face == []:
            return -1
        feature = self.generate_feature_128(align_face)
        return feature

# if __name__ == "__main__":
#     image_path = "test_data/69264356101573563301609675830640888568610816n-15696603325551387270557.jpg"
#     # ident_onnx_path = 'facefeaturelib/onnx/identification_mask.onnx'
#     ident_onnx_path = 'onnx/face_id_mobile.onnx'
#     face_id_tflite_path = 'tflite/tf_arcface_100_v1.tflite'
#     quality_onnx_path = 'onnx/face_quality_42.onnx'
#     detect_onnx_path = 'onnx/scrfd_2.5g_bnkps_shape640x640.onnx'
#     generator = ImageFeatureGenerator( ident_onnx_path, quality_onnx_path, detect_onnx_path, face_id_tflite_path)
#     feature = generator.get_feature_128_from_path(image_path)
#     # feature = generator.get_feature_from_path(image_path)
    # print(feature.shape)
    # idx, label = generator.get_face_quality(image_path)
    # print(idx, label)