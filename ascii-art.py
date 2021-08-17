import os, signal, argparse, time
import cv2
from PIL import Image

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def signal_handler(sig, stack_frame):
        clear_term()
        exit(0)

def resize_img(img, nw):
        (w, h) = img.size
        aspect_ratio = float(h)/float(w)
        nh = int(aspect_ratio * nw)
        return img.resize((nw, nh))

def img_to_ascii(img, width):
        img = resize_img(img, width)
        init_px = list(img.getdata())
        mod_img = ''.join([ASCII_CHARS[v//25] for v in init_px])
        return'\n'.join([mod_img[i : i + width]
                         for i in range(0, len(mod_img), width)])

def move_term_cursor(y, x):
        print("\033[%d;%dH" % (y, x))

def clear_term():
        os.system('cls' if os.name == 'nt' else 'clear')

def init_vid(path):
        vid = cv2.VideoCapture(path)
        fps = vid.get(cv2.CAP_PROP_FPS)
        return (vid, fps)

def print_vid(vid, fps, width):
        success, img = vid.read()
        while success:
                move_term_cursor(0, 0)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                print(img_to_ascii(Image.fromarray(gray_img), width))
                success, img = vid.read()
                time.sleep(1/fps)

if __name__ == "__main__":
        descStr = "Play video files in the terminal as ascii art"
        parser = argparse.ArgumentParser(description=descStr)
        parser.add_argument('-f', dest='filepath', required=True)
        parser.add_argument('-w', dest='width', required=False)
        args = parser.parse_args()

        signal.signal(signal.SIGINT, signal_handler)
        
        (vid, fps) = init_vid(args.filepath)
        clear_term()
        print_vid(vid, fps, int(args.width) if args.width else 50)
