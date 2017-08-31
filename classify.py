from nets.vgg_f import vggf
from nets.caffenet import caffenet
from nets.vgg_16 import vgg16
from nets.vgg_19 import vgg19
from nets.googlenet import googlenet
from nets.resnet_50 import resnet50
from nets.resnet_152 import resnet152
from nets.inception_v3 import inceptionv3
from misc.utils import *
import tensorflow as tf
import numpy as np
import argparse

def validate_arguments(args):
    nets = ['vggf', 'caffenet', 'vgg16', 'vgg19', 'googlenet', 'resnet50', 'resnet152', 'inceptionv3']
    if not(args.network in nets):
        print ('invalid network')
        exit (-1)
    #if args.evaluate:
        #if args.img_list is None or args.gt_labels is None:
        #    print ('provide image list and labels')
        #    exit (-1)

def choose_net(network, inp):    
    MAP = {
        'vggf'     : vggf,
        'caffenet' : caffenet,
        'vgg16'    : vgg16,
        'vgg19'    : vgg19, 
        'googlenet': googlenet, 
        'resnet50' : resnet50,
        'resnet152': resnet152, 
        'inceptionv3': inceptionv3,
    }
    
    if network == 'caffenet':
        size = 227
    elif network == 'inceptionv3':
        size = 299
    else:
        size = 224
        
    #placeholder to pass image

    return MAP[network](inp)

def evaluate(sess , net, in_im, net_name):
        sess.run(tf.global_variables_initializer())
        print "In evaluate function"
        return net['prob']

def predict(net, im_path, in_im, net_name):
    synset = open('misc/ilsvrc_synsets.txt').readlines()
    config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
    with tf.Session(config=config) as sess:
        sess.run(tf.global_variables_initializer())
        if net_name=='caffenet':
                im = img_preprocess(im_path, size=227)
        elif net_name == 'inceptionv3':
                im = v3_preprocess(im_path)
        else:
                im = img_preprocess(im_path)
        im = np.vstack([im,im])
        
                
        softmax_scores = sess.run(net['prob'], feed_dict={in_im: im})
        return net['prob']#scores
        inds = np.argsort(softmax_scores[0])[::-1][:5]
        print '{:}\t{:}'.format('Score','Class')
        for i in inds:
            print '{:.4f}\t{:}'.format(softmax_scores[0,i], synset[i].strip().split(',')[0])

def scores(inp_img):
    parser = argparse.ArgumentParser()
    parser.add_argument('--network', default='resnet50', help='The network eg. googlenet')
    parser.add_argument('--img_path', default='misc/sample.jpg',  help='Path to input image')
    parser.add_argument('--evaluate', default=True,  help='Flag to evaluate over full validation set')
    parser.add_argument('--img_list',  help='Path to the validation image list')
    parser.add_argument('--gt_labels', help='Path to the ground truth validation labels')
    args = parser.parse_args()
    validate_arguments(args)
    net = choose_net(args.network,inp_img)
    print "In scores function"
        #evaluate(net, args.img_list, inp_im, args.gt_labels, args.network)
    scores = net #evaluate(sess, net, inp_img, args.network)

    _,topk = tf.nn.top_k(scores['prob'],1)
    return scores,topk
    
if __name__ == '__main__':
    scores()
