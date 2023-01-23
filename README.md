# YOLOR
implementation of paper - [You Only Learn One Representation: Unified Network for Multiple Tasks](https://arxiv.org/abs/2105.04206)

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/you-only-learn-one-representation-unified/real-time-object-detection-on-coco)](https://paperswithcode.com/sota/real-time-object-detection-on-coco?p=you-only-learn-one-representation-unified)

![Unified Network](https://github.com/WongKinYiu/yolor/blob/main/figure/unifued_network.png)

<img src="https://github.com/WongKinYiu/yolor/blob/main/figure/performance.png" height="480">

## About the repo

This repo is the example of detecting objects via class-based inference structure and counting specified objects

## Get Started

Before everything, you must have cuda-cudnn-torch installed. (Preffered Cuda-11.3, Cudnn-8.2.1 and Pytorch for Cuda 11.3)

## Pretrained weights

You can download pretrained weights via https://drive.google.com/file/d/1Tdn3yqpZ79X7R1Ql0zNlNScB1Dv9Fp76/view

!!! Use pip3 instead of pip for python3.x 

```
https://github.com/ozgurkaplanturgut/YolorObjectDetectionAndCounting.git
cd YolorObjectDetectionAndCounting
pip3 install -r requirements
```
After these points, you are free to run yolor_inference.py file.


```
@article{ozgurK,
  title={You Only Learn One Representation: Class-based structure for inference},
  year={2023}
}
```
