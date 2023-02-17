import cv2
import torch
import numpy as np
from torchvision.transforms.functional import to_tensor, to_pil_image
from model import Generator




torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

device = "cuda"
def initNet():
    net = Generator()
    net.load_state_dict(torch.load('./weights/face_paint_512_v2.pt', map_location="cpu"))
    net.to(device).eval()
    print("model loaded: ")
    return net


def oneFrameCvt(image, net):
    with torch.no_grad():
        image = to_tensor(image).unsqueeze(0) * 2 - 1
        out = net(image.to(device), False).cpu()
        out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
        out = to_pil_image(out)
    out = cv2.cvtColor(np.asarray(out), cv2.COLOR_BGR2RGB)
    torch.cuda.empty_cache()
    return out

def cvt2anime_video(video, output):
    net = initNet()
    vid = cv2.VideoCapture(video)
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vid.get(cv2.CAP_PROP_FPS)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = cv2.VideoWriter_fourcc(*"MP4V")
    video_out = cv2.VideoWriter(output, codec, fps, (width, height))

    index = 0
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        cv2.imshow("video", frame)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print(f"开始转换第{index+1}帧")
        out = oneFrameCvt(img, net)
        print(f"第{index + 1}帧转换完成")
        print(f"进度：{(index+1)/total*100}")
        cv2.imshow("video1", out)
        cv2.waitKey(1)
        video_out.write(out)
        index += 1

    vid.release()
    video_out.release()



if __name__ == '__main__':
    cvt2anime_video('./samples/video/3.mp4', './samples/temp/3.mp4')
