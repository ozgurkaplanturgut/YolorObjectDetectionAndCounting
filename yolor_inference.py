import enum
import os
import torch 
from models.models import *
from utils.datasets import letterbox
from utils.plots import plot_one_box
from utils.torch_utils import select_device

def load_classes(path):
    # Loads *.names file at 'path'
    with open(path, 'r') as f:
        names = f.read().split('\n')
    return list(filter(None, names))  # filter removes empty strings (such as last line)

class YoloR:
    def __init__(self,weights,cfg,names,device='0',img_size=1280):
        self.weights = weights
        self.cfg = cfg
        self.names = names
        self.device = select_device(device)
        self.img_size = img_size

        self.model = Darknet(self.cfg, self.img_size).cuda()
        self.model.load_state_dict(torch.load(self.weights, map_location=self.device)['model'])
        self.model.to(self.device).eval()
        self.names = load_classes(self.names)

        color_values = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]
        self.colors = {self.names[i]:color_values[i] for i in range(len(self.names))}
    
    def detect(self,img_raw,conf_thresh=0.4,iou_thresh=0.5):
        with torch.no_grad():
            img = letterbox(img_raw, new_shape=self.img_size, auto_size=64)[0]

            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(self.device)
            img = img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            
            predictions = self.model(img, augment=False)[0]
            predictions= non_max_suppression(predictions, conf_thresh, iou_thresh, classes=None, agnostic=False)[0]
            predictions[:, :4] = scale_coords(img.shape[2:], predictions[:, :4], img_raw.shape).round()             

            detection_lst = []
            for *xyxy,conf,cls in predictions:
                #bboxes
                x1,y1,x2,y2 = int(xyxy[0]),int(xyxy[1]),int(xyxy[2]),int(xyxy[3])
                #label to print
                #dets to draw
                detection_lst.append([self.names[int(cls)],[x1,y1,x2,y2],float(conf)])

            return detection_lst      
            
    
    def draw_bbox(self,img_raw,dets_list):      
        for lbl,bbox,conf in dets_list:
            label = '%s %.2f' % (lbl, conf)
            plot_one_box(bbox, img_raw, label=label, color=self.colors[lbl], line_thickness=1)

        return img_raw


if __name__=='__main__':
    yolor_detector=YoloR('yolor_p6.pt', 'cfg/yolor_p6.cfg', 'data/coco.names')
    cap=cv2.VideoCapture('test.mp4')

    while True:
        person_count=0
        ret, frame=cap.read()
        if not ret:
            break

        predictions=yolor_detector.detect(frame)
        for lbl,bbox,conf in predictions:
            if lbl=='person':
                person_count+=1

        processed_frame=yolor_detector.draw_bbox(frame, predictions)
        cv2.rectangle(processed_frame, (10, 0), (300, 40), (0,0,0), -1)
        cv2.putText(processed_frame, 'Person Count: '+str(person_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('dets', processed_frame)
        if cv2.waitKey(30) & 0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()    


